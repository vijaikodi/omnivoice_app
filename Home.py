import streamlit as st

from common import pick_device

st.set_page_config(page_title="OmniVoice Studio", page_icon="🎙️")
st.title("🎙️ OmniVoice Studio")
st.markdown(
    """
Use the sidebar to choose a page:

1. **Create Voice Template**: upload reference audio and its transcript, then download a `.pt` voice template.
2. **Generate Audio**: upload a `.pt` voice template and some text, then generate and download a WAV file.
"""
)
device, dtype = pick_device()
st.info(f"Detected device: **{device}** ({dtype})")
