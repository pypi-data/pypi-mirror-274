import pandas as pd


DEFAULT_SCENARIO_COLUMNS = ["build", "bench", "invocation", "iteration"]


def default_index(options: list[str], *, default: str | None) -> int | None:
    if default is not None and default in options:
        return options.index(default)
    if len(options) > 0:
        return 0
    return None


def default_values(
    options: list[str], *, default: list[str] | str | None
) -> list[str] | None:
    if default is not None:
        if isinstance(default, str):
            default = [default]
        if all([d in options for d in default]):
            return default
    return None


def scenario_columns(
    data: pd.DataFrame, *, exclude: list[str] | str | None = None
) -> list[str]:
    if exclude is None:
        exclude = []
    if isinstance(exclude, str):
        exclude = [exclude]
    default_scenarios = [
        c for c in data.columns if c in DEFAULT_SCENARIO_COLUMNS and c not in exclude
    ]
    # any columns with non-numeric values
    non_numeric = [
        c
        for c in data.columns
        if c not in default_scenarios
        and not pd.api.types.is_numeric_dtype(data[c])
        and c not in exclude
    ]
    return default_scenarios + non_numeric


def is_ci_column(col: str) -> bool:
    if ":" not in col:
        return False
    suffix = col.split(":")[-1]
    return suffix in ["ci95-lo", "ci95-hi", "sem", "count"]


def value_columns(
    data: pd.DataFrame, *, ci: bool, exclude: list[str] | str | None = None
) -> list[str]:
    if exclude is None:
        exclude = []
    if isinstance(exclude, str):
        exclude = [exclude]
    return [
        c
        for c in data.columns
        if c not in DEFAULT_SCENARIO_COLUMNS
        and (ci or not is_ci_column(c))
        and c not in exclude
    ]
