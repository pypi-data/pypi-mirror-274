from pathlib import Path
import sys, os
import streamlit.web.cli as stcli
import dotenv

from vizkit import Options

_WEB_DIR = Path(__file__).parent / "web"


def inject_api():
    from vizkit.pipeline.data_source import DATA_SOURCE

    if not DATA_SOURCE.is_local:
        from vizkit.api.api import inject_api

        inject_api()


def main():
    dotenv.load_dotenv()
    options = Options.parse()
    sys.argv = [
        "streamlit",
        "run",
        *(["--server.headless", "true"] if not options.open else []),
        "--server.port",
        str(options.port),
        str(_WEB_DIR / "plot.py"),
    ]
    os.environ["PYTHONPATH"] = os.curdir
    inject_api()
    sys.exit(stcli.main())
