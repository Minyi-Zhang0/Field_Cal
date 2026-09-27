import os
import sys

os.environ["STREAMLIT_GLOBAL_DEVELOPMENT_MODE"] = "false"
from streamlit.web import cli as stcli


def main():
    if getattr(sys, "frozen", False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    app_path = os.path.join(base_dir, "st_app.py")

    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--server.headless=false",
        "--server.address=127.0.0.1",
        # "--server.port=8501",
        "--browser.gatherUsageStats=false",
    ]

    sys.exit(stcli.main())


if __name__ == "__main__":
    main()