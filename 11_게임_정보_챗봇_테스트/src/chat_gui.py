import threading
import json
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from typing import Callable, Optional


class ChatGUI:
    def __init__(self, root, reply_func: Optional[Callable[[str], str]] = None,
                 judge=None, save_callback: Optional[Callable] = None,
                 log_callback: Optional[Callable] = None,
                 clear_callback: Optional[Callable] = None):
        self.root = root
        self.reply_func = reply_func
        self.judge = judge
        self.save_callback = save_callback
        self.log_callback = log_callback
        self.clear_callback = clear_callback
        # 가장 최근 개별 평가 결과 (요약 블록과 함께 다시 그릴 때 사용)
        self.last_eval_text = ""

        root.title("Chat GUI")
        root.geometry("900x600")

        # 레이아웃: 왼쪽(채팅 히스토리 + 입력), 오른쪽(저지 결과)
        main_frame = tk.Frame(root)
        main_frame.pack(fill='both', expand=True)
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=0)

        # 왼쪽 프레임: 히스토리 및 입력
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, rowspan=2, sticky='nsew')
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)

        # 오른쪽 프레임: 저지 결과 출력창
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 5), pady=(5, 5))
        right_frame.rowconfigure(0, weight=1)

        # 채팅 기록창 (읽기 전용, 스크롤)
        self.history = ScrolledText(left_frame, state='disabled', wrap='word')
        self.history.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        # 저지 결과 출력창 (읽기 전용)
        self.judge_output = ScrolledText(right_frame, state='disabled', wrap='word', width=40)
        self.judge_output.grid(row=0, column=0, sticky='nsew')

        # 입력창과 전송 버튼을 담는 하단 프레임 (왼쪽 하단)
        bottom_frame = tk.Frame(left_frame)
        bottom_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

        # 채팅 입력창 (하단, 엔터로 전송)
        self.entry = tk.Entry(bottom_frame)
        self.entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.entry.bind('<Return>', self.on_enter)

        # 오른쪽 전송 버튼
        send_btn = tk.Button(bottom_frame, text='전송', width=8, command=self.on_send)
        send_btn.pack(side='right')

        # 클리어 버튼: 대화/평가 컨텍스트 초기화
        clear_btn = tk.Button(bottom_frame, text='클리어', width=8, command=self.on_clear)
        clear_btn.pack(side='right', padx=(0, 5))

    def add_message(self, sender, text):
        # 메시지를 아래쪽(시간순)으로 추가
        self.history.configure(state='normal')
        content = f"{sender}: {text}\n\n"
        self.history.insert('end', content)
        self.history.configure(state='disabled')
        # 항상 마지막이 보이도록
        try:
            self.history.yview_moveto(1.0)
        except Exception:
            pass
        try:
            self.history.update_idletasks()
        except Exception:
            pass

    def _session_summary(self) -> str:
        """세션 누적 평균 점수와 종합 Pass/Fail 요약 블록 생성."""
        if not self.judge:
            return ""
        avg = self.judge.running_average()
        verdict = self.judge.session_verdict()
        count = len(getattr(self.judge, 'scores', []))
        if avg is None:
            return "=== 세션 요약 ===\n평가 기록 없음\n\n"
        max_score = getattr(self.judge, 'MAX_SCORE', 5)
        return (
            "=== 세션 요약 ===\n"
            f"누적 질문 수: {count}\n"
            f"평균 점수: {avg:.1f} / {max_score}\n"
            f"종합 판정: {verdict} (기준 {self.judge.PASS_THRESHOLD})\n\n"
        )

    def add_judge_output(self, text: str):
        # 최근 개별 평가 텍스트를 저장하고, 세션 요약과 함께 다시 그림
        self.last_eval_text = text
        self._render_judge_output()

    def _render_judge_output(self):
        self.judge_output.configure(state='normal')
        self.judge_output.delete('1.0', 'end')
        self.judge_output.insert('end', self._session_summary())
        self.judge_output.insert('end', "=== 최근 평가 ===\n" + self.last_eval_text)
        self.judge_output.configure(state='disabled')

    def on_clear(self):
        # 대화/평가 컨텍스트 초기화
        if self.clear_callback:
            try:
                self.clear_callback()
            except Exception as e:
                print(f"[DEBUG] Clear callback error: {e}")
        # 채팅창 비우기
        self.history.configure(state='normal')
        self.history.delete('1.0', 'end')
        self.history.configure(state='disabled')
        # judge창 비우기
        self.last_eval_text = ""
        self.judge_output.configure(state='normal')
        self.judge_output.delete('1.0', 'end')
        self.judge_output.configure(state='disabled')

    def on_enter(self, event):
        self.on_send()
        return 'break'

    def on_send(self):
        msg = self.entry.get().strip()
        if not msg:
            return
        # 사용자 메시지 추가
        print(f"[DEBUG] Sending message: {msg}")
        self.add_message('나', msg)
        self.entry.delete(0, 'end')
        # 응답 생성: 에이전트 호출을 별도 스레드에서 처리
        thread = threading.Thread(target=self._handle_message, args=(msg,), daemon=True)
        thread.start()

    def generate_reply(self, msg):
        # 기본 폴백: reply_func이 없을 때 로컬 에코 응답
        if self.reply_func:
            try:
                return self.reply_func(msg)
            except Exception as e:
                return f"Error: {e}"
        return 'Echo: ' + msg

    def _handle_message(self, msg: str):
        # 에이전트에 메시지 전송
        try:
            if self.reply_func:
                reply = self.reply_func(msg)
            else:
                reply = 'Echo: ' + msg
        except Exception as e:
            reply = f"오류: {e}"
        print(f"[DEBUG] Generated reply: {reply}")

        # GUI 업데이트는 메인 스레드에서 수행: 응답(B)
        try:
            self.root.after(0, lambda: self.add_message('응답', reply))
        except Exception:
            self.add_message('응답', reply)

        # Judge 평가 및 저장/로그 처리 (비동기)
        eval_rec = None
        if self.judge:
            try:
                eval_rec = self.judge.evaluate(msg, reply)
            except Exception as e:
                eval_rec = {"error": str(e)}

        # 저장 콜백 호출 (C) — 평가 레코드 전체 전달
        if self.save_callback:
            try:
                self.save_callback(msg, reply, eval_rec)
            except Exception as e:
                print(f"[DEBUG] Save callback error: {e}")

        # 저지 결과를 우측 창에 출력 (D)
        try:
            judge_text = json_safe(eval_rec) if eval_rec is not None else ""
            self.root.after(0, lambda: self.add_judge_output(judge_text))
        except Exception as e:
            print(f"[DEBUG] Judge display error: {e}")

        # 로그 콜백 호출 (질문, 답변, Judge)
        if self.log_callback:
            try:
                lines = [f"## 질문", "", msg, "", "### 답변", "", reply, "", "### Judge", "", json_safe(eval_rec) if eval_rec is not None else ""]
                self.log_callback(lines)
            except Exception as e:
                print(f"[DEBUG] Log callback error: {e}")


def json_safe(obj):
    try:
        import json
        return json.dumps(obj, ensure_ascii=False, indent=2)
    except Exception:
        return str(obj)


def main():
    root = tk.Tk()
    app = ChatGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
