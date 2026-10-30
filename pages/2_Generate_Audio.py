import io
import os

import numpy as np
import soundfile as sf
import streamlit as st

from common import VoiceClonePrompt, load_model, save_upload_to_temp

st.set_page_config(page_title="Generate Audio", page_icon="🔊")
st.title("🔊 Generate Audio from Voice Template")
model = load_model()

pt_file = st.file_uploader("Voice template (.pt)", type=["pt"])
text = st.text_area("Text to synthesize", height=150,
                    help="You can add tags like [laughter] too.")

with st.expander("Advanced settings"):
    language = st.text_input("Language (e.g. en, zh, English); leave empty for auto", "")
    speed = st.slider("Speed", 0.5, 2.0, 1.0, 0.05)
    num_step = st.slider("Diffusion steps (quality vs. speed)", 8, 64, 32)

if st.button("Generate", type="primary", disabled=pt_file is None):
    if not text.strip():
        st.error("Please enter some text.")
        st.stop()
    pt_path = save_upload_to_temp(pt_file, suffix=".pt")
    try:
        with st.spinner("Generating speech..."):
            prompt = VoiceClonePrompt.load(pt_path)
            kwargs = dict(text=text.strip(), voice_clone_prompt=prompt,
                          speed=speed, num_step=num_step)
            if language.strip():
                kwargs["language"] = language.strip()
            audio = model.generate(**kwargs)[0]
            if hasattr(audio, "cpu"):
                audio = audio.detach().cpu().float().numpy()
            audio = np.asarray(audio).squeeze()
        buf = io.BytesIO()
        sf.write(buf, audio, model.sampling_rate, format="WAV")
        st.session_state["gen_wav"] = buf.getvalue()
        st.caption(f"Template reference text: \u201c{prompt.ref_text}\u201d")
    except Exception as e:
        st.exception(e)
    finally:
        if os.path.exists(pt_path):
            os.remove(pt_path)

if "gen_wav" in st.session_state:
    st.audio(st.session_state["gen_wav"], format="audio/wav")
    st.download_button("⬇️ Download audio (.wav)", st.session_state["gen_wav"],
                       file_name="omnivoice_output.wav", mime="audio/wav")
