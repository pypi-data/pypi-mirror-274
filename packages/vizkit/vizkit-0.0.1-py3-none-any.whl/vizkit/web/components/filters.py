from typing import Literal, cast
import uuid
import streamlit as st
from .flex import flexbox
import pandas as pd

from vizkit.pipeline.utils import (
    default_index,
    default_values,
    scenario_columns,
    value_columns,
)


def scenario_filters(
    data: pd.DataFrame,
    filters: list[tuple[str, Literal["includes", "excludes"], list[str]]],
    filter_ids: list[str],
    initial_filters: dict[str, tuple[str, Literal["includes", "excludes"], list[str]]],
    key: str,
):
    """Render a list of scenario filters, and returns the latest filters."""
    scenario_cols = scenario_columns(data)
    outer_key = key
    new_filters, new_filter_ids = [], []
    for i, (col, op, values) in enumerate(filters):
        key = filter_ids[i]
        with flexbox(children_styles=["", "flex: 1", "flex: 1"]):
            if st.button("❌", key=f"{key}-remove"):
                filters.pop(i)
                filter_ids.pop(i)
                st.rerun()
            col = st.selectbox(
                "Scenario",
                scenario_cols,
                index=default_index(
                    scenario_cols, default=initial_filters.get(key, [None])[0]
                ),
                label_visibility="collapsed",
                placeholder="Scenario",
                key=f"{key}-col",
            )
            op = st.selectbox(
                "Operation",
                ["includes", "excludes"],
                index=default_index(
                    ["includes", "excludes"],
                    default=initial_filters.get(key, [None, "includes"])[1],
                ),
                label_visibility="collapsed",
                placeholder="op",
                key=f"{key}-op",
            )
        candidates: list[str] = sorted(list(set(data[col].astype(str))))
        values = st.multiselect(
            "Values",
            candidates,
            default=default_values(
                candidates,
                default=initial_filters.get(key, [None, "includes", []])[2],
            ),
            label_visibility="collapsed",
            placeholder="Values",
            key=f"{key}-values",
        )
        assert op is None or op in ["includes", "excludes"]
        op = cast(Literal["includes", "excludes"], op or "includes")
        new_filters.append((col or "", op, values))
        new_filter_ids.append(key)
        st.write("")
        st.write("")
    if st.button("Add Filter", key=f"{outer_key}-add", use_container_width=True):
        filters.append(("", "includes", []))
        filter_ids.append(uuid.uuid4().hex)
        st.rerun()
    return new_filters, new_filter_ids


def value_filters(
    data: pd.DataFrame,
    filters: list[tuple[Literal["in", "out"], float, str, float]],
    filter_ids: list[str],
    initial_filters: dict[str, tuple[Literal["in", "out"], float, str, float]],
    key: str,
):
    outer_key = key
    value_cols = value_columns(data, ci=False)
    new_filters, new_filter_ids = [], []
    for i, (col, lower, op, upper) in enumerate(filters):
        key = filter_ids[i]
        with flexbox(children_styles=["", "flex: 1"]):
            if st.button("❌", key=f"{key}-remove"):
                assert filters is not None
                filters.pop(i)
                filter_ids.pop(i)
                st.rerun()
            col = st.selectbox(
                "Column",
                value_cols,
                index=default_index(
                    value_cols, default=initial_filters.get(key, [None])[0]
                ),
                label_visibility="collapsed",
                placeholder="Column",
                key=f"{key}-col",
            )
            op = st.selectbox(
                "Operation",
                ["in", "out"],
                index=default_index(
                    ["in", "out"],
                    default=initial_filters.get(key, [None, None, "in"])[2],
                ),
                label_visibility="collapsed",
                placeholder="op",
                key=f"{key}-op",
            )
        with flexbox(children_styles=["flex: 1", "flex: 1"]):
            lower = st.number_input(
                "Lower",
                value=initial_filters.get(key, [None, 0.0, None, 0.0])[1],
                label_visibility="collapsed",
                placeholder="Lower",
                key=f"{key}-lower",
            )
            upper = st.number_input(
                "Upper",
                value=initial_filters.get(key, [None, 0.0, None, 0.0])[3],
                label_visibility="collapsed",
                placeholder="Upper",
                key=f"{key}-upper",
            )
        assert op is None or op in ["in", "out"]
        op = cast(Literal["in", "out"], op or "in")
        new_filters.append((op, lower, col or "", upper))
        new_filter_ids.append(key)
        st.write("")
        st.write("")
    if st.button("Add Filter", key=f"{outer_key}-add", use_container_width=True):
        filters.append(("in", 0.0, "", 0.0))
        filter_ids.append(uuid.uuid4().hex)
        st.rerun()
    return new_filters, new_filter_ids
