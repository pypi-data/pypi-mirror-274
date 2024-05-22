from dataclasses import dataclass
import os
from pathlib import Path
import sqlite3
from typing import TYPE_CHECKING
import pandas as pd
import toml
import streamlit as st
from . import DataSource, DataFiles, DataFile, DataFileMeta


if TYPE_CHECKING:
    from .. import Pipeline


class LocalDataSource(DataSource):
    path: Path

    results: dict[str, Path]
    """
    Can be .csv files or directories containing a config.toml and results.csv
    """

    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path
        self.results = {}
        self.cache_file = Path(os.curdir) / ".cache" / "vizkit-share-links.db"
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        db_exists = self.cache_file.exists()
        if not db_exists:
            with sqlite3.connect(self.cache_file) as con:
                con.execute(
                    "CREATE TABLE share_links (id TEXT PRIMARY KEY, inflated TEXT);"
                )

    @property
    def is_local(self) -> bool:
        return True

    def get_inflated_link(self, key: str) -> str | None:
        with sqlite3.connect(self.cache_file) as con:
            c = con.cursor()
            res = c.execute("SELECT inflated FROM share_links WHERE id = ?;", (key,))
            row = res.fetchone()
            if row is None:
                return None
            return row[0]

    def insert_inflated_link(self, inflated: str) -> str:
        with sqlite3.connect(self.cache_file) as con:
            c = con.cursor()
            # If the inflated pipeline already exists, return the key
            res = c.execute(
                "SELECT id FROM share_links WHERE inflated = ?;", (inflated,)
            )
            row = res.fetchone()
            if row is not None:
                return row[0]
            while True:
                # We use shortuuid to generate a key instead of sql-generated key, so it looks consistent with the firebase implementation.
                key = self._generate_share_link_key()
                # Check if key already exists
                res = c.execute("SELECT id FROM share_links WHERE id = ?;", (key,))
                if res.fetchone() is None:
                    break
            c.execute(
                "INSERT INTO share_links (id, inflated) VALUES (?, ?);", (key, inflated)
            )
            c.close()
        return key

    def __refresh(self):
        if not self.path.exists() or not self.path.is_dir():
            self.results = {}
        # For a rust crate: list all log directories
        logs = []
        if (self.path / "Cargo.toml").exists():
            logs_dir = self.path / "target" / "harness" / "logs"
            for d in logs_dir.iterdir():
                if d.name == "latest" or not d.is_dir():
                    continue
                if (d / "config.toml").exists() and (d / "results.csv").exists():
                    logs.append(d.resolve())
        # list all csv files
        logs_csvs = set([d / "results.csv" for d in logs])
        csvs = [p for p in self.path.glob("*.csv") if p not in logs_csvs]
        # construct map
        results = {}
        for log in logs:
            results[log.name] = log
        for csv in csvs:
            results[csv.name] = csv
        self.results = results

    def list_data_files(self) -> DataFiles:
        self.__refresh()
        return DataFiles(runids=list(self.results.keys()))

    def load_data_file(self, id: str) -> DataFile:
        self.__refresh()
        path = self.results[id]
        if path.suffix == ".csv":
            return DataFile(
                results=pd.read_csv(path),
                config={},
                meta=DataFileMeta(runid=path.name),
            )
        config = toml.load(path / "config.toml")
        runid = config.get("runid", id)
        return DataFile(
            results=pd.read_csv(path / "results.csv"),
            config=config,
            meta=DataFileMeta(
                runid=runid,
                project=config.get("project"),
                profile=config["profile"]["name"],
            ),
        )

    def render_data_source_block(self, pipeline: "Pipeline"):
        data_ids = self.list_data_files().runids

        with st.sidebar:
            # Data Source selector
            input = pipeline.inputs[0] if len(pipeline.inputs) > 0 else None
            index = data_ids.index(input) if input in data_ids else None
            selected_data = st.sidebar.selectbox("Data Source", data_ids, index=index)
            if selected_data:
                pipeline.inputs = [selected_data]
            # Share button
            self._render_share_button(pipeline)
