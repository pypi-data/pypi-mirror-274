import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import os

_CACHED_OPTIONS: Any = None


@dataclass
class Options:
    path: Path | None
    firebase: bool
    port: int
    open: bool

    @property
    def domain(self) -> str:
        d = os.environ.get("DOMAIN", f"http://localhost:{self.port}")
        while d.endswith("/"):
            d = d[:-1]
        return d

    def validate(self):
        if self.path:
            assert self.path.is_dir(), f"{self.path} is not a directory"
            self.path = self.path.resolve()
        if self.firebase:
            assert not self.path, "Cannot use --firebase with a path"

    @staticmethod
    def get() -> "Options":
        return _CACHED_OPTIONS

    @staticmethod
    def parse():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "path",
            nargs="?",
            help="path to the logs directory. default to the current directory",
        )
        parser.add_argument(
            "--firebase",
            action="store_true",
            help="fetch log files from firebase and enable auth guards",
        )
        parser.add_argument(
            "--port",
            type=int,
            default=8501,
            help="port to run the streamlit server on",
        )
        parser.add_argument(
            "--open",
            action="store_true",
            help="open the browser after starting the server",
        )
        options = parser.parse_args()
        firebase = options.firebase or False
        path = (
            Path(options.path)
            if options.path
            else (Path(".") if not firebase else None)
        )
        port = options.port
        options = Options(path=path, firebase=firebase, port=port, open=options.open)
        global _CACHED_OPTIONS
        _CACHED_OPTIONS = options
        return options
