from dataclasses import dataclass

from vizkit.pipeline.data_source import DataFileMeta
from ..api import api, RequestHandler
import io
from zipfile import ZipFile
import pandas as pd
import toml
from tornado.httputil import HTTPFile
import hashlib
import vizkit.pipeline.data_source.firebase.fb_utils as fb_utils
import threading
import time


@api("/api/v1/version")
class HelloWorldHandler(RequestHandler):
    def get(self):
        self.write({"api_version": 1})


@dataclass
class ReportFiles:
    results: str
    config: str

    meta: DataFileMeta | None

    @staticmethod
    def from_http_files(files: list[HTTPFile]):
        if not sorted([f.filename for f in files]) == sorted(
            ["results.csv", "config.toml"]
        ):
            raise ValueError("Invalid files")
        results_file = next((f for f in files if f.filename == "results.csv"), None)
        config_file = next((f for f in files if f.filename == "config.toml"), None)
        if not results_file or not config_file:
            raise ValueError("Invalid files")
        report_files = ReportFiles(
            results=results_file.body.decode("utf-8"),
            config=config_file.body.decode("utf-8"),
            meta=None,
        )
        report_files.__validate_and_fix_meta()
        return report_files

    def __format_files(self, results: pd.DataFrame, config: dict):
        self.results = results.to_csv(index=False)
        self.config = toml.dumps(config)

    def __validate_and_fix_meta(self):
        # try parse csv
        df = pd.read_csv(io.StringIO(self.results))
        # try parse toml
        self.meta = DataFileMeta(sha256="", runid="")
        config = toml.loads(self.config)
        self.__format_files(results=df, config=config)
        if "runid" not in config or not isinstance(config["runid"], str):
            raise ValueError("Invalid config")
        self.meta.runid = config["runid"]
        if (
            "profile" not in config
            or not isinstance(config["profile"], dict)
            or not isinstance(config["profile"].get("name"), str)
        ):
            raise ValueError("Invalid config")
        self.meta.profile = config["profile"]["name"]
        if "project" not in config or not isinstance(config["project"], str):
            raise ValueError("Invalid config")
        self.meta.project = config["project"]
        self.meta.sha256 = self.sha256()
        if (
            "commit" not in config
            or not isinstance(config["commit"], str)
            or config["commit"].endswith("-dirty")
        ):
            raise ValueError("Invalid config")

    def sha256(self):
        sha256 = hashlib.sha256()
        sha256.update(self.results.encode("utf-8"))
        sha256.update(self.config.encode("utf-8"))
        return sha256.hexdigest()

    def zip(self):
        file_body = io.BytesIO()
        with ZipFile(file_body, "w") as zip:
            zip.writestr("results.csv", self.results)
            zip.writestr("config.toml", self.config)
        return file_body.getvalue()


_LAST_UPLOAD_TIME = 0
_UPLOAD_API_RATE_LIMIT = 5  # seconds


@api("/api/v1/upload-results")
class ReportUploadHandler(RequestHandler):
    def __post_impl(self):
        # Read uploaded files
        try:
            if "files" not in self.request.files:
                raise ValueError("Invalid files")
            uploaded_files = self.request.files["files"]
            report_files = ReportFiles.from_http_files(uploaded_files)
        except Exception as e:
            self.set_status(400)
            self.write({"error": "Invalid files"})
            return
        # Zip and upload to firebase
        try:
            sha256 = report_files.sha256()
            zipped = report_files.zip()
            assert report_files.meta
            url, new_blob = fb_utils.upload_file(
                zipped, name=f"results/{sha256}.zip", meta=report_files.meta
            )
            if not new_blob:
                self.set_status(200)
                self.write({"status": "already exists", "url": url, "hash": sha256})
            else:
                self.set_status(201)
                self.write({"status": "created", "url": url, "hash": sha256})
        except Exception as e:
            print(e)
            self.set_status(500)
            self.write({"error": "Failed to upload files"})
            return

    def put(self):
        with threading.Lock():
            global _LAST_UPLOAD_TIME
            # sleep if less than 5 seconds since last upload
            if time.time() - _LAST_UPLOAD_TIME < _UPLOAD_API_RATE_LIMIT:
                time.sleep(_UPLOAD_API_RATE_LIMIT - (time.time() - _LAST_UPLOAD_TIME))
            self.__post_impl()
            _LAST_UPLOAD_TIME = time.time()

    def check_xsrf_cookie(self) -> None:
        return None
