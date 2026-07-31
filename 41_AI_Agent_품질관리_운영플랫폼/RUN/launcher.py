"""AI Agent 품질관리 운영플랫폼 통합 런처 (GUI).

서버 역할을 하는 컴퓨터(이 프로젝트가 있는 컴퓨터)에서 실행한다.
- ▶ 전체 시작 / ⏹ 전체 종료: docker compose(챗봇 API/Prometheus/Grafana) + Streamlit 대시보드를 한 번에 기동/종료
- 서비스별 ▶ 시작 / ⏹ 종료: 챗봇 API, Streamlit 대시보드, Prometheus, Grafana를 개별로 켜고 끌 수 있음
- Docker 엔진: 꺼져 있으면 자동으로 켜준다. 단, Docker Desktop을 통째로 "종료"하는 기능은 다른 프로젝트의
  컨테이너에도 영향을 줄 수 있어 위험하다고 판단해 의도적으로 넣지 않았다 (시작만 지원).
- 서비스별 버튼: 동료 공유용 LAN IP 링크를 기본 브라우저로 열기 (준비된 서비스부터 활성화)
- 창 X 버튼: 서비스 종료 후 창도 닫기
추가 패키지 없이 파이썬 표준 라이브러리(tkinter)만 사용한다.
"""
import os
import queue
import socket
import subprocess
import sys
import threading
import urllib.request
import webbrowser
from datetime import datetime
from pathlib import Path

import tkinter as tk
from tkinter import scrolledtext

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# (표시 이름, docker compose 서비스명(Streamlit은 docker가 아니라 None), 포트, 브라우저로 열 경로, 헬스체크 경로)
SERVICES = [
    ("🤖 챗봇 API (Swagger)", "app", 8000, "/docs", "/health"),
    ("📊 Streamlit 대시보드", None, 8501, "", "/"),
    ("📈 Prometheus", "prometheus", 9090, "", "/-/ready"),
    ("📉 Grafana", "grafana", 3000, "", "/api/health"),
]
HEALTH_TIMEOUT_SECONDS = 240  # 시작 버튼 클릭 후 이 시간 안에 준비 안 되면 실패로 간주 (Grafana 초기 DB 마이그레이션 대비)
DOCKER_START_TIMEOUT_SECONDS = 120  # Docker Desktop을 자동 실행한 뒤 엔진이 준비될 때까지 최대 대기 시간


