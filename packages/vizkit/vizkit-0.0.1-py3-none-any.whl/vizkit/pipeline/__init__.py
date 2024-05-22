from typing import TYPE_CHECKING, Optional
import pandas as pd
import streamlit as st
from vizkit.pipeline.data_source import DATA_SOURCE
from vizkit.pipeline.utils import is_ci_column

# from streamlit_tree_select import tree_select

if TYPE_CHECKING:
    from .blocks import Block


class Pipeline:
    project: str | None
    """The selected project name"""

    inputs: list[str]
    """List of runids or firebase ids"""

    blocks: list["Block"]
    """List of blocks to be executed in order"""

    final_add_block: "Block"
    """Add block at the end of the pipeline"""

    def __init__(self, inputs: list[str], project: str | None) -> None:
        from .blocks import AddBlock, Block

        self.project = project
        self.inputs = inputs
        self.blocks = Block.create_initial_blocks()
        self.final_add_block = AddBlock(pipeline=self)

    def serialize_and_encode(self) -> str:
        from .serialize import serialize_and_encode

        return serialize_and_encode(self)

    @staticmethod
    def decode_and_deserialize(pipeline_compressed_base64: str) -> "Pipeline":
        from .serialize import decode_and_deserialize

        return decode_and_deserialize(pipeline_compressed_base64)

    @staticmethod
    def load_from_short_id(short_id: str) -> Optional["Pipeline"]:
        px = DATA_SOURCE.get_inflated_link(short_id)
        return Pipeline.decode_and_deserialize(px) if px else None

    def __block_controls(self, i: int, block: "Block"):
        from vizkit.web.components.block_controls import block_controls
        from .blocks import AddBlock

        if block.is_fixed_block():
            return

        match block_controls(key=f"{block.id}-block_controls"):
            case "add":
                self.blocks.insert(i, AddBlock(pipeline=self))
                st.rerun()
            case "delete":
                self.blocks = [b for b in self.blocks if b.id != block.id]
                st.rerun()
            case _:
                ...

    def __block_header(self, i: int | None, block: "Block"):
        st.subheader(f":red-background[{block.title}]")

    def __load_and_cache_data(self):
        if len(self.inputs) == 0:
            return pd.DataFrame()
        with st.sidebar:
            with st.spinner("Loading ..."):
                data = DATA_SOURCE.load_data_file_cached(self.inputs[0])
        return data.results

    def process(self):
        from .blocks import GraphBlock

        DATA_SOURCE.render_data_source_block(self)

        with st.sidebar:
            st.divider()

        data = self.__load_and_cache_data()
        original_data = data

        add_block = self.final_add_block
        graph_blocks: list[tuple[GraphBlock, pd.DataFrame]] = []
        # Pipeline
        with st.sidebar:
            for i, block in enumerate(self.blocks):
                # Block content
                self.__block_controls(i, block)
                with st.container(border=True):
                    self.__block_header(i, block)
                    # Block Content: rendered by `Block.__call__`
                    data = block(data)
                    if isinstance(block, GraphBlock):
                        graph_blocks.append((block, data))
            with st.container(border=True):
                self.__block_header(None, add_block)
                data = add_block(data)
        # Graphs
        for block, df in graph_blocks:
            block.plot(df)
        # Table
        ci_cols = [c for c in data.columns if is_ci_column(c)]
        data_without_ci = data.drop(columns=ci_cols, errors="ignore")
        st.dataframe(data_without_ci, use_container_width=True)
        if ci_cols:
            with st.expander("Raw Data with CI", expanded=False):
                st.dataframe(data, use_container_width=True)
        with st.expander("Original Data", expanded=False):
            st.dataframe(original_data, use_container_width=True)
