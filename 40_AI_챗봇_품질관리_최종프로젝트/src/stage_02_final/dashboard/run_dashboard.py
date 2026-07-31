import sys
from pathlib import Path

from streamlit.web import cli as stcli

if __name__ == "__main__":
    app_path = Path(__file__).resolve().parent / "streamlit_app.py"
    sys.argv = ["streamlit", "run", str(app_path)]
    sys.exit(stcli.main())
