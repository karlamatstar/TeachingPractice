import os
import sys
import shutil
import socket
import threading
import subprocess
import urllib.request
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import webbrowser

# 경로 처리 — 두 가지 실행 환경을 모두 지원한다:
#  1) 프로젝트 안에서 실행 (개발자/서버 컴퓨터): performance/ 폴더의 스크립트와 results/를 그대로 사용
#  2) exe 단독 배포 (동료 컴퓨터, 프로젝트 없음): exe에 번들된 스크립트 사용, 결과는 exe 옆 results/에 저장
# PyInstaller onefile exe에서는 __file__이 임시 압축해제 폴더(sys._MEIPASS)를 가리키므로 구분해서 처리한다.
if getattr(sys, 'frozen', False):
    _BASE_DIR = os.path.dirname(sys.executable)          # exe가 놓인 폴더
    _BUNDLE_DIR = os.path.join(sys._MEIPASS, 'performance')  # exe에 내장된 스크립트 사본
else:
    _BASE_DIR = os.path.dirname(__file__)
    _BUNDLE_DIR = None

PROJECT_ROOT = os.path.abspath(os.path.join(_BASE_DIR, '..'))
PERFORMANCE_DIR = os.path.join(PROJECT_ROOT, 'performance')

if os.path.isdir(PERFORMANCE_DIR):
    # 프로젝트 구조가 있으면 프로젝트 스크립트(수정 즉시 반영)와 기존 결과 폴더를 사용
    SCRIPTS_DIR = PERFORMANCE_DIR
    RESULTS_DIR = os.path.join(PROJECT_ROOT, '_OUTPUT', 'performance')
    STANDALONE_MODE = False
else:
    # 단독 배포 모드: 내장 스크립트 사용, 결과는 exe 옆에 저장
    SCRIPTS_DIR = _BUNDLE_DIR or PERFORMANCE_DIR
    RESULTS_DIR = os.path.join(PROJECT_ROOT, '_OUTPUT', 'performance')
    STANDALONE_MODE = True
LOG_DIR = os.path.join(RESULTS_DIR, 'k6_log')

# STANDALONE_MODE(동료 컴퓨터에 exe만 배포된 상태)에서는 "검증 테스트" 탭만 만들지 않는다.
# 이 탭은 pytest가 TestClient로 로컬 app.main을 직접 파이썬 코드로 임포트해서 실행하는 방식이라
# "원격 서버 IP를 대상으로 테스트"라는 개념 자체가 성립하지 않는 로컬(이 프로젝트 코드가 있는 컴퓨터) 전용
# 기능이다. 반면 "API 종합 성능 테스트"/"API 끊김 방어 테스트"는 원래 원격 IP를 대상으로 할 수 있는
# 로직이라, run_performance_tests.py/run_api_disconnect_test.py를 별도 프로세스(sys.executable)로 띄우는
# 대신 아래에서 이 모듈들을 직접 import해 인라인 함수 호출로 실행한다 (PyInstaller exe 안에서는
# sys.executable이 파이썬 인터프리터가 아니라 exe 자기 자신이라 subprocess로 스크립트를 못 띄우기 때문).
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# 개발 모드(python RUN/test_launcher.py)에서는 scripts/ 폴더가 실제로 있어야 아래 import가 되고,
# exe로 빌드할 때는 빌드 명령에 --paths로 같은 폴더를 넘겨줘서 모듈이 exe 안에 통째로 번들된다
# (번들된 exe 안에서는 이 경로가 실제로 없어도 상관없다 — import는 exe 내장 모듈로 해결됨).
_SCRIPTS_DIR_FOR_IMPORT = os.path.join(PROJECT_ROOT, 'scripts')
if os.path.isdir(_SCRIPTS_DIR_FOR_IMPORT) and _SCRIPTS_DIR_FOR_IMPORT not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR_FOR_IMPORT)

import run_performance_tests as perf_runner
import run_api_disconnect_test as disconnect_runner


