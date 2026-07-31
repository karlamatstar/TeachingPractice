import json
import subprocess
import venv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
REQUIREMENTS_FILE = BASE_DIR / "requirements.txt"
VENV_DIR = BASE_DIR / ".venv"
VENV_PYTHON = VENV_DIR / "Scripts" / "python.exe"
VSCODE_SETTINGS_FILE = BASE_DIR / ".vscode" / "settings.json"


def create_venv_if_missing() -> None:
    if VENV_PYTHON.exists():
        print(f"가상환경 이미 존재: {VENV_DIR}")
        return
    print(f"가상환경 생성 중: {VENV_DIR}")
    venv.create(VENV_DIR, with_pip=True)


def install_requirements() -> None:
    subprocess.run(
        [str(VENV_PYTHON), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)],
        check=True,
    )


def set_vscode_interpreter() -> None:
    VSCODE_SETTINGS_FILE.parent.mkdir(exist_ok=True)
    settings = {}
    if VSCODE_SETTINGS_FILE.exists():
        settings = json.loads(VSCODE_SETTINGS_FILE.read_text(encoding="utf-8"))
    settings["python.defaultInterpreterPath"] = "${workspaceFolder}/.venv/Scripts/python.exe"
    VSCODE_SETTINGS_FILE.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    create_venv_if_missing()
    install_requirements()
    set_vscode_interpreter()
    print(f"\n완료. VS Code 인터프리터가 다음 경로로 설정되었습니다: {VENV_PYTHON}")
    print("VS Code(Antigravity)를 재시작하거나 창을 다시 로드하면 자동으로 이 가상환경을 사용합니다.")
