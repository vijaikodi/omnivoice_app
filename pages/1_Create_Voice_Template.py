import os
import tempfile

import streamlit as st

from common import load_model, save_upload_to_temp

st.set_page_config(page_title="Create Voice Template", page_icon="🎤")
st.title("🎤 Create Voice Template")
model = load_model()

ref_audio = st.file_uploader("Reference audio", type=["wav", "mp3", "flac", "ogg", "m4a"])
if ref_audio is not None:
    st.audio(ref_audio)
ref_text = st.text_area("Reference text (exact transcript of the audio)", height=120)
name = st.text_input("Template name", "voice_template")

if st.button("Create template", type="primary", disabled=ref_audio is None):
    if not ref_text.strip():
        st.error("Please enter the reference text.")
        st.stop()
    audio_path = save_upload_to_temp(ref_audio)
    tmp_pt = tempfile.NamedTemporaryFile(delete=False, suffix=".pt")
    tmp_pt.close()
    pt_path = tmp_pt.name
    try:
        with st.spinner("Encoding reference audio..."):
            prompt = model.create_voice_clone_prompt(ref_audio=audio_path, ref_text=ref_text.strip())
            prompt.save(pt_path)
        with open(pt_path, "rb") as f:
            st.session_state["template_bytes"] = f.read()
        st.session_state["template_name"] = name.strip() or "voice_template"
    except Exception as e:
        st.exception(e)
    finally:
        for p in (audio_path, pt_path):
            if os.path.exists(p):
                os.remove(p)

if "template_bytes" in st.session_state:
    st.success("Voice template created.")
    st.download_button(
        "⬇️ Download template (.pt)",
        st.session_state["template_bytes"],
        file_name=f"{st.session_state['template_name']}.pt",
        mime="application/octet-stream",
    )