def is_server_reachable(target_host: str, timeout: float = 3.0) -> bool:
    """타겟 서버의 /health 엔드포인트가 응답하는지 확인한다 (사전 점검용)."""
    try:
        with urllib.request.urlopen(f"http://{target_host}/health", timeout=timeout) as response:
            return 200 <= response.status < 400
    except Exception:
        return False


def find_k6() -> str | None:
    """k6 실행 파일을 찾는다: exe에 번들된 것 → exe 옆 k6.exe → 시스템 PATH 순."""
    if getattr(sys, 'frozen', False):
        bundled = os.path.join(sys._MEIPASS, 'k6.exe')
        if os.path.exists(bundled):
            return bundled
    side_by_side = os.path.join(_BASE_DIR, 'k6.exe')
    if os.path.exists(side_by_side):
        return side_by_side
    return shutil.which('k6')

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class K6Launcher:
    def __init__(self, root):
        self.root = root
        self.root.title("K6 Performance Test Launcher")
        self.root.geometry("800x700")
        
        self.process = None
        self.is_running = False

        self._build_ui()

    def _build_ui(self):
        # 상단 설정 영역
        header_frame = tk.Frame(self.root, padx=15, pady=10)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="AI Agent 성능 테스트 런처", font=("Malgun Gothic", 16, "bold")).pack(anchor="w", pady=(0, 10))
        
        ip_frame = tk.Frame(header_frame)
        ip_frame.pack(fill="x")
        tk.Label(ip_frame, text="타겟 서버 IP:", font=("Malgun Gothic", 10, "bold")).pack(side="left")
        
        self.ip_var = tk.StringVar(value="192.168.0.22:8000")
        self.ip_entry = tk.Entry(ip_frame, textvariable=self.ip_var, width=25, font=("Consolas", 11))
        self.ip_entry.pack(side="left", padx=10)
        
        self.status_label = tk.Label(ip_frame, text="🟢 대기 중", font=("Malgun Gothic", 11, "bold"), fg="green")
        self.status_label.pack(side="right")

        # 탭 영역
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=5)
        
        # 탭별 콘솔을 저장할 딕셔너리
        self.consoles = {}
        # toggle_ui_state에서 일괄 활성/비활성 처리할 탭 목록 (모드에 따라 실제로 만들어진 탭만 담김)
        self.all_tabs = []

        # 1. Smoke Tab
        self.smoke_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.smoke_tab, text=" Smoke Test ")
        self._build_tab(self.smoke_tab, "smoke_test", "smoke_test.js", "기본 연결 및 200 OK 상태를 빠르게 확인합니다. (VUs 고정 1)")
        self.all_tabs.append(self.smoke_tab)

        # 2. Load Tab
        self.load_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.load_tab, text=" Load Test ")
        self.load_vus = tk.StringVar(value="20")
        self.load_dur = tk.StringVar(value="60") # 초 단위
        self._build_tab(self.load_tab, "load_test", "load_test.js", "일상적인 부하 상황에서의 안정성을 검증합니다.", self.load_vus, self.load_dur)
        self.all_tabs.append(self.load_tab)

        # 2.5 Random Tab
        self.random_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.random_tab, text=" Random Test ")
        self.random_vus = tk.StringVar(value="100")
        self.random_dur = tk.StringVar(value="60") # 초 단위
        self._build_tab(self.random_tab, "random_test", "random_test.js", "매 초마다 무작위로 변동하는 트래픽(Chaos Load)을 시뮬레이션합니다.", self.random_vus, self.random_dur)
        self.all_tabs.append(self.random_tab)

        # 3. Stress Tab
        self.stress_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stress_tab, text=" Stress Test ")
        self.stress_vus = tk.StringVar(value="100")
        self.stress_dur = tk.StringVar(value="120") # 초 단위
        self._build_tab(self.stress_tab, "stress_test", "stress_test.js", "서버가 버틸 수 있는 한계점을 파악합니다. 서서히 유저가 증가합니다.", self.stress_vus, self.stress_dur)
        self.all_tabs.append(self.stress_tab)

        # 4. Spike Tab
        self.spike_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.spike_tab, text=" Spike Test ")
        self.spike_vus = tk.StringVar(value="200")
        self.spike_dur = tk.StringVar(value="60") # 초 단위
        self._build_tab(self.spike_tab, "spike_test", "spike_test.js", "순간적인 트래픽 폭주 시 시스템 복원력을 검증합니다.", self.spike_vus, self.spike_dur)
        self.all_tabs.append(self.spike_tab)

        if not STANDALONE_MODE:
            # 5. Validation Tab (Phase 2) — pytest가 TestClient로 로컬 app 모듈을 직접 임포트해서 도는
            # 방식이라 "원격 IP 대상 테스트"라는 개념 자체가 성립하지 않는 로컬 전용 기능. 배포용 exe에는 안 넣음.
            self.validation_tab = ttk.Frame(self.notebook)
            self.notebook.add(self.validation_tab, text=" 검증 테스트 ")
            self._build_validation_tab(self.validation_tab)
            self.all_tabs.append(self.validation_tab)
        else:
            # 배포용 exe: 검증 테스트 탭 대신 왜 없는지 안내만 표시
            info_tab = ttk.Frame(self.notebook)
            self.notebook.add(info_tab, text=" 안내 ")
            tk.Label(
                info_tab, justify="left", padx=15, pady=15, font=("Malgun Gothic", 9),
                text=(
                    "검증 테스트 탭은 서버 컴퓨터의 프로젝트 코드(pytest, app 모듈 등)를\n"
                    "직접 임포트해서 로컬로 실행하는 기능이라, 원격 IP를 대상으로 하는\n"
                    "이 배포용 프로그램에는 포함하지 않았습니다.\n\n"
                    "나머지 탭(Smoke / Load / Stress / Spike / API 종합 성능 테스트 /\n"
                    "API 끊김 방어 테스트)은 입력한 서버 IP를 대상으로 이 컴퓨터에서\n"
                    "바로 실행할 수 있습니다."
                ),
            ).pack(anchor="w")
            self.all_tabs.append(info_tab)

        # 6. API Performance Tab (Phase 3) — 원격 IP를 대상으로 할 수 있어 두 모드 모두에서 생성
        self.api_perf_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.api_perf_tab, text=" API 종합 성능 테스트 ")
        self._build_api_perf_tab(self.api_perf_tab)
        self.all_tabs.append(self.api_perf_tab)

        # 7. API Disconnect Test Tab — 원격 IP를 대상으로 할 수 있어 두 모드 모두에서 생성
        self.api_disconnect_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.api_disconnect_tab, text=" API 끊김 방어 테스트 ")
        self._build_api_disconnect_tab(self.api_disconnect_tab)
        self.all_tabs.append(self.api_disconnect_tab)

    def _build_tab(self, parent, test_type, script_name, desc, vus_var=None, dur_var=None):
        frame = tk.Frame(parent, padx=15, pady=15)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text=desc, font=("Malgun Gothic", 9)).pack(anchor="w", pady=(0, 10))
        
        input_frame = tk.Frame(frame)
        input_frame.pack(fill="x", pady=(0, 15))
        
        if vus_var:
            tk.Label(input_frame, text="Max VUs (가상 유저):").pack(side="left")
            tk.Entry(input_frame, textvariable=vus_var, width=10).pack(side="left", padx=5)
            
        if dur_var:
            tk.Label(input_frame, text="총 시간 (초):").pack(side="left", padx=(15, 0))
            tk.Entry(input_frame, textvariable=dur_var, width=10).pack(side="left", padx=5)
            
        btn = tk.Button(frame, text="▶ 테스트 시작", bg="#2563eb", fg="white", font=("Malgun Gothic", 10, "bold"),
                        command=lambda: self.start_test(test_type, script_name, vus_var, dur_var))
        btn.pack(anchor="w", pady=(0, 15))

        # 탭별 독립적인 콘솔창
        tk.Label(frame, text="실시간 로그 출력", font=("Malgun Gothic", 9, "bold")).pack(anchor="w")
        console = scrolledtext.ScrolledText(frame, bg="black", fg="#00FF00", font=("Consolas", 10))
        console.pack(fill="both", expand=True, pady=5)
        self.consoles[test_type] = console

    def toggle_ui_state(self, state):
        state_str = "normal" if state else "disabled"
        self.ip_entry.config(state=state_str)
        for tab in self.all_tabs:
            for child in tab.winfo_children():
                for sub in child.winfo_children():
                    if isinstance(sub, (tk.Entry, tk.Button)):
                        if hasattr(self, 'report_btn') and sub == self.report_btn and state:
                            continue # Leave report button alone on toggle, wait, it gets enabled specially
                        if hasattr(self, 'perf_report_btn') and sub == self.perf_report_btn and state:
                            continue
                        sub.config(state=state_str)
                if isinstance(child, (tk.Entry, tk.Button)):
                    child.config(state=state_str)

    def append_console(self, test_type, text):
        console = self.consoles[test_type]
        console.insert(tk.END, text)
        console.see(tk.END)

    def read_output(self, process, test_type):
        for line in iter(process.stdout.readline, b''):
            decoded_line = line.decode('utf-8', errors='replace')
            self.root.after(0, self.append_console, test_type, decoded_line)
            
        process.stdout.close()
        process.wait()
        
        self.root.after(0, self.on_test_finished, test_type)

    def start_test(self, test_type, script_name, vus_var, dur_var):
        if self.is_running: return
        
        self.is_running = True
        self.toggle_ui_state(False)
        self.consoles[test_type].delete(1.0, tk.END)
        
        self.status_label.config(text=f"🟠 {test_type.upper()} 진행 중...", fg="#f59e0b")
        
        k6_bin = find_k6()
        if not k6_bin:
            self.append_console(test_type, "[오류] k6 실행 파일을 찾을 수 없습니다.\n")
            self.append_console(test_type, "k6.exe를 이 프로그램과 같은 폴더에 두거나, https://k6.io 에서 설치하세요.\n")
            self.on_test_finished(test_type)
            return

        script_path = os.path.join(SCRIPTS_DIR, script_name)
        result_file = os.path.join(RESULTS_DIR, f"{test_type}_result.json")

        # Prometheus 지표 전송 주소는 타겟 서버 IP에서 유도한다 — 다른 컴퓨터에서 실행해도
        # 지표가 서버(타겟) 쪽 Prometheus/Grafana로 모이도록 (localhost 하드코딩 금지).
        # 주의: k6는 "--out experimental-prometheus-rw=URL"의 인라인 URL을 무시하고 기본값
        # (localhost:9090)을 쓴다. 반드시 K6_PROMETHEUS_RW_SERVER_URL 환경변수로 지정해야 한다.
        target_host = self.ip_var.get().strip().split(":")[0] or "localhost"

        # 실행자마다/실행마다 고유한 testid 태그를 붙여 Prometheus 시리즈를 분리한다.
        # 태그가 없으면 여러 컴퓨터에서 동시에 테스트할 때 전원이 같은 시리즈(k6_vus 등)에 쓰게 되어
        # "out of order sample" 400 에러로 서로의 지표를 밀어내는 충돌이 발생한다.
        run_id = f"{socket.gethostname()}_{datetime.now().strftime('%H%M%S')}"

        cmd = [
            k6_bin, "run",
            "--out", "experimental-prometheus-rw",
            "--tag", f"testid={run_id}",
            f"--summary-export={result_file}",
            script_path
        ]

        env = os.environ.copy()
        env["K6_PROMETHEUS_RW_SERVER_URL"] = f"http://{target_host}:9090/api/v1/write"
        # k6 지연시간 트렌드 지표를 p95 기준으로 remote-write 하도록 명시 지정
        # (기본값에 의존하지 않고 Grafana K6 대시보드의 p95 패널이 항상 존재하도록 보장)
        env["K6_PROMETHEUS_RW_TREND_STATS"] = "p(95)"
        env["TARGET_IP"] = self.ip_var.get()
        if vus_var: env["K6_VUS"] = vus_var.get()
        if dur_var: env["SCRIPT_DURATION"] = dur_var.get() # K6 예약어(K6_DURATION)와 충돌 방지를 위해 이름 변경

        self.append_console(test_type, f"🚀 테스트 시작: {script_name}\n")
        self.append_console(test_type, f"💻 타겟 서버: {env['TARGET_IP']}\n")
        self.append_console(test_type, f"📈 지표 전송: http://{target_host}:9090 (Grafana K6 대시보드)\n")
        self.append_console(test_type, "-" * 60 + "\n")

        try:
            creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            self.process = subprocess.Popen(
                cmd, env=env,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                creationflags=creationflags,
            )
            
            thread = threading.Thread(target=self.read_output, args=(self.process, test_type))
            thread.daemon = True
            thread.start()
        except Exception as e:
            self.append_console(test_type, f"\n[오류] K6 실행 실패: {e}\n")
            self.on_test_finished(test_type)

    def on_test_finished(self, test_type):
        self.is_running = False
        self.toggle_ui_state(True)
        self.status_label.config(text="🟢 대기 중", fg="green")
        self.append_console(test_type, "\n✅ 테스트가 종료되었습니다.\n")
        
        latest_file = os.path.join(RESULTS_DIR, f"{test_type}_result.json")
        if os.path.exists(latest_file):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"{timestamp}_{test_type}_result.json"
            log_file_path = os.path.join(LOG_DIR, log_filename)
            shutil.copy2(latest_file, log_file_path)
            self.append_console(test_type, f"📁 결과 저장 완료: {log_filename}\n")

    def _build_validation_tab(self, parent):
        frame = tk.Frame(parent, padx=15, pady=15)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text="장애 유발(Chaos) + 기능(Pytest) 자동화 파이프라인", font=("Malgun Gothic", 9)).pack(anchor="w", pady=(0, 10))
        
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", pady=(0, 15))
        
        btn = tk.Button(btn_frame, text="▶ QA 자동화 시작", bg="#2563eb", fg="white", font=("Malgun Gothic", 10, "bold"),
                        command=self.start_validation_test)
        btn.pack(side="left")

        self.report_btn = tk.Button(btn_frame, text="결함 보고서 확인", bg="#10b981", fg="white", font=("Malgun Gothic", 10, "bold"),
                        command=lambda: webbrowser.open(f"http://{self.ip_var.get().strip().split(':')[0]}:8000/reports/defects/chaos/defect_report.md"), state="disabled")
        self.report_btn.pack(side="left", padx=15)

        tk.Label(frame, text="실시간 로그 출력", font=("Malgun Gothic", 9, "bold")).pack(anchor="w")
        console = scrolledtext.ScrolledText(frame, bg="black", fg="#00FF00", font=("Consolas", 10))
        console.pack(fill="both", expand=True, pady=5)
        self.consoles["validation_test"] = console

    def start_validation_test(self):
        if self.is_running: return
        
        test_type = "validation_test"
        self.is_running = True
        self.toggle_ui_state(False)
        self.consoles[test_type].delete(1.0, tk.END)
        self.report_btn.config(state="disabled")
        
        self.status_label.config(text=f"🟠 통합 검증 진행 중...", fg="#f59e0b")
        
        script_path = os.path.join(PROJECT_ROOT, "scripts", "run_validation_tests.py")
        cmd = [sys.executable, "-u", script_path]
        
        env = os.environ.copy()
        
        try:
            creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            self.process = subprocess.Popen(
                cmd, env=env,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                creationflags=creationflags,
            )
            
            thread = threading.Thread(target=self.read_output_validation, args=(self.process, test_type))
            thread.daemon = True
            thread.start()
        except Exception as e:
            self.append_console(test_type, f"\n[오류] 검증 스크립트 실행 실패: {e}\n")
            self.on_validation_finished()
            
    def read_output_validation(self, process, test_type):
        for line in iter(process.stdout.readline, b''):
            decoded_line = line.decode('utf-8', errors='replace')
            self.root.after(0, self.append_console, test_type, decoded_line)
            
        process.stdout.close()
        process.wait()
        
        self.root.after(0, self.on_validation_finished)
        
    def on_validation_finished(self):
        self.is_running = False
        self.toggle_ui_state(True)
        self.status_label.config(text="🟢 대기 중", fg="green")
        self.report_btn.config(state="normal")
        self.append_console("validation_test", "\n✅ QA 자동화 파이프라인 종료.\n")

    def _build_api_perf_tab(self, parent):
        frame = tk.Frame(parent, padx=15, pady=15)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text="LLM API 계단식 부하(1➔10➔25 VUs) 성능 및 신뢰성 검증", font=("Malgun Gothic", 9)).pack(anchor="w", pady=(0, 10))
        
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", pady=(0, 15))
        
        btn = tk.Button(btn_frame, text="▶ 테스트 진행", bg="#dc2626", fg="white", font=("Malgun Gothic", 10, "bold"),
                        command=self.start_api_perf_test)
        btn.pack(side="left")

        self.perf_report_btn = tk.Button(btn_frame, text="성능 보고서 확인", bg="#10b981", fg="white", font=("Malgun Gothic", 10, "bold"),
                        command=self.open_perf_report, state="disabled")
        self.perf_report_btn.pack(side="left", padx=15)

        tk.Label(frame, text="실시간 로그 출력", font=("Malgun Gothic", 9, "bold")).pack(anchor="w")
        console = scrolledtext.ScrolledText(frame, bg="black", fg="#00FF00", font=("Consolas", 10))
        console.pack(fill="both", expand=True, pady=5)
        self.consoles["api_perf_test"] = console

    def start_api_perf_test(self):
        if self.is_running: return

        if not messagebox.askyesno("⚠️ 과금 발생 경고", "실제 API를 호출하기 때문에 토큰 사용에 따른 요금(비용)이 발생할 수 있습니다.\n정말로 테스트를 진행하시겠습니까?"):
            return

        test_type = "api_perf_test"
        self.is_running = True
        self.toggle_ui_state(False)
        self.consoles[test_type].delete(1.0, tk.END)
        self.perf_report_btn.config(state="disabled")

        self.status_label.config(text="🟠 종합 성능 분석 중...", fg="#f59e0b")

        k6_bin = find_k6()
        if not k6_bin:
            self.append_console(test_type, "[오류] k6 실행 파일을 찾을 수 없습니다.\n")
            self.on_api_perf_finished()
            return

        target_host = self.ip_var.get().strip()
        script_path = os.path.join(SCRIPTS_DIR, "api_latency_test.js")

        thread = threading.Thread(
            target=self._run_api_perf_worker, args=(k6_bin, script_path, target_host), daemon=True,
        )
        thread.start()

    def _run_api_perf_worker(self, k6_bin, script_path, target_host):
        test_type = "api_perf_test"

        def on_line(text):
            self.root.after(0, self.append_console, test_type, text)

        try:
            on_line(f"💻 타겟 서버: {target_host}\n")
            on_line("서버 연결 확인 중...\n")
            if not is_server_reachable(target_host):
                on_line(
                    f"\n❌ 대상 서버({target_host})에 연결할 수 없습니다. "
                    "서버가 켜져 있는지, IP/포트가 맞는지, 방화벽이 막고 있지 않은지 확인 후 다시 시도하세요.\n"
                )
                return
            on_line("✅ 서버 연결 확인됨.\n")
            on_line("-" * 60 + "\n")
            raw_json = perf_runner.run_k6_performance(k6_bin, script_path, target_host, RESULTS_DIR, on_line=on_line)
            report_path = perf_runner.parse_and_generate_report(raw_json, RESULTS_DIR, on_line=on_line)
            if report_path:
                self.last_perf_report_path = str(report_path)
        except Exception as e:
            on_line(f"\n[오류] 성능 테스트 실행 실패: {e}\n")
        finally:
            self.root.after(0, self.on_api_perf_finished)

    def on_api_perf_finished(self):
        self.is_running = False
        self.toggle_ui_state(True)
        self.status_label.config(text="🟢 대기 중", fg="green")
        if getattr(self, 'last_perf_report_path', None):
            self.perf_report_btn.config(state="normal")
        self.append_console("api_perf_test", "\n✅ 종합 성능 분석 파이프라인 종료.\n")

    def open_perf_report(self):
        report_path = getattr(self, 'last_perf_report_path', None)
        if report_path and os.path.exists(report_path):
            webbrowser.open(f"file:///{report_path.replace(os.sep, '/')}")
        else:
            messagebox.showinfo("알림", "아직 생성된 리포트가 없습니다.")

    def _build_api_disconnect_tab(self, parent):
        frame = tk.Frame(parent, padx=15, pady=15)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text="의도적인 API 서버 503 통신 장애 유발 및 Fallback 방어 검증", font=("Malgun Gothic", 9)).pack(anchor="w", pady=(0, 10))
        
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", pady=(0, 15))
        
        btn = tk.Button(btn_frame, text="▶ 테스트 진행", bg="#8b5cf6", fg="white", font=("Malgun Gothic", 10, "bold"),
                        command=self.start_api_disconnect_test)
        btn.pack(side="left")

        tk.Label(frame, text="실시간 로그 출력", font=("Malgun Gothic", 9, "bold")).pack(anchor="w")
        console = scrolledtext.ScrolledText(frame, bg="black", fg="#00FF00", font=("Consolas", 10))
        console.pack(fill="both", expand=True, pady=5)
        self.consoles["api_disconnect_test"] = console

    def start_api_disconnect_test(self):
        if self.is_running: return

        test_type = "api_disconnect_test"
        self.is_running = True
        self.toggle_ui_state(False)
        self.consoles[test_type].delete(1.0, tk.END)

        self.status_label.config(text="🟠 API 끊김 방어 검증 중...", fg="#f59e0b")

        target_host = self.ip_var.get().strip()

        thread = threading.Thread(target=self._run_api_disconnect_worker, args=(target_host,), daemon=True)
        thread.start()

    def _run_api_disconnect_worker(self, target_host):
        test_type = "api_disconnect_test"

        def on_line(text):
            self.root.after(0, self.append_console, test_type, text)

        try:
            on_line(f"💻 타겟 서버: {target_host}\n")
            on_line("서버 연결 확인 중...\n")
            if not is_server_reachable(target_host):
                on_line(
                    f"\n❌ 대상 서버({target_host})에 연결할 수 없습니다. "
                    "서버가 켜져 있는지, IP/포트가 맞는지, 방화벽이 막고 있지 않은지 확인 후 다시 시도하세요.\n"
                )
                return
            on_line("✅ 서버 연결 확인됨.\n\n")
            disconnect_runner.run_api_disconnect_test(target_host, on_line=on_line)
        except Exception as e:
            on_line(f"\n[오류] 테스트 실행 실패: {e}\n")
        finally:
            self.root.after(0, self.on_api_disconnect_finished)
        
    def on_api_disconnect_finished(self):
        self.is_running = False
        self.toggle_ui_state(True)
        self.status_label.config(text="🟢 대기 중", fg="green")
        self.append_console("api_disconnect_test", "\n✅ API 끊김 방어 테스트 종료.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = K6Launcher(root)
    root.mainloop()
