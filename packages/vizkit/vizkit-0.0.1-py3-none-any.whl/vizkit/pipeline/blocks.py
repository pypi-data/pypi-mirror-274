from dataclasses import dataclass, field
from typing import Literal, Self, cast
import numpy as np
import pandas as pd
import scipy
import streamlit as st
from . import Pipeline
import uuid
import copy
from streamlit_tree_select import tree_select

from vizkit.web.components.flex import flexbox

from .utils import (
    default_index,
    default_values,
    scenario_columns,
    value_columns,
)

import vizkit.web.components.filters as filters


@dataclass
class Block:
    title: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        self.__default = copy.deepcopy(self)

    @property
    def default(self) -> Self:
        return self.__default

    def is_fixed_block(self) -> bool:
        return False

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    @staticmethod
    def create_initial_blocks() -> list["Block"]:
        return [
            ColumnsBlock(),
        ]


DEFAULT_SCENARIO_COLUMNS = ["build", "bench", "invocation", "iteration"]


@dataclass
class ColumnsBlock(Block):
    title: str = "Columns"
    type: Literal["columns"] = "columns"

    scenario_columns: list[str] | None = None
    value_columns: list[str] | None = None

    def is_fixed_block(self) -> bool:
        return True

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        value_cols = value_columns(data, ci=True)
        scenario_cols = scenario_columns(data)
        nodes = [
            {
                "label": "Scenario Columns",
                "value": "sall",
                "children": [{"label": c, "value": "s:" + c} for c in scenario_cols],
            },
            {
                "label": "Value Columns",
                "value": "vall",
                "children": [{"label": c, "value": "v:" + c} for c in value_cols],
            },
        ]
        pre_checked = []
        # Pre-checked scenario columns
        if self.scenario_columns is None:
            # By default select all scenario columns
            pre_checked += [f"s:{s}" for s in scenario_cols]
        else:
            pre_checked += [
                f"s:{s}" for s in self.scenario_columns if s in scenario_cols
            ]
        # Pre-checked value columns
        if self.value_columns is None:
            # By default select "time" only
            pre_checked += ["v:time"] if "time" in value_cols else []
        else:
            pre_checked += [f"v:{v}" for v in self.value_columns if v in value_cols]

        checked: list[str] = tree_select(
            nodes, checked=pre_checked, key=f"{self.id}-ts"
        )["checked"]

        # Update scenario columns
        if self.scenario_columns is not None or len(scenario_cols) != 0:
            self.scenario_columns = sorted(
                [c[2:] for c in checked if c.startswith("s:")]
            )
        # Update value columns
        if self.value_columns is not None or len(value_cols) != 0:
            self.value_columns = sorted([c[2:] for c in checked if c.startswith("v:")])
        data = data[[*(self.scenario_columns or []), *(self.value_columns or [])]]
        return data


@dataclass
class AddBlock(Block):
    pipeline: Pipeline | None = None

    title: str = "Add Block"
    type: Literal["add_block"] = "add_block"

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        blocks = [
            ScenarioFilterBlock,
            ValueFilterBlock,
            AggregateBlock,
            NormalizeBlock,
            GraphBlock,
        ]
        with flexbox(children_styles=["flex: 1"], justify_content="flex-end"):
            selected_block = st.selectbox(
                "Block Type",
                blocks,
                format_func=lambda x: x.title,
                label_visibility="collapsed",
                placeholder="Add a block",
                key=f"opt-{self.id}",
            )
            if (
                st.button(
                    "&nbsp;&nbsp;&nbsp;**\\+**&nbsp;&nbsp;&nbsp;",
                    use_container_width=True,
                    type="primary",
                    key=f"{self.id}-block-add",
                )
                and selected_block
            ):
                assert self.pipeline is not None
                try:
                    index = self.pipeline.blocks.index(self)
                except ValueError:
                    index = -1
                if index != len(self.pipeline.blocks) - 1 and index != -1:
                    self.pipeline.blocks[index] = selected_block()
                else:
                    self.pipeline.blocks.append(selected_block())
                st.rerun()
        return data


