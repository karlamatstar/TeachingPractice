"""
RAG 챗봇 도구 런처
실행: python launcher.py
"""
import sys, subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


def _launch(script: str):
    subprocess.Popen(
        [sys.executable, str(BASE_DIR / script)],
        cwd=str(BASE_DIR),
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
    )
    QApplication.instance().quit()


class Launcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RAG 챗봇 도구")
        self.setFixedSize(420, 200)
        self.setStyleSheet("background:#1E1E1E;")
        self._build_ui()
        self._center()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 32)
        root.setSpacing(20)

        title = QLabel("RAG 챗봇 도구 모음")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color:#CCCCCC;font-size:15px;font-weight:bold;background:transparent;")
        root.addWidget(title)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(16)

        chatbot_btn = QPushButton("💬\n\n챗봇")
        chatbot_btn.setFixedHeight(88)
        chatbot_btn.setCursor(Qt.PointingHandCursor)
        chatbot_btn.setStyleSheet("""
            QPushButton{background:#0E639C;border:none;border-radius:8px;
                color:white;font-size:14px;font-weight:bold;}
            QPushButton:hover{background:#1177BB;}
            QPushButton:pressed{background:#0A4D7A;}
        """)
        chatbot_btn.clicked.connect(lambda: _launch("app_gui.py"))
        btn_row.addWidget(chatbot_btn)

        judge_btn = QPushButton("🧪\n\n저지 에이전트")
        judge_btn.setFixedHeight(88)
        judge_btn.setCursor(Qt.PointingHandCursor)
        judge_btn.setStyleSheet("""
            QPushButton{background:#4CAF50;border:none;border-radius:8px;
                color:white;font-size:14px;font-weight:bold;}
            QPushButton:hover{background:#66BB6A;}
            QPushButton:pressed{background:#388E3C;}
        """)
        judge_btn.clicked.connect(lambda: _launch("judge_gui.py"))
        btn_row.addWidget(judge_btn)

        root.addLayout(btn_row)

    def _center(self):
        screen = QApplication.primaryScreen().geometry()
        fg = self.frameGeometry()
        fg.moveCenter(screen.center())
        self.move(fg.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("맑은 고딕", 10))
    win = Launcher()
    win.show()
    sys.exit(app.exec_())
