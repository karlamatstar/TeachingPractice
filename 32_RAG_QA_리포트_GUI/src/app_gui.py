"""
RAG 챗봇 — PyQt5 데스크톱 GUI 클라이언트
실행: python app_gui.py   (_reports/ 폴더에서 실행)

중요: chromadb 는 QApplication 생성 전 모듈 레벨에서 초기화해야 합니다.
"""
import sys, shutil, threading, csv
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

DOCUMENTS_DIR = BASE_DIR / "documents"
PERSIST_DIRECTORY = str(BASE_DIR / "chroma_db")
COLLECTION_NAME = "rag_documents"
ALLOWED_EXT = {".pdf", ".txt", ".md"}

DOCUMENTS_DIR.mkdir(exist_ok=True)

CHAT_LOG_DIR = BASE_DIR / "chat_log"
CHAT_LOG_DIR.mkdir(exist_ok=True)

# ── ChromaDB + LangChain 초기화 (QApplication 생성 전 필수) ───────────────────
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
_vector_db = Chroma(
    persist_directory=PERSIST_DIRECTORY,
    embedding_function=_embeddings,
    collection_name=COLLECTION_NAME,
)

# ── PyQt5 ─────────────────────────────────────────────────────────────────────
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QScrollArea, QFrame, QFileDialog,
    QListWidget, QListWidgetItem, QSizePolicy, QMessageBox,
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QProcess
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent

# ── 상태 아이콘 ───────────────────────────────────────────────────────────────
_ICON = {"DB 등록됨": "✅", "로딩 중…": "⏳", "오류": "❌"}


# ── 채팅 로그 ─────────────────────────────────────────────────────────────────

def _save_chat_log(question: str, answer: str):
    now  = datetime.now()
    path = CHAT_LOG_DIR / f"chat_{now.strftime('%Y%m%d')}.csv"
    is_new = not path.exists()
    seq = 1
    if not is_new:
        try:
            with open(path, encoding="utf-8-sig", newline="") as f:
                seq = sum(1 for r in csv.reader(f) if r)  # header 포함 행 수 = 다음 데이터 번호
        except Exception:
            seq = 1
    with open(path, "a", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(["번호", "날짜&시간", "질문", "답변"])
        w.writerow([seq, now.strftime("%Y-%m-%d %H:%M:%S"), question, answer])


# ── RAG 헬퍼 ─────────────────────────────────────────────────────────────────

def _get_db_sources() -> set:
    try:
        results = _vector_db.get(include=["metadatas"])
        return {
            Path(m["source"]).name
            for m in results.get("metadatas", [])
            if m.get("source")
        }
    except Exception:
        return set()


def _run_rag(question: str) -> tuple:
    docs = _vector_db.similarity_search(question, k=3)
    if not docs:
        return "관련 문서를 찾지 못했습니다. 먼저 문서를 업로드해 주세요.", []

    context = "\n\n".join(
        f"[출처: {d.metadata.get('source','알 수 없음')}]\n{d.page_content}"
        for d in docs
    )
    prompt = f"""당신은 업로드된 문서 기반 챗봇입니다.

반드시 아래 제공된 문서 내용만 근거로 답변하십시오.
문서에 없는 내용은 추측하지 말고,
"제공된 문서에서는 확인할 수 없습니다."라고 답하십시오.

[문서 내용]
{context}

[사용자 질문]
{question}

[답변 작성 원칙]
1. 한국어로 답변한다.
2. 핵심 답변을 먼저 제시한다.
3. 문서 근거가 있으면 자연스럽게 설명한다.
4. 답변 끝에 참고한 파일명을 표시한다.
"""
    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    response = llm.invoke(prompt)
    sources = list({d.metadata.get("source", "알 수 없음") for d in docs})
    return response.content, sources


# ── RAG 시그널 브리지 ─────────────────────────────────────────────────────────
class _RAGBridge(QObject):
    done   = pyqtSignal(str, list)
    failed = pyqtSignal(str)

_rag_bridge = _RAGBridge()


# ── DB 재생성 완료 브리지 ─────────────────────────────────────────────────────
class _RebuildBridge(QObject):
    done   = pyqtSignal()
    failed = pyqtSignal(str)

_rebuild_bridge = _RebuildBridge()


# ── 드래그 & 드롭 영역 ────────────────────────────────────────────────────────
class DropZone(QFrame):
    files_dropped = pyqtSignal(list)
    _N = "DropZone{border:2px dashed #AAA;border-radius:10px;background:#FAFAFA;}"
    _H = "DropZone{border:2px dashed #FEE500;border-radius:10px;background:#FFFDE7;}"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumHeight(80)
        self.setStyleSheet(self._N)
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignCenter)
        lay.setSpacing(3)
        icon = QLabel("📂"); icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("font-size:24px;border:none;background:transparent;")
        hint = QLabel("파일을 드래그하세요\n(PDF · TXT · MD)")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color:#888;font-size:11px;border:none;background:transparent;")
        lay.addWidget(icon); lay.addWidget(hint)

    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls():
            e.acceptProposedAction(); self.setStyleSheet(self._H)
    def dragLeaveEvent(self, e): self.setStyleSheet(self._N)
    def dropEvent(self, e: QDropEvent):
        self.setStyleSheet(self._N)
        paths = [u.toLocalFile() for u in e.mimeData().urls()
                 if Path(u.toLocalFile()).suffix.lower() in ALLOWED_EXT]
        if paths: self.files_dropped.emit(paths)


