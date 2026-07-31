import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QScrollArea, QFrame, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

# 자체 모듈 임포트
from chatbot import generate_response_stream, ChatbotError
from evaluator import evaluate_response, METRIC_NAMES_KO
from logger import save_log

METRICS = list(METRIC_NAMES_KO.keys())
WINDOW_TITLE = "스타일몰 채팅 상담 (Client) - PASS 데모"
WELCOME_MESSAGE = "트렌디한 쇼핑몰 '스타일몰'에 오신 것을 환영합니다! 무엇이든 물어보세요. (PASS 데모)"


class ChatThread(QThread):
    chunk_received = pyqtSignal(str)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, chat_history):
        super().__init__()
        self.chat_history = chat_history

    def run(self):
        full_text = ""
        try:
            stream_gen = generate_response_stream(self.chat_history)
            for chunk in stream_gen:
                if chunk:
                    full_text += chunk
                    self.chunk_received.emit(full_text)
            self.finished_signal.emit(full_text)
        except ChatbotError as e:
            self.error_signal.emit(str(e))


class EvalThread(QThread):
    eval_finished = pyqtSignal(dict, dict)  # log_data, eval_result

    def __init__(self, chat_history, question, answer, is_continued_chat):
        super().__init__()
        self.chat_history = chat_history
        self.question = question
        self.answer = answer
        self.is_continued_chat = is_continued_chat

    def run(self):
        eval_result = evaluate_response(self.chat_history, self.question, self.answer)
        if eval_result:
            log_data = save_log(self.question, self.answer, eval_result, self.is_continued_chat)
            self.eval_finished.emit(log_data, eval_result)
        else:
            self.eval_finished.emit({}, {})


class StyleMallChatClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(1000, 700)
        self.messages = []

        # 메인 위젯 및 레이아웃 설정
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # 좌측: 채팅창 영역
        chat_section = QWidget()
        chat_layout = QVBoxLayout(chat_section)

        # 스크롤 영역 (카카오톡 배경색)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: #b2c7d9; border: none;")

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: #b2c7d9;")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.scroll_content)
        chat_layout.addWidget(self.scroll_area)

        # 입력 영역
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("메시지를 입력하세요...")
        self.input_field.setFixedHeight(40)
        self.input_field.returnPressed.connect(self.send_message)

        self.send_btn = QPushButton("전송")
        self.send_btn.setFixedHeight(40)
        self.send_btn.setStyleSheet("background-color: #fef01b; font-weight: bold; border-radius: 5px;")
        self.send_btn.clicked.connect(self.send_message)

        self.reset_btn = QPushButton("대화 초기화")
        self.reset_btn.setFixedHeight(40)
        self.reset_btn.setStyleSheet("background-color: #ffcccc; font-weight: bold; border-radius: 5px;")
        self.reset_btn.clicked.connect(self.reset_chat)

        self.log_btn = QPushButton("로그 확인")
        self.log_btn.setFixedHeight(40)
        self.log_btn.setStyleSheet("background-color: #aaddff; font-weight: bold; border-radius: 5px;")
        self.log_btn.clicked.connect(self.open_log_file)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)
        input_layout.addWidget(self.reset_btn)
        input_layout.addWidget(self.log_btn)
        chat_layout.addLayout(input_layout)

        # 우측: 평가 결과 사이드바
        sidebar_section = QFrame()
        sidebar_section.setFixedWidth(300)
        sidebar_section.setStyleSheet("background-color: #ffffff; border-left: 1px solid #ddd;")
        sidebar_layout = QVBoxLayout(sidebar_section)
        sidebar_layout.setAlignment(Qt.AlignTop)

        title_label = QLabel("📊 평가 결과 패널")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        sidebar_layout.addWidget(title_label)

        desc_label = QLabel("마지막으로 생성된 챗봇 응답의\n8대 지표 평가 점수입니다.")
        desc_label.setStyleSheet("color: gray;")
        sidebar_layout.addWidget(desc_label)

        self.eval_labels = {}
        # 지표별 라벨 생성
        self.total_score_label = QLabel("총 평균 점수: 대기 중")
        self.total_score_label.setFont(QFont("Arial", 12, QFont.Bold))
        sidebar_layout.addWidget(self.total_score_label)
        sidebar_layout.addSpacing(10)

        for metric in METRICS:
            lbl = QLabel(f"<b>{metric.upper()}</b>: -")
            lbl.setWordWrap(True)
            self.eval_labels[metric] = lbl
            sidebar_layout.addWidget(lbl)

        # 레이아웃 결합
        main_layout.addWidget(chat_section, 7)  # 채팅창 비율 7
        main_layout.addWidget(sidebar_section, 3)  # 사이드바 비율 3

        # 초기 환영 메시지 추가
        self.add_bubble(WELCOME_MESSAGE, is_user=False)
        self.current_bot_bubble = None

    def add_bubble(self, text, is_user=True):
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setContentsMargins(10, 10, 10, 10)

        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        if is_user:
            bubble.setStyleSheet("background-color: #fef01b; color: black; border-radius: 10px;")
            container_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
            container_layout.addWidget(bubble)
        else:
            bubble.setStyleSheet("background-color: #ffffff; color: black; border-radius: 10px; border: 1px solid #d9d9d9;")
            container_layout.addWidget(bubble)
            container_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.scroll_layout.addWidget(container)

        # 스크롤 최하단으로 내리기
        QTimer.singleShot(50, self.scroll_to_bottom)
        return bubble

    def scroll_to_bottom(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def _reset_eval_panel(self, placeholder="-"):
        # 렌더링된 라벨 텍스트를 역파싱하지 않고, self.eval_labels의 키(metric 이름)를
        # 직접 사용해서 라벨을 재구성한다.
        for metric, lbl in self.eval_labels.items():
            lbl.setText(f"<b>{metric.upper()}</b>: {placeholder}")

    def reset_chat(self):
        self.messages = []

        # 채팅창 비우기
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # 평가 패널 초기화
        self.total_score_label.setText("총 평균 점수: 대기 중")
        self._reset_eval_panel("-")

        # 초기 환영 메시지 추가
        self.add_bubble(WELCOME_MESSAGE, is_user=False)
        self.current_bot_bubble = None
        self.input_field.clear()
        self.input_field.setFocus()

    def open_log_file(self):
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        log_file_path = os.path.join(project_root, "_OUTPUT", "pass", "logs", "QA_Result_Log.csv")
        if os.path.exists(log_file_path):
            os.startfile(log_file_path)
        else:
            print("로그 파일이 존재하지 않습니다:", log_file_path)

    def send_message(self):
        text = self.input_field.text().strip()
        if not text:
            return

        # 사용자 메시지 UI 추가
        self.add_bubble(text, is_user=True)
        self.input_field.clear()
        self.input_field.setEnabled(False)
        self.send_btn.setEnabled(False)

        # 챗봇 빈 말풍선 생성
        self.current_bot_bubble = self.add_bubble("...", is_user=False)

        # 이전 대화 히스토리 (현재 질문 제외)
        chat_history = self.messages.copy()
        is_continued_chat = len(chat_history) > 0
        self.messages.append({"role": "user", "content": text})

        # 챗봇 답변 쓰레드 시작
        self.chat_thread = ChatThread(self.messages.copy())
        self.chat_thread.chunk_received.connect(self.update_stream)
        self.chat_thread.finished_signal.connect(lambda response: self.on_chat_finished(response, text, chat_history, is_continued_chat))
        self.chat_thread.error_signal.connect(self.on_chat_error)
        self.chat_thread.start()

    def update_stream(self, text):
        if self.current_bot_bubble:
            self.current_bot_bubble.setText(text)
            self.scroll_to_bottom()

    def on_chat_error(self, error_message):
        if self.current_bot_bubble:
            self.current_bot_bubble.setText(f"[오류] {error_message}")
            self.scroll_to_bottom()
        self.input_field.setEnabled(True)
        self.send_btn.setEnabled(True)
        self.input_field.setFocus()

    def on_chat_finished(self, response, user_question, history_for_eval, is_continued_chat):
        # 챗봇 답변 기록
        self.messages.append({"role": "assistant", "content": response})

        # 평가 중 표시
        self.total_score_label.setText("총 평균 점수: 평가 중... ⏳")
        self._reset_eval_panel("평가 중...")

        # 평가 쓰레드 시작
        self.eval_thread = EvalThread(history_for_eval, user_question, response, is_continued_chat)
        self.eval_thread.eval_finished.connect(self.update_eval_panel)
        self.eval_thread.start()

        # UI 활성화
        self.input_field.setEnabled(True)
        self.send_btn.setEnabled(True)
        self.input_field.setFocus()

    def update_eval_panel(self, log_data, eval_result):
        if not log_data or not eval_result:
            self.total_score_label.setText("총 평균 점수: 평가 실패")
            self._reset_eval_panel("에러")
            return

        avg_score = log_data.get('average_score', 0)
        passed = log_data.get('total_passed', False)
        status = "<span style='color:green;'>PASS</span>" if passed else "<span style='color:red;'>FAIL</span>"

        self.total_score_label.setText(f"총 평균 점수: {avg_score:.2f} / 5.0 ({status})")

        for metric, data in eval_result.items():
            if metric not in self.eval_labels:
                continue

            score = data.get("score", 0)
            reason = data.get("reason", "")
            color = "green" if score >= 3.5 else "red"

            lbl_text = f"<b>{metric.upper()}</b>: <span style='color:{color}'>{score}</span> 점<br><span style='color:gray; font-size:11px;'>{reason}</span><br>"
            self.eval_labels[metric].setText(lbl_text)


if __name__ == '__main__':
    print("====================================================")
    print("        스타일몰 챗봇 프로그램 (Client) - PASS 데모   ")
    print("====================================================")
    print("\n현재 챗봇 프로그램이 실행 중입니다...\n")
    print("[주의]")
    print("이 명령 프롬프트 창을 임의로 종료하지 마세요.")
    print("챗봇 클라이언트 화면을 닫으면 이 창도 함께 자동으로 종료됩니다.\n")
    print("====================================================\n")

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = StyleMallChatClient()
    window.show()
    sys.exit(app.exec_())
