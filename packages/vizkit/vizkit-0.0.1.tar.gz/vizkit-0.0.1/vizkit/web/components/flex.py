import streamlit as st
import uuid


def flexbox(
    flex_direction: str = "row",
    align_items: str = "center",
    justify_content: str = "flex-start",
    flex_wrap: str = "wrap",
    children_styles: dict[int, str] | list[str] | None = None,
):

    id = "_" + uuid.uuid4().hex

    container_selector = f'div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stHtml > span.{id})'

    children_styles = children_styles or {}
    children_css = ""

    if isinstance(children_styles, dict):
        for i, style in children_styles.items():
            children_css += (
                f"{container_selector} > div:nth-child({i+2}) {{ {style} }}\n"
            )
    elif isinstance(children_styles, list):
        for i, style in enumerate(children_styles):
            children_css += (
                f"{container_selector} > div:nth-child({i+2}) {{ {style} }}\n"
            )
    container = st.container()

    container.html(
        f"""
        <span style="display:none" class="{id}"></span>

        <style>
            {container_selector} {{
                display: flex !important;
                flex-direction: {flex_direction} !important;
                align-items: {align_items} !important;
                flex-wrap: {flex_wrap} !important;
                justify-content: {justify_content} !important;
            }}

            {container_selector} div:has(> div.stSelectbox)  {{
                width: unset !important;
            }}

            {container_selector} div.stSelectbox  {{
                width: unset !important;
            }}

            {container_selector} div:has(> div.stButton)  {{
                width: unset !important;
            }}

            {container_selector} div.stButton  {{
                width: unset !important;
            }}

            {container_selector} div.stNumberInput  {{
                width: unset !important;
            }}

            {container_selector} div:has(> div.stHtml)  {{
                width: unset !important;
            }}

            {container_selector} div.stHtml  {{
                width: unset !important;
            }}

            {container_selector} div[data-testid="stVerticalBlock"]  {{
                width: unset !important;
            }}

            {children_css}
        </style>
        """
    )

    return container
