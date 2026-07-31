"""AI Agent 품질관리 운영플랫폼 접속 클라이언트 (배포용).

동료(클라이언트) 컴퓨터에서 실행한다. 서비스 시작/종료 기능은 없고,
서버에서 이미 기동 중인 서비스에 버튼으로 접속만 한다.
- 상단: 서버 IP 입력 (마지막 값은 client_config.json에 저장되어 다음 실행 때 유지)
- 서버 상태 ON/OFF 표시 + 서비스별 상태 점(●) — 5초마다 자동 확인
- 하단: 상태 확인 진행 상황 로그
파이썬 표준 라이브러리(tkinter)만 사용한다.
"""
import json
import queue
import threading
import urllib.request
import webbrowser
from datetime import datetime
from pathlib import Path

import tkinter as tk
from tkinter import scrolledtext

CONFIG_PATH = Path(__file__).resolve().parent / "client_config.json"
DEFAULT_SERVER_IP = "192.168.0.22"
POLL_INTERVAL_MS = 5000  # 자동 상태 확인 주기 (5초)

# (표시 이름, 포트, 브라우저로 열 경로, 헬스체크 경로)
SERVICES = [
    ("🤖 챗봇 API (Swagger)", 8000, "/docs", "/health"),
    ("📊 Streamlit 대시보드", 8501, "", "/"),
    ("📈 Prometheus", 9090, "", "/-/ready"),
    ("📉 Grafana", 3000, "", "/api/health"),
]

STATUS_ON = ("● ON", "#188a4c")
STATUS_OFF = ("● OFF", "#c0392b")
STATUS_CHECKING = ("● 확인 중...", "#c07a12")


def load_saved_ip() -> str:
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8")).get("server_ip", DEFAULT_SERVER_IP)
    except (OSError, json.JSONDecodeError):
        return DEFAULT_SERVER_IP


def save_ip(server_ip: str) -> None:
    try:
        CONFIG_PATH.write_text(json.dumps({"server_ip": server_ip}, indent=2), encoding="utf-8")
    except OSError:
        pass  # 저장 실패해도 접속 기능에는 지장 없음


