from typing import Literal
import streamlit as st

from vizkit.web.components.flex import flexbox


def block_controls(key: str) -> Literal["add", "delete"] | None:
    action = None

    button_style = """
        button {
            min-height: unset !important;
            line-height: 1 !important;
            padding: 0.25rem 0.65rem;
            p {
                font-size: 1.5rem !important;
            }
        }
    """

    with flexbox(children_styles=["flex:1", button_style, button_style]):
        st.html("")
        if st.button(":green[**\\+**]", key=f"{key}-add"):
            action = "add"
        if st.button(":red[**×**]", key=f"{key}-delete"):
            action = "delete"
    return action
