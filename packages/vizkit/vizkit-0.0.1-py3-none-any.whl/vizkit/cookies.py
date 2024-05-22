import streamlit as st
from typing import TYPE_CHECKING, Any, Union, overload

if TYPE_CHECKING:
    from streamlit_cookies_manager import CookieManager


def guard():
    from streamlit_cookies_manager import CookieManager

    cm = CookieManager()
    st.session_state["cookie_manager"] = cm
    # if not cm.ready():
    #     st.stop()


@overload
def get() -> "CookieManager": ...


@overload
def get(key: str, default=None) -> Any: ...


def get(key: str | None = None, default: Any = None) -> Union["CookieManager", Any]:
    if key is not None:
        return get().get(key, default=default)

    from streamlit_cookies_manager import CookieManager

    if "cookie_manager" not in st.session_state:
        st.session_state["cookie_manager"] = CookieManager()
    return st.session_state["cookie_manager"]


def set(key: str, value: Any):
    get()[key] = value


def ready() -> bool:
    return get().ready()


def save():
    return get().save()


def pop(key: str, default: Any = None) -> Any:
    return get().pop(key, default=default)
