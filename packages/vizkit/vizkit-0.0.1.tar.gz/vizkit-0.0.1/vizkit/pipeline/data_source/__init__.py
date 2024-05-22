from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TYPE_CHECKING
import pandas as pd
import shortuuid
import streamlit as st

from vizkit import Options


if TYPE_CHECKING:
    from .. import Pipeline


@dataclass
class DataFileMeta:
    runid: str

    sha256: str | None = None
    project: str | None = None
    profile: str | None = None
    owner: str | None = None

    def to_dict(self):
        values = {"sha256": self.sha256}
        if self.runid:
            values["runid"] = self.runid
        if self.project:
            values["project"] = self.project
        if self.profile:
            values["profile"] = self.profile
        if self.owner:
            values["owner"] = self.owner
        return values


@dataclass
class DataFile:
    results: pd.DataFrame
    config: Any
    meta: DataFileMeta


@dataclass
class DataFiles:
    runids: list[str] = field(default_factory=list)
    projects: dict[str, list[DataFileMeta]] = field(
        default_factory=dict
    )  # project -> runid


class DataSource:
    @property
    def is_local(self) -> bool:
        raise NotImplementedError

    def get_data_file_meta(self, id: str) -> DataFileMeta:
        """Get data file metadata"""
        raise NotImplementedError

    def load_data_file(self, id: str) -> DataFile:
        """Load data file"""
        raise NotImplementedError

    def load_data_file_cached(self, id: str) -> DataFile:
        """Load and cache data file"""
        key = "runid" if self.is_local else "sha256"
        if id not in st.session_state or st.session_state[id].meta.to_dict()[key] != id:
            st.session_state[id] = self.load_data_file(id)
        return st.session_state[id]

    def render_data_source_block(self, pipeline: "Pipeline"):
        """Show data source selection block"""
        raise NotImplementedError

    def _render_share_link_dialog(self, px: str):
        _show_share_link(px)

    def _render_share_button(self, pipeline: "Pipeline"):
        if st.button("🔗 Share Pipeline", use_container_width=True):
            self._render_share_link_dialog(px=pipeline.serialize_and_encode())

    def _generate_share_link_key(self) -> str:
        return shortuuid.ShortUUID().random(length=16)

    def get_inflated_link(self, key: str) -> str | None:
        raise NotImplementedError

    def insert_inflated_link(self, inflated: str) -> str:
        raise NotImplementedError


def create_data_source():
    options = Options.get()
    if options.firebase:
        from vizkit.pipeline.data_source.firebase import FirebaseDataSource

        return FirebaseDataSource()
    else:
        from vizkit.pipeline.data_source.local import LocalDataSource

        return LocalDataSource(path=options.path or Path("."))


DATA_SOURCE: DataSource = create_data_source()


@st.experimental_dialog("Pipeline Share Link")  # type: ignore
def _show_share_link(px: str):
    with st.spinner("Generating link..."):
        key = DATA_SOURCE.insert_inflated_link(px)
    short_link = f"{Options.get().domain}/?p={key}"
    st.markdown(f"Your [pipeline share link]({short_link}) is ready!")
    st.code(short_link)
