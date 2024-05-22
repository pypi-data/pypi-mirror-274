import base64
from dataclasses import asdict
import json
import zlib
import streamlit as st

from vizkit.pipeline import Pipeline
from .blocks import Block, AddBlock, ALL_BLOCKS


def serialize_and_encode(pipeline: Pipeline) -> str:
    # Serialize to an json string
    if len(pipeline.inputs) > 0:
        blocks = [asdict(b) for b in pipeline.blocks if not isinstance(b, AddBlock)]
    else:
        initial_blocks = Block.create_initial_blocks()
        blocks = [asdict(b) for b in initial_blocks if not isinstance(b, AddBlock)]
    for b in blocks:
        del b["id"]
        del b["title"]
    pipeline_json = {
        "project": pipeline.project,
        "inputs": pipeline.inputs,
        "blocks": blocks,
    }
    pipeline_json_str = json.dumps(pipeline_json, separators=(",", ":"))
    # Compress the string
    pipeline_bytes = pipeline_json_str.encode("utf-8")
    pipeline_compressed = zlib.compress(pipeline_bytes, level=9)
    # convert to base64
    pipeline_compressed_base64 = base64.urlsafe_b64encode(pipeline_compressed).decode(
        "utf-8"
    )
    # print(
    #     f"{len(pipeline_bytes)} -> {len(pipeline_compressed)} -> {len(pipeline_compressed_base64)}"
    # )
    return pipeline_compressed_base64


def __dict_to_block(d: dict) -> Block | None:
    if d["type"] not in ALL_BLOCKS:
        return None
    BlockType = ALL_BLOCKS[d["type"]]
    try:
        block = BlockType(**d)
    except TypeError:
        st.error(f"Failed to deserialize block: {d}")
        return None
    return block


def decode_and_deserialize(pipeline_compressed_base64: str) -> "Pipeline":
    pipeline = Pipeline(inputs=[], project=None)
    # Decode from base64
    pipeline_compressed = base64.urlsafe_b64decode(
        pipeline_compressed_base64 + "=" * (-len(pipeline_compressed_base64) % 4)
    )
    pipeline_bytes = zlib.decompress(pipeline_compressed)
    pipeline_json_str = pipeline_bytes.decode("utf-8")
    # Deserialize
    pipeline_json = json.loads(pipeline_json_str)
    pipeline.inputs = pipeline_json["inputs"]
    pipeline.project = pipeline_json.get("project")
    deserialzied_blocks = [__dict_to_block(b) for b in pipeline_json["blocks"]]
    pipeline.blocks = [b for b in deserialzied_blocks if b is not None]
    return pipeline