@dataclass
class ScenarioFilterBlock(Block):
    title: str = "Scenario Filter"
    type: Literal["scenario_filter"] = "scenario_filter"

    filters: list[tuple[str, Literal["includes", "excludes"], list[str]]] | None = None
    """(column, op, values_list)"""

    def __post_init__(self):
        if self.filters is not None:
            self.filter_ids = [uuid.uuid4().hex for _ in self.filters]
        else:
            self.filter_ids = []
        self.initial_filters = {
            self.filter_ids[i]: copy.deepcopy(f)
            for i, f in enumerate(self.filters or [])
        }

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        if self.filters is None:
            if "iteration" in data.columns:
                max_invocation = data["iteration"].max()
                self.filters = [("iteration", "includes", [f"{max_invocation}"])]
                self.filter_ids = [uuid.uuid4().hex]
                self.initial_filters = {
                    self.filter_ids[0]: (
                        cast(str, "iteration"),
                        cast(Literal["includes", "excludes"], "includes"),
                        [f"{max_invocation}"],
                    )
                }
            else:
                self.filters = []
        scenario_cols = scenario_columns(data)
        # Build filters UI

        self.filters, self.filter_ids = filters.scenario_filters(
            data,
            self.filters,
            self.filter_ids,
            key=self.id + "-filters",
            initial_filters=self.initial_filters,
        )
        # Apply filters
        for col, op, values in self.filters:
            if col and op and values:
                if op == "includes":
                    data = data[data[col].astype(str).isin(values)]
                elif op == "excludes":
                    data = data[~data[col].astype(str).isin(values)]
        # Remove scenario columns if all values are the same
        data = data[
            [c for c in data.columns if c not in scenario_cols or len(set(data[c])) > 1]
        ]
        return data.reset_index(drop=True)


@dataclass
class ValueFilterBlock(Block):
    title: str = "Value Filter"
    type: Literal["value_filter"] = "value_filter"

    filters: list[tuple[Literal["in", "out"], float, str, float]] | None = None
    """(op, lower, column, upper)"""

    def __post_init__(self):
        if self.filters is not None:
            self.filter_ids = [uuid.uuid4().hex for _ in self.filters]
        else:
            self.filter_ids = []
        self.initial_filters = {
            self.filter_ids[i]: copy.deepcopy(f)
            for i, f in enumerate(self.filters or [])
        }

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        value_cols = value_columns(data, ci=False)
        if self.filters is None and len(value_cols) > 0:
            self.filters = [("in", 0.0, value_cols[0], 0.0)]
            self.filter_ids = [uuid.uuid4().hex]
            self.initial_filters = {
                self.filter_ids[0]: (
                    cast(Literal["in", "out"], "in"),
                    0.0,
                    value_cols[0],
                    0.0,
                )
            }
        # Build filters UI
        self.filters, self.filter_ids = filters.value_filters(
            data,
            self.filters or [],
            self.filter_ids,
            initial_filters=self.initial_filters,
            key=self.id + "-filters",
        )
        # Apply filters
        for kind, lower, col, upper in self.filters:
            if kind and col and (lower is not None) and (upper is not None):
                if kind.lower() == "in":
                    data = data[data[col].between(lower, upper)]
                elif kind.lower() == "out":
                    data = data[data[col].between(lower, upper)]
        return data.reset_index(drop=True)


