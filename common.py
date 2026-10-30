import os
import tempfile

import streamlit as st
import torch
from omnivoice import OmniVoice

try:
    from omnivoice import VoiceClonePrompt
except ImportError:
    from omnivoice.models.omnivoice import VoiceClonePrompt


def pick_device():
    if torch.cuda.is_available():
        return "cuda:0", torch.float16
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps", torch.float16
    if hasattr(torch, "xpu") and torch.xpu.is_available():
        return "xpu", torch.float16
    return "cpu", torch.float32


@st.cache_resource(show_spinner="Loading OmniVoice model (first run downloads weights)...")
def load_model():
    device, dtype = pick_device()
    return OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map=device, dtype=dtype)


def save_upload_to_temp(uploaded_file, suffix=None):
    """Write a Streamlit UploadedFile to disk and return the path."""
    if suffix is None:
        suffix = os.path.splitext(uploaded_file.name)[1] or ".wav"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded_file.getvalue())
    tmp.close()
    return tmp.name
