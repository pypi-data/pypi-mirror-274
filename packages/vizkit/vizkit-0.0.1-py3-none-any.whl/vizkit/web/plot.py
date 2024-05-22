from vizkit import cookies
from vizkit.web.components.footer import footer
import streamlit as st

st.set_page_config(page_title="VizKit", page_icon="💥")
cookies.guard()

import streamlit as st
from vizkit.pipeline.data_source import DATA_SOURCE
from vizkit.pipeline import Pipeline

# If no id/px/p query params, get an empty pipeline
if not any(
    [st.query_params.get("id"), st.query_params.get("px"), st.query_params.get("p")]
):
    st.session_state.pipeline = Pipeline(inputs=[], project=None)
# If a data id is provided, create an empty pipeline
if data_id := st.query_params.get("id", None):
    meta = DATA_SOURCE.get_data_file_meta(data_id) if not DATA_SOURCE.is_local else None
    pipeline = Pipeline(inputs=[data_id], project=meta.project if meta else None)
    inflated_pid = pipeline.serialize_and_encode()
    st.query_params["px"] = inflated_pid
    del st.query_params["id"]
    if "p" in st.query_params:
        del st.query_params["p"]
    st.session_state.pipeline = pipeline
# If there is a pipeline cached in the session state, load it
elif "pipeline" in st.session_state:
    pipeline: Pipeline = st.session_state.pipeline
# If an inflated pipeline id is provided, load the pipeline
elif inflated_pipeline_id := st.query_params.get("px", None):
    st.session_state.pipeline = Pipeline.decode_and_deserialize(inflated_pipeline_id)
    pipeline: Pipeline = st.session_state.pipeline
# If a short pipeline id is provided, load the pipeline
elif short_pipeline_id := st.query_params.get("p", None):
    pipeline_opt = Pipeline.load_from_short_id(short_pipeline_id)
    if pipeline_opt is None:
        # show an empty pipeline
        pipeline_opt = Pipeline(inputs=[], project=None)
        st.error("ERR: decode failed")
        st.stop()
    pipeline: Pipeline = pipeline_opt
    st.session_state.pipeline = pipeline
    del st.query_params["p"]
    st.query_params["px"] = pipeline.serialize_and_encode()
else:
    st.error("No pipeline provided")
    st.stop()

# Render the pipeline content
pipeline.process()

# Update the query params
st.query_params["px"] = pipeline.serialize_and_encode()

# Footer

footer()