@dataclass
class AggregateBlock(Block):
    title: str = "Aggregate"
    type: Literal["aggregate"] = "aggregate"

    op: str | None = None
    col: str | None = None

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        scenario_cols = scenario_columns(data)
        with flexbox(children_styles=["flex: 1", "", "flex: 1"]):
            op = st.selectbox(
                "Type",
                ["mean", "geomean"],
                label_visibility="collapsed",
                key=f"{self.id}-type",
            )
            st.html('<span style="text-align: center"><b>over</b></span>')
            col = st.selectbox(
                "Column",
                scenario_cols,
                index=default_index(
                    scenario_cols, default=self.default.col or "invocation"
                ),
                label_visibility="collapsed",
                placeholder="Scenario",
                key=f"{self.id}-col",
            )
        if op and col:
            group_cols = scenario_columns(data, exclude=col)
            all_cols = [c for c in data.columns if c != col and c not in group_cols]
            value_cols = value_columns(data, ci=False)  # discard previous ci columns
            if op == "mean":
                groups = data.groupby(group_cols)
                stats = groups[all_cols].agg(["mean", "count", "std", "sem"])
                cols = {}
                conf = 0.95
                for v in value_cols:
                    s = stats[v]
                    mean, count, sem = (s["mean"], s["count"], s["sem"])
                    h = sem * scipy.stats.t.ppf((1 + conf) / 2.0, count - 1)
                    cols[v] = mean
                    cols[v + ":ci95-lo"] = mean - h
                    cols[v + ":ci95-hi"] = mean + h
                    cols[v + ":count"] = count
                    cols[v + ":sem"] = sem
                data = pd.DataFrame(cols)
            elif op == "geomean":
                data = data.groupby(group_cols)[all_cols].agg("geomean")
            self.op = op
            self.col = col
        data = data.reset_index()
        return data


@dataclass
class NormalizeBlock(Block):
    title: str = "Normalize"
    type: Literal["normalize"] = "normalize"

    target: Literal["scenario", "best_value"] | None = None
    scenario: str | None = None
    scenario_value: str | None = None
    grouping: list[str] | None = None

    def __is_with_ci(self, group: pd.DataFrame, col: str):
        return (
            col + ":ci95-lo" in group.columns
            and col + ":ci95-hi" in group.columns
            and col + ":count" in group.columns
            and col + ":sem" in group.columns
        )

    def __normalize_fn(self, value_cols: list[str]):
        def normalize(group: pd.DataFrame) -> pd.DataFrame:
            conf = 0.95
            baseline = group.loc[group[self.scenario] == self.scenario_value]
            for c in value_cols:
                if self.__is_with_ci(group, c):
                    # References:
                    #   1. Fieller's theorem: https://en.wikipedia.org/wiki/Fieller%27s_theorem
                    #   2. Motulsky, 'Intuitive Biostatistics', pp285-6, 'Confidence Interval of a Ratio of Two Means'
                    #   3. Harvey Motulsky (https://stats.stackexchange.com/users/25/harvey-motulsky), How to compute the confidence interval of the ratio of two normal means, URL (version: 2016-05-11): https://stats.stackexchange.com/q/16354
                    val = group[c] / baseline[c].iloc[0]
                    tinv = scipy.stats.t.ppf(
                        (1 + conf) / 2.0,
                        group[f"{c}:count"] + baseline[f"{c}:count"].iloc[0] - 2,
                    )
                    g = (
                        tinv * (baseline[f"{c}:sem"].iloc[0] / baseline[c].iloc[0])
                    ) ** 2
                    sem = (val / (1 - g)) * np.sqrt(
                        (1 - g) * (group[f"{c}:sem"] / group[c]) ** 2
                        + (baseline[f"{c}:sem"].iloc[0] / baseline[c].iloc[0]) ** 2
                    )
                    group[f"{c}:ci95-lo"] = (val / (1 - g)) - tinv * sem
                    group[f"{c}:ci95-hi"] = (val / (1 - g)) + tinv * sem
                    group[c] = val
                    group.pop(f"{c}:count")
                    group.pop(f"{c}:sem")
                else:
                    group[c] = group[c] / baseline[c].iloc[0]
            return group

        return normalize

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        kind = st.radio(
            "Normalize to",
            ["To Specific Scenario", "To Best Value"],
            label_visibility="collapsed",
            key=f"{self.id}-kind",
        )
        self.target = "scenario" if kind == "To Specific Scenario" else "best_value"
        # get scenario and value columns
        scenario_cols = scenario_columns(data)
        # get scenario values
        if self.target == "scenario":
            col1, col2 = st.columns([1, 1])
            with col1:
                self.scenario = st.selectbox(
                    "Scenario",
                    scenario_cols,
                    index=default_index(
                        scenario_cols, default=self.default.scenario or "build"
                    ),
                    key=f"{self.id}-scenario",
                )
            with col2:
                scenario_vals = sorted(list(set(data[self.scenario])))
                self.scenario_value = st.selectbox(
                    "Value",
                    sorted(list(set(data[self.scenario]))),
                    index=default_index(
                        scenario_vals, default=self.default.scenario_value
                    ),
                    key=f"{self.id}-scenario_value",
                )
        # get grouping columns
        grouping_scenario_cols = (
            scenario_columns(data, exclude=self.scenario)
            if self.target == "scenario"
            else scenario_cols
        )
        self.grouping = st.multiselect(
            "Grouping",
            grouping_scenario_cols,
            default=default_values(
                grouping_scenario_cols, default=self.default.grouping or "bench"
            ),
            key=f"{self.id}-grouping",
        )
        # process data
        if self.target == "scenario":
            value_cols = value_columns(data, ci=False)
            if self.scenario and self.scenario_value and self.grouping:
                data = data.groupby(self.grouping).apply(
                    self.__normalize_fn(value_cols)
                )
                data = data.reset_index(drop=True)
        elif self.target == "best_value":
            st.error("Not implemented")
        return data


