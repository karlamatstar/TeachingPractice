"""
RAG 챗봇 Judge Agent GUI
실행: python judge_gui.py   (_reports/ 폴더 기준)
"""
import sys, os, re
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR.parent / "_OUTPUT"

from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QFileDialog, QTextEdit, QListWidget,
    QListWidgetItem, QFrame, QProgressBar,
)
from PyQt5.QtCore import Qt, QProcess, QProcessEnvironment
from PyQt5.QtGui import QFont, QColor

_TC_PROGRESS = re.compile(r'\[(\d+)/(\d+)\]')

_FILE_ICONS = {".md": "📄", ".json": "📊", ".csv": "📋"}
_FILE_LABEL = {
    ".csv":  "📋  CSV 생성",
    ".json": "📊  결과 JSON 생성",
    ".md":   "📄  보고서 MD 생성",
}

_SUPPRESS = ("UserWarning", "DeprecationWarning", "pydantic", "langchain-community",
             "LangChainDeprecationWarning")

_RUN_STYLE = """
    QPushButton{background:#4CAF50;border:none;border-radius:5px;
        color:white;font-size:13px;font-weight:bold;padding:0 18px;}
    QPushButton:hover{background:#66BB6A;}
    QPushButton:pressed{background:#388E3C;}
    QPushButton:disabled{background:#555;color:#888;}
"""
_STOP_STYLE = """
    QPushButton{background:#E53935;border:none;border-radius:5px;
        color:white;font-size:13px;font-weight:bold;padding:0 18px;}
    QPushButton:hover{background:#EF5350;}
"""


class JudgeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RAG 챗봇 Judge Agent")
        self.resize(1220, 780)
        self._proc = None
        self._files_before: set = set()
        self._build_ui()
        self._refresh_file_list()

    # ── UI 구성 ────────────────────────────────────────────────────

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        h = QHBoxLayout(root)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)

        # ── 좌측 패널 ─────────────────────────────────────────────
        left = QWidget()
        left.setStyleSheet("background:#1E1E1E;")
        lv = QVBoxLayout(left)
        lv.setContentsMargins(18, 16, 18, 16)
        lv.setSpacing(10)

        # 로그 영역을 먼저 생성 (버튼 connect 시 참조 필요)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFont(QFont("Consolas", 10))
        self.log.setStyleSheet("""
            QTextEdit{background:#141414;border:1px solid #333;border-radius:4px;
                color:#D4D4D4;padding:6px;}
        """)

        title = QLabel("🧪  RAG 챗봇 Judge Agent")
        title.setStyleSheet(
            "color:#CCCCCC;font-size:15px;font-weight:bold;background:transparent;")
        lv.addWidget(title)

        # TC 파일 선택 행
        tc_row = QHBoxLayout()
        tc_row.setSpacing(6)
        tc_lbl = QLabel("TC 파일")
        tc_lbl.setFixedWidth(54)
        tc_lbl.setStyleSheet("color:#9CDCFE;font-size:12px;background:transparent;")
        tc_row.addWidget(tc_lbl)

        self.tc_edit = QLineEdit(str(BASE_DIR / "test_cases.json"))
        self.tc_edit.setStyleSheet("""
            QLineEdit{background:#2D2D2D;border:1px solid #555;border-radius:4px;
                color:#D4D4D4;padding:4px 8px;font-size:12px;}
            QLineEdit:focus{border-color:#569CD6;}
        """)
        tc_row.addWidget(self.tc_edit, 1)

        browse = QPushButton("찾기")
        browse.setFixedWidth(54)
        browse.setCursor(Qt.PointingHandCursor)
        browse.setStyleSheet("""
            QPushButton{background:#3C3C3C;border:1px solid #555;border-radius:4px;
                color:#D4D4D4;padding:4px 8px;font-size:11px;}
            QPushButton:hover{background:#4C4C4C;}
        """)
        browse.clicked.connect(self._browse_tc)
        tc_row.addWidget(browse)
        lv.addLayout(tc_row)

        # 버튼 행
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.run_btn = QPushButton("▶  평가 실행")
        self.run_btn.setFixedHeight(40)
        self.run_btn.setCursor(Qt.PointingHandCursor)
        self.run_btn.setStyleSheet(_RUN_STYLE)
        self.run_btn.clicked.connect(self._toggle_run)
        btn_row.addWidget(self.run_btn)

        clr_btn = QPushButton("🗑  로그 지우기")
        clr_btn.setFixedHeight(40)
        clr_btn.setCursor(Qt.PointingHandCursor)
        clr_btn.setStyleSheet("""
            QPushButton{background:#3C3C3C;border:1px solid #555;border-radius:5px;
                color:#D4D4D4;font-size:12px;padding:0 12px;}
            QPushButton:hover{background:#4C4C4C;}
        """)
        clr_btn.clicked.connect(self.log.clear)
        btn_row.addWidget(clr_btn)
        btn_row.addStretch()

        self.status_lbl = QLabel("대기 중")
        self.status_lbl.setStyleSheet(
            "color:#666;font-size:11px;background:transparent;")
        btn_row.addWidget(self.status_lbl)
        lv.addLayout(btn_row)

        # 진행률 바
        self.progress = QProgressBar()
        self.progress.setFixedHeight(6)
        self.progress.setTextVisible(False)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setStyleSheet("""
            QProgressBar{background:#2D2D2D;border:none;border-radius:3px;}
            QProgressBar::chunk{background:#4CAF50;border-radius:3px;}
        """)
        lv.addWidget(self.progress)

        lv.addWidget(self.log, 1)

        h.addWidget(left, 1)

        # ── 구분선 ────────────────────────────────────────────────
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setStyleSheet("color:#333;background:#333;")
        sep.setFixedWidth(1)
        h.addWidget(sep)

        # ── 우측 파일 패널 ────────────────────────────────────────
        right = QWidget()
        right.setFixedWidth(290)
        right.setStyleSheet("background:#252526;")
        rv = QVBoxLayout(right)
        rv.setContentsMargins(12, 16, 12, 12)
        rv.setSpacing(8)

        file_hdr = QLabel("📁  생성된 파일")
        file_hdr.setStyleSheet(
            "color:#CCCCCC;font-size:13px;font-weight:bold;background:transparent;")
        rv.addWidget(file_hdr)

        self.file_list = QListWidget()
        self.file_list.setStyleSheet("""
            QListWidget{background:#252526;border:none;color:#CCCCCC;font-size:11px;}
            QListWidget::item{padding:5px 6px;border-radius:3px;}
            QListWidget::item:hover{background:#2A2D2E;}
            QListWidget::item:selected{background:#094771;color:white;}
        """)
        self.file_list.itemDoubleClicked.connect(self._open_file)
        rv.addWidget(self.file_list, 1)

        hint = QLabel("더블클릭으로 파일 열기")
        hint.setStyleSheet("color:#555;font-size:10px;background:transparent;")
        hint.setAlignment(Qt.AlignCenter)
        rv.addWidget(hint)

        refresh_btn = QPushButton("🔄  새로고침")
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton{background:#3C3C3C;border:1px solid #555;border-radius:5px;
                color:#D4D4D4;font-size:11px;padding:7px;}
            QPushButton:hover{background:#4C4C4C;}
        """)
        refresh_btn.clicked.connect(self._refresh_file_list)
        rv.addWidget(refresh_btn)

        h.addWidget(right)

    # ── 파일 선택 ──────────────────────────────────────────────────

    def _browse_tc(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "TC JSON 파일 선택", str(BASE_DIR), "JSON 파일 (*.json)")
        if path:
            self.tc_edit.setText(path)

    # ── 실행 토글 ──────────────────────────────────────────────────

    def _toggle_run(self):
        if self._proc and self._proc.state() != QProcess.NotRunning:
            self._proc.kill()
        else:
            self._start_eval()

    def _start_eval(self):
        self._files_before = self._get_output_files()
        self.progress.setValue(0)
        self.log.clear()
        self._sep()
        self._log(f"  평가 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "#569CD6")
        self._log(f"  TC 파일: {self.tc_edit.text().strip()}", "#569CD6")
        self._sep()

        self._proc = QProcess(self)
        env = QProcessEnvironment.systemEnvironment()
        env.insert("PYTHONIOENCODING", "utf-8")
        env.insert("PYTHONUTF8", "1")
        env.insert("PYTHONUNBUFFERED", "1")
        self._proc.setProcessEnvironment(env)

        self._proc.readyReadStandardOutput.connect(self._on_stdout)
        self._proc.readyReadStandardError.connect(self._on_stderr)
        self._proc.finished.connect(self._on_finished)

        tc_path = self.tc_edit.text().strip()
        self._proc.start(sys.executable, [str(BASE_DIR / "judge_agent.py"), tc_path])

        self.run_btn.setText("⏹  중단")
        self.run_btn.setStyleSheet(_STOP_STYLE)
        self.status_lbl.setText("평가 실행 중…")

    # ── 프로세스 출력 핸들링 ──────────────────────────────────────

    def _on_stdout(self):
        raw = bytes(self._proc.readAllStandardOutput()).decode("utf-8", "replace")
        for line in raw.splitlines():
            line = line.rstrip()
            if not line:
                continue
            m = _TC_PROGRESS.search(line)
            if m:
                cur, total = int(m.group(1)), int(m.group(2))
                self.progress.setValue(int(cur / total * 100))
                self.status_lbl.setText(f"{cur} / {total} 평가 중")
            self._log(line, self._line_color(line))

    def _on_stderr(self):
        raw = bytes(self._proc.readAllStandardError()).decode("utf-8", "replace")
        for line in raw.splitlines():
            line = line.rstrip()
            if not line:
                continue
            if any(k in line for k in _SUPPRESS):
                continue
            self._log(line, "#CE9178")

    def _on_finished(self, code, _):
        self._sep()
        if code == 0:
            self._log("  ✅  평가 완료!", "#4EC9B0")
            self.progress.setValue(100)
        else:
            self._log(f"  ❌  오류 발생 (exit: {code})", "#F44747")
        self._sep()

        # 새로 생성된 파일 알림
        new_files = self._get_output_files() - self._files_before
        if new_files:
            self._log("  📂  생성된 파일:", "#DCDCAA")
            for ps in sorted(new_files):
                p = Path(ps)
                label = _FILE_LABEL.get(p.suffix, "파일 생성")
                self._log(f"     {label}: {p.name}", "#DCDCAA")

        self.run_btn.setText("▶  평가 실행")
        self.run_btn.setStyleSheet(_RUN_STYLE)
        self.status_lbl.setText("완료" if code == 0 else "오류 발생")
        self._refresh_file_list()

    # ── 로그 헬퍼 ─────────────────────────────────────────────────

    def _line_color(self, line: str) -> str:
        s = line.strip()
        if "PASS" in s:             return "#4EC9B0"
        if "FAIL" in s:             return "#F44747"
        if s.startswith("✅"):      return "#6A9955"
        if s.startswith("❌"):      return "#F44747"
        if s.startswith("⚠"):      return "#CE9178"
        if s.startswith("→"):       return "#DCDCAA"
        if s.startswith("["):       return "#9CDCFE"
        if "결함위치:" in s:        return "#C586C0"
        if "보고서:" in s or "JSON" in s or "CSV" in s:  return "#DCDCAA"
        return "#BBBBBB"

    def _log(self, text: str, color: str = "#D4D4D4"):
        self.log.setTextColor(QColor(color))
        self.log.append(text)
        sb = self.log.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _sep(self):
        self._log("─" * 60, "#3A3A3A")

    # ── 파일 패널 ─────────────────────────────────────────────────

    def _get_output_files(self) -> set:
        result = set()
        for folder in ("reports", "test_results"):
            d = OUTPUT_DIR / folder
            if d.exists():
                result.update(str(f) for f in d.iterdir() if f.is_file())
        return result

    def _refresh_file_list(self):
        self.file_list.clear()
        sections = [
            ("📄  보고서 (MD)", ".md"),
            ("📊  결과 (JSON)", ".json"),
            ("📋  CSV", ".csv"),
        ]
        found = False
        for title, ext in sections:
            files = []
            for folder in ("reports", "test_results"):
                d = OUTPUT_DIR / folder
                if d.exists():
                    files += [f for f in d.iterdir() if f.suffix == ext]
            files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            if not files:
                continue
            found = True
            hdr = QListWidgetItem(title)
            hdr.setFlags(Qt.NoItemFlags)
            hdr.setForeground(QColor("#569CD6"))
            self.file_list.addItem(hdr)
            for f in files:
                item = QListWidgetItem(f"   {f.name}")
                item.setData(Qt.UserRole, str(f))
                item.setToolTip(str(f))
                self.file_list.addItem(item)

        if not found:
            empty = QListWidgetItem("  생성된 파일 없음")
            empty.setFlags(Qt.NoItemFlags)
            empty.setForeground(QColor("#555"))
            self.file_list.addItem(empty)

    def _open_file(self, item: QListWidgetItem):
        path = item.data(Qt.UserRole)
        if path:
            os.startfile(path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("맑은 고딕", 10))
    win = JudgeGUI()
    win.show()
    sys.exit(app.exec_())
