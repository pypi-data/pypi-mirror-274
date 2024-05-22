from typing import TYPE_CHECKING
import streamlit as st

from vizkit.pipeline.data_source.firebase import fb_utils
from .. import DataSource, DataFiles, DataFile, DataFileMeta
from . import auth


if TYPE_CHECKING:
    from .. import Pipeline


class FirebaseDataSource(DataSource):
    @property
    def is_local(self) -> bool:
        return False

    def __init__(self) -> None:
        super().__init__()

    def get_inflated_link(self, key: str) -> str | None:
        return fb_utils.get_inflated_id(key)

    def insert_inflated_link(self, inflated: str) -> str:
        return fb_utils.insert_inflated_id(inflated, self._generate_share_link_key)

    def list_user_data_files(self) -> DataFiles | None:
        if user := auth.get_user():
            metas = fb_utils.get_owned_data_files(user.uid)
            projects: dict[str, list[DataFileMeta]] = {}
            for m in metas:
                assert m.project is not None
                projects.setdefault(m.project, []).append(m)
            return DataFiles(projects=projects)
        else:
            return None

    def get_data_file_meta(self, id: str) -> DataFileMeta:
        return fb_utils.get_data_file_meta(id)

    def load_data_file(self, id: str) -> DataFile:
        return fb_utils.get_data_file(id)

    def __get_owner_info(self, meta: DataFileMeta | None) -> str | None:
        if meta and meta.owner is not None:
            owner_info = f"Owner: {fb_utils.get_user_name_by_uid(meta.owner)}"
            user = auth.get_user()
            if user and user.uid == meta.owner:
                owner_info += " (You)"
            return owner_info
        elif meta:
            return "This data file is not owned by anyone"
        else:
            return None

    def __get_projects(
        self,
        data_files: DataFiles,
        curr_file: DataFileMeta | None,
        curr_proj: str | None,
    ) -> tuple[list[str], int | None]:
        projects = list(data_files.projects.keys())
        # If this is an unclaimed data file, add the project to the list, and select this one by default
        if curr_file and (not curr_file.owner or curr_file.project not in projects):
            assert curr_file.project is not None
            projects.append(curr_file.project)
            curr_proj = curr_file.project
        index = projects.index(curr_proj) if curr_proj in projects else None
        return projects, index

    def __get_files_for_project(
        self,
        project: str | None,
        data_files: DataFiles,
        selected: DataFileMeta | None,
    ) -> tuple[list[DataFileMeta], int | None]:
        if not project:
            return [], None
        files: list[DataFileMeta] = []
        index = None
        # Add all files in the project
        for m in data_files.projects.get(project, []):
            files.append(m)
            if selected and selected.sha256 == m.sha256:
                index = len(files) - 1
        # Add the unclaimed data file
        user = auth.get_user()
        uid = user.uid if user else None
        if selected and (
            not selected.owner or (selected.owner != uid and selected not in files)
        ):
            files.append(selected)
            index = len(files) - 1
        return files, index

    def render_data_source_block(self, pipeline: "Pipeline"):
        with st.spinner("Loading ..."):
            if "user_data_files" in st.session_state:
                data_files = st.session_state["user_data_files"]
            else:
                data_files = self.list_user_data_files()
                if data_files is not None:
                    st.session_state["user_data_files"] = data_files
                data_files = data_files or DataFiles()
        user = auth.get_user()
        curr_data_file = (
            self.get_data_file_meta(pipeline.inputs[0])
            if len(pipeline.inputs) > 0
            else None
        )
        curr_data_file_is_claimed = curr_data_file and curr_data_file.owner is not None
        with st.sidebar:
            owner_info = self.__get_owner_info(curr_data_file)
            # 1. Project selector
            projects, index = self.__get_projects(
                data_files, curr_data_file, pipeline.project
            )
            pipeline.project = st.selectbox(
                "Project", projects, index=index, help=owner_info
            )
            # 2. Data file selector
            files, index = self.__get_files_for_project(
                pipeline.project, data_files, curr_data_file
            )
            selected = st.selectbox(
                "Data Source",
                files,
                index=index,
                format_func=lambda x: x.runid,
                help=owner_info,
            )
            if selected:
                assert selected.sha256
                pipeline.inputs = [selected.sha256]

            # Claim and Login buttons
            if curr_data_file:
                if curr_data_file.owner is not None:
                    if user is None:
                        auth.google_login_button("🔒 Login to share pipeline")
                else:
                    if user is not None:
                        if st.button("✅ Claim Ownership", use_container_width=True):
                            fb_utils.claim_data_file(pipeline.inputs[0], user.uid)
                            st.rerun()
                    else:
                        auth.google_login_button("🔒 Login to claim ownership")
            else:
                if user is None:
                    auth.google_login_button("🔒 Login to get your pipelines")

            # Share button
            if curr_data_file_is_claimed and user is not None:
                self._render_share_button(pipeline)

            # Logout button
            if user is not None:
                if st.button("⎋ Logout", use_container_width=True):
                    auth.logout()
                    st.rerun()
