# 🎙️ OmniVoice Studio

A two-page [Streamlit](https://streamlit.io) app for [k2-fsa/OmniVoice](https://github.com/k2-fsa/OmniVoice) zero-shot voice cloning.

## Features

- **Create Voice Template**: upload a reference audio clip and its transcript, and download a reusable `.pt` voice template.
- **Generate Audio**: upload a `.pt` template and any text, generate speech in that voice, and download it as a WAV file.
- The model loads once and both pages share it (`st.cache_resource`).
- Picks the device automatically: CUDA, Apple Silicon (MPS), Intel XPU or CPU.

## Project structure

```
omnivoice_app/
├── requirements.txt
├── common.py                        # model loading + shared helpers
├── Home.py                          # landing page
└── pages/
    ├── 1_Create_Voice_Template.py
    └── 2_Generate_Audio.py
```

## Requirements

- **Python 3.11 or 3.12.** Don't use 3.13+ (including 3.15). Packages such as PyYAML and PyTorch don't ship prebuilt wheels for those versions yet, so pip tries to compile them and fails with `Microsoft Visual C++ 14.0 or greater is required`.
- An NVIDIA GPU is recommended. CPU works but is slow.

## Installation

### Windows (PowerShell)

```powershell
git clone https://github.com/vijaikodi/omnivoice_app.git
cd omnivoice_app
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

If PowerShell blocks the activate script, run this once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### Linux / macOS

```bash
git clone https://github.com/vijaikodi/omnivoice_app.git
cd omnivoice_app
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### Install PyTorch first, then the rest

```bash
# NVIDIA GPU (CUDA 12.x)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124
# or CPU / macOS
pip install torch torchaudio

pip install -r requirements.txt
```

## Run

```bash
streamlit run Home.py
```

Then open http://localhost:8501 in your browser.

## Usage

### 1. Create Voice Template
1. Upload a clean reference clip (wav/mp3/flac/ogg/m4a). 3 to 15 seconds of a single speaker works best.
2. Enter the exact transcript of the clip.
3. Click **Create template**, then **Download template (.pt)**.

### 2. Generate Audio
1. Upload a `.pt` template.
2. Enter the text to speak. Tags such as `[laughter]` are supported.
3. You can change language, speed and diffusion steps under *Advanced settings*.
4. Click **Generate**, listen to the result, and download the WAV.

## About the template format

The `.pt` file is written by OmniVoice's own `VoiceClonePrompt.save()`. It's a small dict that holds the reference audio tokens, the reference text and the loudness. The tokens are stored on the CPU, so a template made on a GPU machine also loads on a CPU or Mac machine, and it can be loaded safely with `torch.load(weights_only=True)`.

## Tips

- The first run downloads the model weights from Hugging Face. If you can't reach Hugging Face, set a mirror first: `HF_ENDPOINT=https://hf-mirror.com` (PowerShell: `$env:HF_ENDPOINT="https://hf-mirror.com"`).
- More diffusion steps give higher quality but slower generation. 32 is a good default.
- A clean, noise-free reference clip gives the best cloning results.

## Troubleshooting

| Problem | Fix |
|---|---|
| `Microsoft Visual C++ 14.0 or greater is required` | You're on an unsupported Python version. Use Python 3.11 or 3.12. |
| `torch.cuda.is_available()` is False | You installed the CPU build. Reinstall with the CUDA index URL above. |
| `generate()` got an unexpected keyword | Your OmniVoice version doesn't support that option. Remove it from `kwargs` in `pages/2_Generate_Audio.py`. |
| Out-of-memory on GPU | Close other GPU apps, or use shorter text. |

## Credits & license

Built on [OmniVoice](https://github.com/k2-fsa/OmniVoice) by k2-fsa. See the OmniVoice repository for the model and code license terms. Only clone voices you have permission to use.