def is_url_healthy(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            return 200 <= response.status < 400
    except Exception:
        return False


class ClientApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.log_queue: queue.Queue[str] = queue.Queue()
        self.checking = False
        self.last_states: list[bool | None] = [None] * len(SERVICES)  # 상태 변화 때만 로그를 남기기 위한 기억

        root.title("AI Agent 품질관리 운영플랫폼 접속 클라이언트")
        root.geometry("680x520")

        header = tk.Frame(root, padx=12, pady=10)
        header.pack(fill="x")
        tk.Label(header, text="AI Agent 품질관리 운영플랫폼 — 접속 클라이언트",
                 font=("Malgun Gothic", 14, "bold")).pack(anchor="w")

        # ---- 서버 IP 입력 + 서버 상태 ----
        server_row = tk.Frame(root, padx=12)
        server_row.pack(fill="x")
        tk.Label(server_row, text="서버 IP:", font=("Malgun Gothic", 10)).pack(side="left")
        self.ip_var = tk.StringVar(value=load_saved_ip())
        self.ip_entry = tk.Entry(server_row, textvariable=self.ip_var, font=("Consolas", 11), width=18)
        self.ip_entry.pack(side="left", padx=(6, 8))
        tk.Button(server_row, text="적용/새로고침", command=self.apply_ip).pack(side="left")

        tk.Label(server_row, text="서버 상태:", font=("Malgun Gothic", 10)).pack(side="left", padx=(18, 4))
        self.server_status_label = tk.Label(server_row, text=STATUS_CHECKING[0],
                                            font=("Malgun Gothic", 11, "bold"), fg=STATUS_CHECKING[1])
        self.server_status_label.pack(side="left")

        # ---- 서비스 버튼 + 서비스별 상태 점 ----
        links = tk.LabelFrame(root, text="서비스 바로가기", padx=10, pady=8)
        links.pack(fill="x", padx=12, pady=8)
        self.status_dots: list[tk.Label] = []
        self.url_entries: list[tk.Entry] = []
        for name, _, _, _ in SERVICES:
            row = tk.Frame(links)
            row.pack(fill="x", pady=2)
            dot = tk.Label(row, text="●", font=("Malgun Gothic", 11), fg="#9aa4b2")
            dot.pack(side="left", padx=(0, 4))
            self.status_dots.append(dot)
            index = len(self.status_dots) - 1
            tk.Button(row, text=name, width=24, anchor="w",
                      command=lambda i=index: self.open_service(i)).pack(side="left")
            entry = tk.Entry(row, font=("Consolas", 9), fg="#2563eb", relief="flat")
            entry.configure(state="readonly")
            entry.pack(side="left", fill="x", expand=True, padx=(8, 0))
            self.url_entries.append(entry)

        # ---- 로그 패널 ----
        self.log_widget = scrolledtext.ScrolledText(
            root, font=("Consolas", 9), bg="#0b1220", fg="#d8e0ee",
            insertbackground="#d8e0ee", state="disabled", height=14,
        )
        self.log_widget.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.refresh_urls()
        self.log(f"클라이언트 준비 완료. 서버 IP: {self.ip_var.get()}")
        self.log("5초마다 서버 상태를 자동 확인합니다.")
        self.root.after(100, self._drain_log_queue)
        self.root.after(300, self.poll_status)

    # ------------------------------------------------------------------ 유틸
    def service_url(self, index: int) -> str:
        _, port, open_path, _ = SERVICES[index]
        return f"http://{self.ip_var.get().strip()}:{port}{open_path}"

    def health_url(self, index: int) -> str:
        _, port, _, health_path = SERVICES[index]
        return f"http://{self.ip_var.get().strip()}:{port}{health_path}"

    def refresh_urls(self) -> None:
        for index, entry in enumerate(self.url_entries):
            entry.configure(state="normal")
            entry.delete(0, "end")
            entry.insert(0, self.service_url(index))
            entry.configure(state="readonly")

    def open_service(self, index: int) -> None:
        url = self.service_url(index)
        self.log(f"브라우저로 열기: {url}")
        webbrowser.open(url)

    def apply_ip(self) -> None:
        server_ip = self.ip_var.get().strip()
        if not server_ip:
            self.log("⚠️ 서버 IP를 입력하세요.")
            return
        save_ip(server_ip)
        self.refresh_urls()
        self.last_states = [None] * len(SERVICES)  # IP가 바뀌었으니 상태를 처음부터 다시 로그
        self.log(f"서버 IP 적용: {server_ip} — 상태를 다시 확인합니다.")

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

    # ------------------------------------------------------------ 상태 확인
    def poll_status(self) -> None:
        if not self.checking:
            self.checking = True
            threading.Thread(target=self._check_status_worker, daemon=True).start()
        self.root.after(POLL_INTERVAL_MS, self.poll_status)

    def _check_status_worker(self) -> None:
        try:
            states = [is_url_healthy(self.health_url(i)) for i in range(len(SERVICES))]
            self.root.after(0, lambda: self._apply_states(states))
        finally:
            self.checking = False

    def _apply_states(self, states: list[bool]) -> None:
        for index, healthy in enumerate(states):
            self.status_dots[index].configure(fg="#188a4c" if healthy else "#c0392b")
            if self.last_states[index] is None or self.last_states[index] != healthy:
                name = SERVICES[index][0]
                self.log(f"{'✅' if healthy else '❌'} {name}: {'ON' if healthy else 'OFF'}")
            self.last_states[index] = healthy

        if all(states):
            text, color = STATUS_ON
        elif not any(states):
            text, color = STATUS_OFF
        else:
            on_count = sum(states)
            text, color = (f"● 일부 ON ({on_count}/{len(states)})", "#c07a12")
        self.server_status_label.configure(text=text, fg=color)


def main() -> None:
    root = tk.Tk()
    ClientApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