def find_docker_desktop_exe() -> Path | None:
    """설치된 Docker Desktop 실행 파일을 흔한 설치 경로에서 탐색한다."""
    candidates = [
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Docker" / "Docker" / "Docker Desktop.exe",
        Path(os.environ.get("ProgramFiles(X86)", r"C:\Program Files (x86)")) / "Docker" / "Docker" / "Docker Desktop.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Docker" / "Docker Desktop.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def detect_lan_ip() -> str:
    """이 컴퓨터(서버)의 LAN IP를 감지한다. 실제로 패킷을 보내지는 않는다."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"


def is_url_healthy(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            return 200 <= response.status < 400
    except Exception:
        return False


class LauncherApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.lan_ip = detect_lan_ip()
        self.log_queue: queue.Queue[str] = queue.Queue()
        self.streamlit_process: subprocess.Popen | None = None
        self.service_running = [False] * len(SERVICES)  # 서비스별 실행 상태
        self.busy = False  # 시작/종료 작업 중 중복 클릭 방지 (전체 공용 락)

        root.title("AI Agent 품질관리 운영플랫폼 런처")
        root.geometry("860x620")
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        header = tk.Frame(root, padx=12, pady=10)
        header.pack(fill="x")
        tk.Label(header, text="AI Agent 품질관리 운영플랫폼", font=("Malgun Gothic", 14, "bold")).pack(anchor="w")
        tk.Label(header, text=f"서버 IP (동료 공유용): {self.lan_ip}", font=("Malgun Gothic", 10), fg="#555").pack(anchor="w")

        controls = tk.Frame(root, padx=12)
        controls.pack(fill="x")
        self.start_button = tk.Button(
            controls, text="▶ 전체 시작", width=16, font=("Malgun Gothic", 10, "bold"),
            bg="#188a4c", fg="white", command=self.start_services,
        )
        self.start_button.pack(side="left", padx=(0, 8), pady=4)
        self.stop_button = tk.Button(
            controls, text="⏹ 전체 종료", width=16, font=("Malgun Gothic", 10, "bold"),
            bg="#c0392b", fg="white", state="disabled", command=self.stop_services,
        )
        self.stop_button.pack(side="left", pady=4)

        links = tk.LabelFrame(root, text="서비스 개별 제어 (동료는 아래 주소로 접속)", padx=10, pady=8)
        links.pack(fill="x", padx=12, pady=8)

        # ---- Docker 엔진: 시작만 지원 (전체 종료는 다른 프로젝트 컨테이너에도 영향 줄 수 있어 위험해서 제외) ----
        docker_row = tk.Frame(links)
        docker_row.pack(fill="x", pady=(0, 6))
        tk.Label(docker_row, text="🐳 Docker 엔진", width=20, anchor="w", font=("Malgun Gothic", 9, "bold")).pack(side="left")
        self.docker_start_button = tk.Button(
            docker_row, text="▶ 시작", width=7, bg="#188a4c", fg="white",
            command=self.start_docker_engine_only,
        )
        self.docker_start_button.pack(side="left", padx=(4, 2))
        tk.Label(docker_row, text="(종료는 다른 프로젝트에도 영향 줄 수 있어 생략함)", fg="#888", font=("Malgun Gothic", 8)).pack(side="left", padx=(2, 8))
        self.docker_status_label = tk.Label(docker_row, text="⚪ 미확인", width=10, anchor="w", fg="#888")
        self.docker_status_label.pack(side="left")
        tk.Frame(links, height=1, bg="#d0d5dd").pack(fill="x", pady=4)

        # ---- 서비스별 시작/종료/열기 ----
        self.svc_start_buttons: list[tk.Button] = []
        self.svc_stop_buttons: list[tk.Button] = []
        self.open_buttons: list[tk.Button] = []
        self.status_labels: list[tk.Label] = []
        for index, (name, _compose_service, port, open_path, _health_path) in enumerate(SERVICES):
            row = tk.Frame(links)
            row.pack(fill="x", pady=3)

            tk.Label(row, text=name, width=20, anchor="w", font=("Malgun Gothic", 9, "bold")).pack(side="left")

            start_btn = tk.Button(
                row, text="▶ 시작", width=7, bg="#188a4c", fg="white",
                command=lambda i=index: self.start_one_service(i),
            )
            start_btn.pack(side="left", padx=(4, 2))
            self.svc_start_buttons.append(start_btn)

            stop_btn = tk.Button(
                row, text="⏹ 종료", width=7, bg="#c0392b", fg="white", state="disabled",
                command=lambda i=index: self.stop_one_service(i),
            )
            stop_btn.pack(side="left", padx=(0, 8))
            self.svc_stop_buttons.append(stop_btn)

            status_label = tk.Label(row, text="⚪ 꺼짐", width=10, anchor="w", fg="#888")
            status_label.pack(side="left", padx=(0, 6))
            self.status_labels.append(status_label)

            url = f"http://{self.lan_ip}:{port}{open_path}"
            open_button = tk.Button(
                row, text="🔗 열기", width=8, state="disabled",
                command=lambda u=url: webbrowser.open(u),
            )
            open_button.pack(side="left")
            self.open_buttons.append(open_button)

            entry = tk.Entry(row, font=("Consolas", 9), fg="#2563eb", relief="flat")
            entry.insert(0, url)
            entry.configure(state="readonly")  # 읽기 전용이지만 복사는 가능
            entry.pack(side="left", fill="x", expand=True, padx=(8, 0))

        self.log_widget = scrolledtext.ScrolledText(
            root, font=("Consolas", 9), bg="#0b1220", fg="#d8e0ee",
            insertbackground="#d8e0ee", state="disabled", height=14,
        )
        self.log_widget.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.log("런처 준비 완료. '▶ 전체 시작' 또는 서비스별 '▶ 시작' 버튼을 눌러 기동하세요.")
        self.log(f"프로젝트 경로: {PROJECT_ROOT}")
        self.root.after(100, self._drain_log_queue)
        self.root.after(300, self._check_docker_status_on_startup)

    # ------------------------------------------------------------------ 로그
    def log(self, message: str) -> None:
        self.log_queue.put(f"[{datetime.now():%H:%M:%S}] {message}")

    def _drain_log_queue(self) -> None:
        try:
            while True:
                line = self.log_queue.get_nowait()
                self.log_widget.configure(state="normal")
                self.log_widget.insert("end", line + "\n")
                self.log_widget.see("end")
                self.log_widget.configure(state="disabled")
        except queue.Empty:
            pass
        self.root.after(100, self._drain_log_queue)

    def _stream_output(self, process: subprocess.Popen, prefix: str) -> None:
        for raw in iter(process.stdout.readline, b""):
            text = raw.decode("utf-8", errors="replace").rstrip()
            if text:
                self.log(f"{prefix} {text}")

    def _run_and_log(self, command: list[str], prefix: str) -> int:
        process = subprocess.Popen(
            command, cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        self._stream_output(process, prefix)
        return process.wait()

    def _is_docker_engine_ready(self) -> bool:
        check = subprocess.run(
            ["docker", "info"], capture_output=True, cwd=PROJECT_ROOT,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        return check.returncode == 0

    def _set_docker_status_label(self, running: bool) -> None:
        self.docker_status_label.configure(
            text="🟢 실행 중" if running else "🔴 꺼짐",
            fg="#188a4c" if running else "#c0392b",
        )

    def _ensure_docker_running(self) -> bool:
        """Docker 엔진이 켜져 있으면 그대로 진행하고, 꺼져 있으면 Docker Desktop을 자동 실행 후 준비될 때까지 대기한다.
        이 함수가 모든 docker 관련 시작 경로(전체 시작/개별 서비스 시작/Docker 시작 버튼)의 공통 진입점이므로,
        여기서 상태 라벨을 갱신해두면 어느 경로로 Docker가 켜지든 "🐳 Docker 엔진" 표시가 항상 최신으로 맞는다."""
        self.log("Docker 엔진 확인 중...")
        if self._is_docker_engine_ready():
            self.log("✅ Docker 엔진이 이미 실행 중입니다.")
            self.root.after(0, lambda: self._set_docker_status_label(True))
            return True

        docker_desktop_exe = find_docker_desktop_exe()
        if docker_desktop_exe is None:
            self.log("❌ Docker 엔진이 꺼져 있고, Docker Desktop 실행 파일을 찾지 못했습니다. Docker Desktop을 직접 실행하세요.")
            self.root.after(0, lambda: self._set_docker_status_label(False))
            return False

        self.log("Docker 엔진이 꺼져 있습니다. Docker Desktop을 자동으로 실행합니다...")
        try:
            subprocess.Popen([str(docker_desktop_exe)], creationflags=subprocess.CREATE_NO_WINDOW)
        except OSError as exc:
            self.log(f"❌ Docker Desktop 실행 실패: {exc}")
            self.root.after(0, lambda: self._set_docker_status_label(False))
            return False

        self.log(f"Docker 엔진 준비 대기 중... (최대 {DOCKER_START_TIMEOUT_SECONDS}초)")
        deadline = datetime.now().timestamp() + DOCKER_START_TIMEOUT_SECONDS
        while datetime.now().timestamp() < deadline:
            if self._is_docker_engine_ready():
                self.log("✅ Docker 엔진 준비 완료.")
                self.root.after(0, lambda: self._set_docker_status_label(True))
                return True
            threading.Event().wait(3)

        self.log(f"❌ Docker 엔진이 {DOCKER_START_TIMEOUT_SECONDS}초 안에 준비되지 않았습니다. Docker Desktop 상태를 확인하세요.")
        self.root.after(0, lambda: self._set_docker_status_label(False))
        return False

    def _check_docker_status_on_startup(self) -> None:
        """런처를 켰을 때, 버튼을 누르지 않아도 Docker 상태를 한 번 확인해 '⚪ 미확인' 상태로 남지 않게 한다."""
        def worker() -> None:
            running = self._is_docker_engine_ready()
            self.root.after(0, lambda: self._set_docker_status_label(running))
        threading.Thread(target=worker, daemon=True).start()

    # ------------------------------------------------------------ 개별 서비스 시작/종료 도우미
    def _start_docker_service(self, service_name: str) -> bool:
        self.log(f"docker compose 기동 중... ({service_name})")
        if self._run_and_log(["docker", "compose", "up", "-d", service_name], "[docker]") != 0:
            self.log(f"❌ {service_name} 기동 실패. 위 로그를 확인하세요.")
            return False
        return True

    def _stop_docker_service(self, service_name: str) -> None:
        self.log(f"docker compose 종료 중... ({service_name})")
        self._run_and_log(["docker", "compose", "stop", service_name], "[docker]")

    def _start_streamlit(self) -> bool:
        if self.streamlit_process and self.streamlit_process.poll() is None:
            return True  # 이미 실행 중
        self.log("Streamlit 대시보드 기동 중...")
        streamlit_env = os.environ.copy()
        # 대시보드의 Grafana 탭(iframe)이 이 컴퓨터의 실제 LAN IP를 가리키도록 지정한다.
        # (localhost로 두면 동료가 LAN IP로 접속했을 때 동료 자신의 컴퓨터를 가리키게 되어 깨진다)
        streamlit_env["GRAFANA_BASE_URL"] = f"http://{self.lan_ip}:3000"
        self.streamlit_process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "dashboard/streamlit_app.py"],
            cwd=PROJECT_ROOT, env=streamlit_env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP,
        )
        threading.Thread(
            target=self._stream_output, args=(self.streamlit_process, "[streamlit]"), daemon=True,
        ).start()
        return True

    def _stop_streamlit(self) -> None:
        if self.streamlit_process and self.streamlit_process.poll() is None:
            self.log("Streamlit 대시보드 종료 중...")
            subprocess.run(
                ["taskkill", "/PID", str(self.streamlit_process.pid), "/T", "/F"],
                capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW,
            )
        self.streamlit_process = None

    # ------------------------------------------------------------ 버튼 상태 일괄 갱신
    def _update_service_display(self, index: int) -> None:
        """이 서비스의 상태 라벨/열기 버튼만 갱신한다. busy(작업 진행 중) 여부와 무관하게 항상 최신
        service_running 값을 반영해야, 전체 시작 중에도 서비스가 켜지는 순간 실시간으로 🟢 표시된다."""
        running = self.service_running[index]
        self.status_labels[index].configure(
            text="🟢 실행 중" if running else "⚪ 꺼짐",
            fg="#188a4c" if running else "#888",
        )
        self.open_buttons[index].configure(state="normal" if running else "disabled")

    def _refresh_all_controls_state(self) -> None:
        for i in range(len(SERVICES)):
            self._update_service_display(i)

        if self.busy:
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="disabled")
            self.docker_start_button.configure(state="disabled")
            for i in range(len(SERVICES)):
                self.svc_start_buttons[i].configure(state="disabled")
                self.svc_stop_buttons[i].configure(state="disabled")
            return

        any_running = any(self.service_running)
        self.start_button.configure(state="disabled" if all(self.service_running) else "normal")
        self.stop_button.configure(state="normal" if any_running else "disabled")
        self.docker_start_button.configure(state="normal")
        for i in range(len(SERVICES)):
            running = self.service_running[i]
            self.svc_start_buttons[i].configure(state="disabled" if running else "normal")
            self.svc_stop_buttons[i].configure(state="normal" if running else "disabled")

    # ------------------------------------------------------------ Docker 엔진만 시작
    def start_docker_engine_only(self) -> None:
        if self.busy:
            return
        self.busy = True
        self._refresh_all_controls_state()
        threading.Thread(target=self._start_docker_engine_only_worker, daemon=True).start()

    def _start_docker_engine_only_worker(self) -> None:
        try:
            self._ensure_docker_running()  # 상태 라벨 갱신은 _ensure_docker_running 내부에서 처리됨
        finally:
            self.busy = False
            self.root.after(0, self._refresh_all_controls_state)

    # ------------------------------------------------------------ 서비스 개별 시작
    def start_one_service(self, index: int) -> None:
        if self.busy:
            return
        self.busy = True
        self._refresh_all_controls_state()
        threading.Thread(target=self._start_one_service_worker, args=(index,), daemon=True).start()

    def _start_one_service_worker(self, index: int) -> None:
        name, compose_service, port, _open_path, health_path = SERVICES[index]
        try:
            if compose_service is None:
                if not self._start_streamlit():
                    return
            else:
                if not self._ensure_docker_running():
                    return
                if not self._start_docker_service(compose_service):
                    return

            self.log(f"{name} 준비 상태 확인 중...")
            deadline = datetime.now().timestamp() + HEALTH_TIMEOUT_SECONDS
            while datetime.now().timestamp() < deadline:
                if is_url_healthy(f"http://localhost:{port}{health_path}"):
                    self.service_running[index] = True
                    self.log(f"✅ {name} 준비 완료")
                    return
                threading.Event().wait(2)
            self.log(f"⚠️ {name} 이(가) {HEALTH_TIMEOUT_SECONDS}초 안에 준비되지 않았습니다.")
        finally:
            self.busy = False
            self.root.after(0, self._refresh_all_controls_state)

    # ------------------------------------------------------------ 서비스 개별 종료
    def stop_one_service(self, index: int) -> None:
        if self.busy:
            return
        self.busy = True
        self._refresh_all_controls_state()
        threading.Thread(target=self._stop_one_service_worker, args=(index,), daemon=True).start()

    def _stop_one_service_worker(self, index: int) -> None:
        name, compose_service, _port, _open_path, _health_path = SERVICES[index]
        try:
            if compose_service is None:
                self._stop_streamlit()
            else:
                self._stop_docker_service(compose_service)
            self.service_running[index] = False
            self.log(f"⏹ {name} 종료 완료")
        finally:
            self.busy = False
            self.root.after(0, self._refresh_all_controls_state)

    # ------------------------------------------------------------ 전체 서비스 시작
    def start_services(self) -> None:
        if self.busy:
            return
        self.busy = True
        self._refresh_all_controls_state()
        threading.Thread(target=self._start_services_worker, daemon=True).start()

    def _start_services_worker(self) -> None:
        try:
            if not self._ensure_docker_running():
                return

            self.log("docker compose 기동 중... (app / prometheus / grafana)")
            if self._run_and_log(["docker", "compose", "up", "-d"], "[docker]") != 0:
                self.log("❌ docker compose 기동 실패. 위 로그를 확인하세요.")
                return

            self._start_streamlit()

            self.log("서비스 준비 상태 확인 중... (준비되는 대로 표시가 바뀝니다)")
            pending = {i for i in range(len(SERVICES))}
            deadline = datetime.now().timestamp() + HEALTH_TIMEOUT_SECONDS
            while pending and datetime.now().timestamp() < deadline:
                for index in sorted(pending):
                    name, _compose_service, port, _open_path, health_path = SERVICES[index]
                    if is_url_healthy(f"http://localhost:{port}{health_path}"):
                        pending.discard(index)
                        self.service_running[index] = True
                        self.log(f"✅ {name} 준비 완료")
                        self.root.after(0, self._refresh_all_controls_state)
                if pending:
                    threading.Event().wait(2)

            if pending:
                for index in pending:
                    self.log(f"⚠️ {SERVICES[index][0]} 이(가) {HEALTH_TIMEOUT_SECONDS}초 안에 준비되지 않았습니다.")
            self.log("서비스 기동 완료. 동료에게 위 주소를 공유하세요.")
        finally:
            self.busy = False
            self.root.after(0, self._refresh_all_controls_state)

    # ------------------------------------------------------------ 전체 서비스 종료
    def stop_services(self, on_done=None) -> None:
        if self.busy:
            return
        self.busy = True
        self._refresh_all_controls_state()
        threading.Thread(target=self._stop_services_worker, args=(on_done,), daemon=True).start()

    def _stop_services_worker(self, on_done) -> None:
        try:
            self._stop_streamlit()

            self.log("docker compose 종료 중...")
            self._run_and_log(["docker", "compose", "down"], "[docker]")

            self.service_running = [False] * len(SERVICES)
            self.log("⏹ 모든 서비스가 종료되었습니다. 다시 시작하려면 '▶ 전체 시작'을 누르세요.")
        finally:
            self.busy = False
            self.root.after(0, self._refresh_all_controls_state)
            if on_done:
                self.root.after(0, on_done)

    # ------------------------------------------------------------ 창 닫기(X)
    def on_close(self) -> None:
        if not any(self.service_running):
            self.root.destroy()
            return
        self.log("창을 닫습니다 — 실행 중인 서비스를 먼저 종료합니다...")
        self.stop_services(on_done=self.root.destroy)


def main() -> None:
    root = tk.Tk()
    LauncherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