# ── 채팅 말풍선 ───────────────────────────────────────────────────────────────
class Bubble(QWidget):
    def __init__(self, text, is_user, ts, parent=None):
        super().__init__(parent)
        row = QHBoxLayout(self)
        row.setContentsMargins(10, 3, 10, 3)
        row.setSpacing(6)

        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        label.setMaximumWidth(420)
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        time_lbl = QLabel(ts)
        time_lbl.setStyleSheet("color:#999;font-size:10px;background:transparent;")
        time_lbl.setAlignment(Qt.AlignBottom)
        time_lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        if is_user:
            label.setStyleSheet("""QLabel{background:#FEE500;border-radius:14px;
                border-bottom-right-radius:3px;padding:10px 14px;
                font-size:13px;color:#111;}""")
            row.addStretch(); row.addWidget(time_lbl); row.addWidget(label)
        else:
            label.setStyleSheet("""QLabel{background:#FFF;border-radius:14px;
                border-top-left-radius:3px;padding:10px 14px;
                font-size:13px;color:#111;}""")
            row.addWidget(label); row.addWidget(time_lbl); row.addStretch()


# ── 메인 윈도우 ───────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RAG 문서 챗봇")
        self.setMinimumSize(1000, 700)
        self.resize(1100, 780)

        self._rag_busy    = False
        self._delete_mode = False
        self._procs: set  = set()

        self._build_ui()
        _rag_bridge.done.connect(self._on_rag_done)
        _rag_bridge.failed.connect(self._on_rag_failed)
        _rebuild_bridge.done.connect(self._on_db_refreshed)
        _rebuild_bridge.failed.connect(lambda msg: self.status_lbl.setText(msg))
        QTimer.singleShot(100, self._auto_ingest_on_start)

    # ── UI ───────────────────────────────────────────────────────────────────
    def _build_ui(self):
        root = QWidget(); self.setCentralWidget(root)
        h = QHBoxLayout(root)
        h.setContentsMargins(0,0,0,0); h.setSpacing(0)
        h.addWidget(self._make_sidebar())
        h.addWidget(self._make_chat_panel(), stretch=1)

    def _make_sidebar(self):
        panel = QWidget()
        panel.setFixedWidth(290)                          # ← 가로폭 확대
        panel.setStyleSheet("background:#EFEFEF;")

        v = QVBoxLayout(panel)
        v.setContentsMargins(12,16,12,12)
        v.setSpacing(8)

        # 타이틀
        v.addWidget(QLabel("📂 문서 관리",
            styleSheet="font-size:14px;font-weight:bold;color:#333;"))

        # 드롭존
        self.drop_zone = DropZone()
        self.drop_zone.files_dropped.connect(self._handle_files)
        v.addWidget(self.drop_zone)

        # 파일 추가 버튼
        add_btn = QPushButton("＋  파일 추가")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setStyleSheet(self._btn_style("#FEE500","#FFD900","#F5C800"))
        add_btn.clicked.connect(self._open_picker)
        v.addWidget(add_btn)

        v.addWidget(self._hsep())
        v.addWidget(QLabel("등록된 문서", styleSheet="font-size:11px;color:#666;"))

        # 문서 리스트
        self.file_list = QListWidget()
        self.file_list.setStyleSheet("""
            QListWidget{border:1px solid #DDD;border-radius:6px;
                background:white;font-size:12px;}
            QListWidget::item{padding:5px 8px;border-bottom:1px solid #F0F0F0;color:#333;}
            QListWidget::item:selected{background:#E3F2FD;color:#1565C0;}
            QListWidget::item:hover{background:#F5F5F5;}
        """)
        v.addWidget(self.file_list)

        # 일반 모드: [문서 삭제] 단독
        self.del_mode_btn = QPushButton("문서 삭제")
        self.del_mode_btn.setCursor(Qt.PointingHandCursor)
        self.del_mode_btn.setStyleSheet(self._outline_btn_style())
        self.del_mode_btn.clicked.connect(self._enter_delete_mode)
        v.addWidget(self.del_mode_btn)

        # 삭제 모드: [전체선택/전체해제] [취소] 행 (숨김으로 시작)
        self._del_btn_row_widget = QWidget()
        del_btn_row = QHBoxLayout(self._del_btn_row_widget)
        del_btn_row.setContentsMargins(0, 0, 0, 0)
        del_btn_row.setSpacing(6)

        self.select_all_btn = QPushButton("전체선택")
        self.select_all_btn.setCursor(Qt.PointingHandCursor)
        self.select_all_btn.setStyleSheet(self._outline_btn_style())
        self.select_all_btn.clicked.connect(self._toggle_select_all)
        del_btn_row.addWidget(self.select_all_btn)

        self.cancel_del_btn = QPushButton("취소")
        self.cancel_del_btn.setCursor(Qt.PointingHandCursor)
        self.cancel_del_btn.setStyleSheet(self._outline_btn_style())
        self.cancel_del_btn.clicked.connect(self._exit_delete_mode)
        del_btn_row.addWidget(self.cancel_del_btn)

        self._del_btn_row_widget.setVisible(False)
        v.addWidget(self._del_btn_row_widget)

        # 삭제 실행 버튼 (삭제 모드에서만 표시)
        self.confirm_del_btn = QPushButton("🗑  선택 항목 삭제")
        self.confirm_del_btn.setCursor(Qt.PointingHandCursor)
        self.confirm_del_btn.setStyleSheet("""
            QPushButton{background:#E53935;border:none;border-radius:7px;
                padding:8px;font-size:12px;font-weight:bold;color:#FFF;}
            QPushButton:hover{background:#C62828;}
            QPushButton:pressed{background:#B71C1C;}
        """)
        self.confirm_del_btn.clicked.connect(self._confirm_delete)
        self.confirm_del_btn.setVisible(False)
        v.addWidget(self.confirm_del_btn)

        v.addWidget(self._hsep())

        # 상태 레이블
        self.status_lbl = QLabel("")
        self.status_lbl.setWordWrap(True)
        self.status_lbl.setStyleSheet("font-size:11px;color:#777;")
        v.addWidget(self.status_lbl)

        # DB 초기화 후 재생성 버튼
        rebuild_btn = QPushButton("🔄  DB 초기화 후 재생성")
        rebuild_btn.setCursor(Qt.PointingHandCursor)
        rebuild_btn.setStyleSheet(self._outline_btn_style("#555"))
        rebuild_btn.clicked.connect(self._ask_rebuild_db)
        v.addWidget(rebuild_btn)

        return panel

    def _make_chat_panel(self):
        panel = QWidget(); panel.setStyleSheet("background:#B2C7A5;")
        v = QVBoxLayout(panel); v.setContentsMargins(0,0,0,0); v.setSpacing(0)

        # 헤더
        hdr = QWidget(); hdr.setFixedHeight(50)
        hdr.setStyleSheet("background:#FEE500;border-bottom:1px solid #E0CE00;")
        hl = QHBoxLayout(hdr); hl.setContentsMargins(16,0,16,0)
        hl.addWidget(QLabel("🤖  RAG 문서 챗봇",
            styleSheet="font-size:15px;font-weight:bold;color:#111;"))
        clr_btn = QPushButton("대화 초기화")
        clr_btn.setCursor(Qt.PointingHandCursor)
        clr_btn.setStyleSheet("""
            QPushButton{background:transparent;border:1px solid #888;
                border-radius:5px;padding:4px 10px;font-size:11px;color:#444;}
            QPushButton:hover{background:rgba(0,0,0,.08);}""")
        clr_btn.clicked.connect(self._clear_chat)
        hl.addStretch(); hl.addWidget(clr_btn)
        v.addWidget(hdr)

        # 채팅 스크롤
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea{border:none;background:transparent;}")
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.chat_widget = QWidget(); self.chat_widget.setStyleSheet("background:transparent;")
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.setContentsMargins(4,14,4,14)
        self.chat_layout.setSpacing(4)
        self.chat_layout.addStretch()
        self.scroll.setWidget(self.chat_widget)
        v.addWidget(self.scroll, stretch=1)

        # 입력창
        inp_bar = QWidget(); inp_bar.setFixedHeight(62)
        inp_bar.setStyleSheet("background:#F0F0F0;border-top:1px solid #CCC;")
        il = QHBoxLayout(inp_bar); il.setContentsMargins(12,11,12,11); il.setSpacing(8)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("메시지를 입력하세요...")
        self.input_box.setStyleSheet("""QLineEdit{border:1px solid #CCC;border-radius:20px;
            padding:8px 18px;font-size:13px;background:white;}
            QLineEdit:focus{border-color:#FEE500;}""")
        self.input_box.returnPressed.connect(self._send)
        il.addWidget(self.input_box)

        self.send_btn = QPushButton("전송")
        self.send_btn.setFixedSize(64,38); self.send_btn.setCursor(Qt.PointingHandCursor)
        self.send_btn.setStyleSheet("""
            QPushButton{background:#FEE500;border:none;border-radius:19px;
                font-size:13px;font-weight:bold;color:#111;}
            QPushButton:hover{background:#FFD900;}
            QPushButton:pressed{background:#F5C800;}
            QPushButton:disabled{background:#CCC;color:#888;}""")
        self.send_btn.clicked.connect(self._send)
        il.addWidget(self.send_btn)
        v.addWidget(inp_bar)
        return panel

    # ── 스타일 헬퍼 ──────────────────────────────────────────────────────────
    @staticmethod
    def _btn_style(bg, hov, press):
        return f"""QPushButton{{background:{bg};border:none;border-radius:7px;
            padding:8px;font-size:13px;font-weight:bold;color:#111;}}
            QPushButton:hover{{background:{hov};}}
            QPushButton:pressed{{background:{press};}}"""

    @staticmethod
    def _outline_btn_style(color="#444"):
        return f"""QPushButton{{background:transparent;border:1px solid #BBB;
            border-radius:6px;padding:6px 8px;font-size:11px;color:{color};}}
            QPushButton:hover{{background:rgba(0,0,0,.07);}}
            QPushButton:disabled{{color:#BBB;border-color:#DDD;}}"""

    @staticmethod
    def _hsep():
        sep = QFrame(); sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color:#CCC;"); return sep

    # ── 리스트 헬퍼 ──────────────────────────────────────────────────────────
    def _make_item(self, name: str, status: str) -> QListWidgetItem:
        icon = _ICON.get(status, "📄")
        item = QListWidgetItem(f"{icon}  {name}")
        item.setData(Qt.UserRole, name)       # 파일명 저장
        item.setToolTip(f"상태: {status}")
        return item

    def _list_add(self, name: str, status: str):
        base = Path(name).name
        for i in range(self.file_list.count()):
            if self.file_list.item(i).data(Qt.UserRole) == base:
                return                         # 이미 있음
        item = self._make_item(base, status)
        if self._delete_mode:
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
        self.file_list.addItem(item)

    def _list_update(self, name: str, status: str):
        base = Path(name).name
        icon = _ICON.get(status, "📄")
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            if item.data(Qt.UserRole) == base:
                item.setText(f"{icon}  {base}")
                item.setToolTip(f"상태: {status}")
                return
        self.file_list.addItem(self._make_item(base, status))

    # ── 자동 인제스트 ─────────────────────────────────────────────────────────
    def _auto_ingest_on_start(self):
        self.status_lbl.setText("DB 상태 확인 중…")
        QApplication.processEvents()

        db_sources = _get_db_sources()
        for name in sorted(db_sources):
            self._list_add(name, "DB 등록됨")

        to_ingest = [
            f for f in sorted(DOCUMENTS_DIR.iterdir())
            if f.suffix.lower() in ALLOWED_EXT and f.name not in db_sources
        ] if DOCUMENTS_DIR.exists() else []

        if not to_ingest:
            self.status_lbl.setText(
                "✅ 모든 문서 DB 등록 완료" if db_sources else "documents/ 폴더가 비어 있습니다."
            )
            return

        self.status_lbl.setText(f"문서 {len(to_ingest)}개 로딩 중…")
        for path in to_ingest:
            self._list_add(path.name, "로딩 중…")
            self._run_ingest_proc(path)

    # ── QProcess 인제스트 ─────────────────────────────────────────────────────
    def _run_ingest_proc(self, file_path: Path):
        proc = QProcess(self)
        proc.setProperty("_fn", file_path.name)

        def on_finish(code, _):
            name = proc.property("_fn")
            out  = bytes(proc.readAllStandardOutput()).decode("utf-8","replace").strip()
            err  = bytes(proc.readAllStandardError()).decode("utf-8","replace").strip()
            if code == 0 and out.startswith("OK:"):
                self._list_update(name, "DB 등록됨")
                self.status_lbl.setText(f"✅ {name} 저장 완료")
            else:
                msg = out[4:] if out.startswith("ERR:") else (err or out or "알 수 없는 오류")
                self._list_update(name, "오류")
                self.status_lbl.setText(f"❌ {name}: {msg[:80]}")
            self._procs.discard(proc); proc.deleteLater()

        proc.finished.connect(on_finish)
        proc.start(sys.executable, [str(BASE_DIR / "_ingest_worker.py"), str(file_path)])
        self._procs.add(proc)

    # ── 파일 추가 ─────────────────────────────────────────────────────────────
    def _open_picker(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "문서 파일 선택", str(Path.home()),
            "문서 파일 (*.pdf *.txt *.md);;PDF (*.pdf);;텍스트 (*.txt *.md)")
        if paths: self._handle_files(paths)

    def _handle_files(self, paths: list):
        for p in paths:
            src = Path(p)
            if src.suffix.lower() not in ALLOWED_EXT: continue
            dest = DOCUMENTS_DIR / src.name
            shutil.copy2(src, dest)
            self._list_add(dest.name, "로딩 중…")
            self.status_lbl.setText(f"처리 중: {dest.name}")
            self._run_ingest_proc(dest)

    # ── 삭제 모드 ─────────────────────────────────────────────────────────────
    def _enter_delete_mode(self):
        self._delete_mode = True
        self._all_selected = False
        self.del_mode_btn.setVisible(False)
        self._del_btn_row_widget.setVisible(True)
        self.confirm_del_btn.setVisible(True)
        self.select_all_btn.setText("전체선택")
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)

    def _exit_delete_mode(self):
        self._delete_mode = False
        self._all_selected = False
        self.del_mode_btn.setVisible(True)
        self._del_btn_row_widget.setVisible(False)
        self.confirm_del_btn.setVisible(False)
        model = self.file_list.model()
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            item.setFlags(item.flags() & ~Qt.ItemIsUserCheckable)
            model.setData(self.file_list.indexFromItem(item), None, Qt.CheckStateRole)

    def _toggle_select_all(self):
        self._all_selected = not self._all_selected
        state = Qt.Checked if self._all_selected else Qt.Unchecked
        for i in range(self.file_list.count()):
            self.file_list.item(i).setCheckState(state)
        self.select_all_btn.setText("전체해제" if self._all_selected else "전체선택")

    def _confirm_delete(self):
        selected = [
            self.file_list.item(i).data(Qt.UserRole)
            for i in range(self.file_list.count())
            if self.file_list.item(i).checkState() == Qt.Checked
        ]
        if not selected:
            self.status_lbl.setText("삭제할 문서를 선택해 주세요.")
            return

        names_text = "\n".join(f"  • {n}" for n in selected)
        box = QMessageBox(self)
        box.setWindowTitle("문서 삭제 확인")
        box.setIcon(QMessageBox.Warning)
        box.setText(
            f"선택한 {len(selected)}개 문서를 삭제합니다.\n\n"
            f"{names_text}\n\n"
            "⚠️  삭제 후 DB 초기화 및 재생성을 진행합니다.\n"
            "계속하시겠습니까?"
        )
        yes = box.addButton("예", QMessageBox.YesRole)
        box.addButton("아니오", QMessageBox.NoRole)
        box.setDefaultButton(yes)
        box.exec_()

        if box.clickedButton() is not yes:
            return

        # 파일 삭제 + 리스트에서 해당 항목만 제거
        for name in selected:
            p = DOCUMENTS_DIR / name
            if p.exists(): p.unlink()

        self._exit_delete_mode()

        # 삭제된 항목만 리스트에서 제거 (나머지는 유지)
        for name in selected:
            for i in range(self.file_list.count() - 1, -1, -1):
                if self.file_list.item(i).data(Qt.UserRole) == name:
                    self.file_list.takeItem(i)
                    break

        self._start_rebuild_db()

    # ── DB 재생성 ─────────────────────────────────────────────────────────────
    def _ask_rebuild_db(self):
        box = QMessageBox(self)
        box.setWindowTitle("DB 초기화 확인")
        box.setIcon(QMessageBox.Question)
        box.setText(
            "documents/ 폴더의 모든 문서를 다시 읽어\n"
            "벡터 DB를 초기화 후 재생성합니다.\n\n"
            "계속하시겠습니까?"
        )
        yes = box.addButton("예", QMessageBox.YesRole)
        box.addButton("아니오", QMessageBox.NoRole)
        box.setDefaultButton(yes)
        box.exec_()
        if box.clickedButton() is yes:
            self._start_rebuild_db()

    def _start_rebuild_db(self):
        self.status_lbl.setText("DB 초기화 중…")
        self._rag_busy = True
        self.send_btn.setEnabled(False)
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            name = item.data(Qt.UserRole)
            item.setText(f"⏳  {name}")
            item.setToolTip("상태: DB 재생성 중")
        QApplication.processEvents()

        proc = QProcess(self)
        proc.readyReadStandardOutput.connect(lambda: self._on_rebuild_out(proc))
        proc.finished.connect(lambda code, _: self._on_rebuild_done(proc, code))
        proc.start(sys.executable, [str(BASE_DIR / "_rebuild_db.py")])
        self._rebuild_proc = proc

    def _on_rebuild_out(self, proc):
        out = bytes(proc.readAllStandardOutput()).decode("utf-8", "replace")
        for line in out.splitlines():
            line = line.strip()
            if line == "DB_CLEARED":
                self.status_lbl.setText("DB 초기화 완료 — 재생성 중…")
            elif line.startswith("FILE_DONE:"):
                parts = line.split(":", 2)
                if len(parts) >= 3:
                    self.status_lbl.setText(f"처리 중: {parts[1]} ({parts[2]}청크)")
            elif line.startswith("FILE_ERR:"):
                parts = line.split(":", 2)
                if len(parts) >= 2:
                    self.status_lbl.setText(f"❌ 오류: {parts[1][:40]}")

    def _on_rebuild_done(self, proc, code):
        err = bytes(proc.readAllStandardError()).decode("utf-8", "replace").strip()
        proc.deleteLater()
        if code == 0:
            self.status_lbl.setText("DB 갱신 중…")
            def _reinit():
                global _vector_db
                try:
                    _vector_db = Chroma(
                        persist_directory=PERSIST_DIRECTORY,
                        embedding_function=_embeddings,
                        collection_name=COLLECTION_NAME,
                    )
                    _rebuild_bridge.done.emit()
                except Exception as e:
                    _rebuild_bridge.failed.emit(f"❌ DB 갱신 실패: {e}")
            threading.Thread(target=_reinit, daemon=True).start()
        else:
            msg = err.splitlines()[-1] if err else "알 수 없는 오류"
            self.status_lbl.setText(f"❌ DB 재생성 오류: {msg[:80]}")
            self._rag_busy = False
            self.send_btn.setEnabled(True)

    def _on_db_refreshed(self):
        db_sources = _get_db_sources()
        self.file_list.clear()
        for name in sorted(db_sources):
            self._list_add(name, "DB 등록됨")
        count = len(db_sources)
        self.status_lbl.setText(
            f"✅ DB 재생성 완료 ({count}개 문서)" if count else "documents/ 폴더가 비어 있습니다."
        )
        self._rag_busy = False
        self.send_btn.setEnabled(True)

    # ── 채팅 ─────────────────────────────────────────────────────────────────
    def _send(self):
        text = self.input_box.text().strip()
        if not text or self._rag_busy: return

        self._rag_busy = True
        self.input_box.clear()
        self.send_btn.setEnabled(False)
        self.input_box.setEnabled(False)
        self._add_bubble(text, is_user=True)
        self._add_bubble("답변을 생성하고 있습니다…", is_user=False, loading=True)

        self._last_question = text
        q = text
        def _w():
            try:
                a, s = _run_rag(q); _rag_bridge.done.emit(a, s)
            except Exception as e:
                _rag_bridge.failed.emit(str(e))
        threading.Thread(target=_w, daemon=True).start()

    def _on_rag_done(self, answer, sources):
        self._remove_loading()
        msg = answer + (f"\n\n📎 참고: {', '.join(sources)}" if sources else "")
        self._add_bubble(msg, is_user=False)
        _save_chat_log(self._last_question, answer)
        self._rag_busy = False
        self.send_btn.setEnabled(True)
        self.input_box.setEnabled(True)
        self.input_box.setFocus()

    def _on_rag_failed(self, err):
        self._remove_loading()
        self._add_bubble(f"오류: {err}", is_user=False)
        self._rag_busy = False
        self.send_btn.setEnabled(True)
        self.input_box.setEnabled(True)

    def _add_bubble(self, text, *, is_user, loading=False):
        b = Bubble(text, is_user, datetime.now().strftime("%H:%M"))
        if loading: b.setObjectName("__loading__")
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, b)
        QTimer.singleShot(30, lambda: self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()))

    def _remove_loading(self):
        for i in range(self.chat_layout.count()):
            it = self.chat_layout.itemAt(i)
            if it and it.widget() and it.widget().objectName() == "__loading__":
                w = it.widget()
                self.chat_layout.removeWidget(w); w.deleteLater(); return

    def _clear_chat(self):
        while self.chat_layout.count() > 1:
            it = self.chat_layout.takeAt(0)
            if it.widget(): it.widget().deleteLater()


# ── 진입점 ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("맑은 고딕", 10))
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