@dataclass
class GraphBlock(Block):
    title: str = "Graph"
    type: Literal["graph"] = "graph"

    format: Literal["Histogram"] = "Histogram"
    # Bar chart configs
    x: str | None = None
    ys: list[str] | None = None
    hue: str | None = None

    def plot(self, data: pd.DataFrame):
        if not self.x or not self.ys or not self.hue:
            return
        all_value_cols = value_columns(data, ci=True)
        for y in self.ys:
            has_ci = (
                y + ":ci95-lo" in all_value_cols and y + ":ci95-hi" in all_value_cols
            )
            layer = [
                {
                    "mark": {"type": "bar", "tooltip": True},
                    "encoding": {
                        "x": {"field": self.x, "axis": {"labelAngle": -45}},
                        "y": {"field": y, "type": "quantitative"},
                        "xOffset": {"field": self.hue},
                        "color": {"field": self.hue},
                    },
                }
            ]
            if has_ci:
                layer.append(
                    {
                        "mark": {
                            "type": "errorbar",
                            "extent": "ci",
                            "ticks": {"color": "black"},
                        },
                        "encoding": {
                            "y": {
                                "field": y + ":ci95-hi",
                                "type": "quantitative",
                                "scale": {"zero": False},
                                "axis": {
                                    "title": y,
                                },
                            },
                            "y2": {"field": y + ":ci95-lo"},
                            "x": {"field": self.x, "type": "ordinal"},
                            "xOffset": {"field": self.hue, "type": "ordinal"},
                        },
                    },
                )
            st.vega_lite_chart(data, {"layer": layer}, use_container_width=True)

    def __config_bar_chart(self, data: pd.DataFrame):
        scenario_cols = scenario_columns(data)
        self.x = st.selectbox(
            "X Asis",
            scenario_cols,
            index=default_index(scenario_cols, default=self.default.x or "bench"),
            key=f"{self.id}-x",
        )

        value_cols = value_columns(data, ci=False)
        self.ys = st.multiselect(
            "Y Axis",
            value_cols,
            default=default_values(value_cols, default=self.default.ys or "time"),
            key=f"{self.id}-ys",
        )

        scenario_cols2 = scenario_columns(data, exclude=self.x)
        self.hue = st.selectbox(
            "Hue",
            scenario_cols2,
            index=default_index(scenario_cols2, default=self.default.hue or "build"),
            key=f"{self.id}-hue",
        )

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        format = st.selectbox("**_Format_**", ["Histogram"], key=f"{self.id}-format")
        match format:
            case "Histogram":
                self.__config_bar_chart(data)
        return data


ALL_BLOCKS: dict[str, type[Block]] = {
    "columns": ColumnsBlock,
    "add_block": AddBlock,
    "scenario_filter": ScenarioFilterBlock,
    "value_filter": ValueFilterBlock,
    "aggregate": AggregateBlock,
    "normalize": NormalizeBlock,
    "graph": GraphBlock,
}
