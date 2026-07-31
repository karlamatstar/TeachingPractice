import sys
from typing import Any

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMargins
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
)

from agent_app import build_agent
def extract_answer(result: dict[str, Any]) -> str:
    """LangChain agent.invoke 결과에서 마지막 AI 응답 텍스트를 꺼냅니다."""

    messages = result.get("messages", [])
    if not messages:
        return "응답 메시지가 없습니다."

    last_message = messages[-1]
    content = getattr(last_message, "content", "")

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
                elif "text" in block:
                    text_parts.append(str(block.get("text", "")))
            else:
                text_parts.append(str(block))
        return "\n".join(part for part in text_parts if part).strip()

    return str(content)


class AgentWorker(QThread):
    """LangChain 에이전트 호출을 백그라운드에서 처리하는 스레드"""

    result_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, agent, user_input: str):
        super().__init__()
        self.agent = agent
        self.user_input = user_input

    def run(self):
        try:
            result = self.agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": self.user_input,
                        }
                    ]
                }
            )
            answer = extract_answer(result)
            self.result_signal.emit(answer)
        except Exception as e:
            self.error_signal.emit(f"오류가 발생했습니다: {str(e)}")


class ChatBubble(QWidget):
    """채팅 말풍선 위젯"""

    def __init__(self, text: str, is_user: bool = False):
        super().__init__()
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 5, 0, 5)

        self.label = QLabel(text)
        self.label.setFont(QFont("Malgun Gothic", 10))
        self.label.setWordWrap(True)
        self.label.setMargin(10)
        self.label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        if is_user:
            # 사용자 메시지 (우측 정렬, 노란색 배경)
            self.label.setStyleSheet(
                """
                QLabel {
                    background-color: #FEE500;
                    color: black;
                    border-radius: 10px;
                }
                """
            )
            layout.addStretch(1)
            layout.addWidget(self.label)
        else:
            # AI 메시지 (좌측 정렬, 흰색 배경)
            self.label.setStyleSheet(
                """
                QLabel {
                    background-color: #FFFFFF;
                    color: black;
                    border-radius: 10px;
                }
                """
            )
            layout.addWidget(self.label)
            layout.addStretch(1)

        self.setLayout(layout)


class ChatWindow(QMainWindow):
    """메인 채팅 창"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LangChain AI 비서 (KakaoTalk Style)")
        self.resize(400, 600)

        try:
            self.agent = build_agent()
        except Exception as e:
            self.agent = None
            print(f"에이전트 초기화 실패: {e}")

        # 메인 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 전체 레이아웃
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        # 채팅 스크롤 영역 (카카오톡 배경색)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(
            """
            QScrollArea { border: none; background-color: #B2C7D9; }
            QWidget#scroll_content { background-color: #B2C7D9; }
            """
        )

        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("scroll_content")
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_content.setLayout(self.chat_layout)
        self.scroll_area.setWidget(self.scroll_content)

        main_layout.addWidget(self.scroll_area)

        # 하단 입력 영역
        input_container = QWidget()
        input_container.setStyleSheet("background-color: white; border-top: 1px solid #E0E0E0;")
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(10, 10, 10, 10)
        input_container.setLayout(input_layout)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("메시지를 입력하세요...")
        self.input_field.setFont(QFont("Malgun Gothic", 10))
        self.input_field.setStyleSheet(
            """
            QLineEdit {
                border: none;
                background-color: transparent;
            }
            """
        )
        self.input_field.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("전송")
        self.send_button.setFont(QFont("Malgun Gothic", 10, QFont.Weight.Bold))
        self.send_button.setStyleSheet(
            """
            QPushButton {
                background-color: #FEE500;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
                color: black;
            }
            QPushButton:hover {
                background-color: #E6CE00;
            }
            QPushButton:disabled {
                background-color: #E0E0E0;
                color: #A0A0A0;
            }
            """
        )
        self.send_button.clicked.connect(self.send_message)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)

        main_layout.addWidget(input_container)

        # 에이전트 초기화 실패 처리
        if not self.agent:
            self.add_message("시스템: 에이전트 초기화에 실패했습니다. 환경 변수를 확인하세요.", is_user=False)
            self.input_field.setEnabled(False)
            self.send_button.setEnabled(False)
        else:
            self.add_message("LangChain 멀티 도구 에이전트가 시작되었습니다. 무엇을 도와드릴까요?", is_user=False)

    def add_message(self, text: str, is_user: bool):
        bubble = ChatBubble(text, is_user)
        self.chat_layout.addWidget(bubble)
        
        # 스크롤 최하단으로 내리기
        self.scroll_area.verticalScrollBar().rangeChanged.connect(
            self.scroll_to_bottom
        )
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def send_message(self):
        text = self.input_field.text().strip()
        if not text:
            return

        # UI 업데이트
        self.add_message(text, is_user=True)
        self.input_field.clear()
        
        # UI 잠금 (입력 중 방지)
        self.input_field.setEnabled(False)
        self.send_button.setEnabled(False)
        
        # 백그라운드 스레드에서 에이전트 실행
        self.worker = AgentWorker(self.agent, text)
        self.worker.result_signal.connect(self.on_agent_response)
        self.worker.error_signal.connect(self.on_agent_error)
        self.worker.start()

    def on_agent_response(self, response: str):
        self.add_message(response, is_user=False)
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input_field.setFocus()

    def on_agent_error(self, error: str):
        self.add_message(error, is_user=False)
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input_field.setFocus()


def main():
    app = QApplication(sys.argv)
    
    # 애플리케이션 기본 폰트
    font = QFont("Malgun Gothic", 10)
    app.setFont(font)
    
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
