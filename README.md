# 🎨 MFLUX-UI - Your Streamlit-Powered FLUX Image Generator!

> *Transform your wildest ideas into stunning visuals with the power of FLUX models, now with a friendly Streamlit interface!*

![Made with Love](https://img.shields.io/badge/Made%20with-🤍-red.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![macOS](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)
![FLUX](https://img.shields.io/badge/Powered%20by-FLUX-purple.svg)

## 🚀 What is MFLUX-UI?

MFLUX-UI is your friendly neighborhood image generator that wraps the amazing [MFLUX](https://github.com/filipstrand/mflux) project in a beautiful, easy-to-use web interface! Whether you're an AI art enthusiast, a creative professional, or just someone who loves making cool images, MFLUX-UI has got you covered.

### ✨ Features

- **🖼️ Multiple FLUX Models**: Choose from:
  - **Schnell** - Lightning-fast generation (1-10 steps)
  - **Dev** - High-quality results with guidance control
  - **Kontext** - Image-to-image transformations
- **🎛️ Real-time Parameter Tuning**: Adjust steps, guidance, dimensions, and more!
- **💾 Smart Output Management**: Auto-organized outputs with timestamps
- **🔧 Advanced Options**: Quantization, VAE tiling, low-RAM mode
- **📊 Live Generation Progress**: Watch your masterpiece come to life!

## 🛠️ Prerequisites

Before we dive into the fun stuff, make sure you have:

- 🍎 **macOS with Apple Silicon** (M1/M2/M3/M4)
- 🐍 **Python 3.10 or higher**
- 💾 **At least 16GB RAM** (32GB+ recommended for best performance)
- 🗄️ **~50GB free disk space** (for model downloads)
- 🤗 **Hugging Face account** (free!)

## 🏃‍♂️ Quick Start

### 1️⃣ Clone this Repository

```bash
git clone https://github.com/jakkaj/mflux-ui.git
cd mflux-ui
```

### 2️⃣ Set Up Your Python Environment

We recommend using a virtual environment to keep things tidy:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
```

### 3️⃣ Install MFLUX

The easiest way is using `uv`:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install MFLUX
uv tool install --upgrade mflux
```

Alternatively, you can use pip:

```bash
pip install mflux
```

### 4️⃣ Install Streamlit

```bash
pip install streamlit
```

### 5️⃣ Set Up Hugging Face

First, create a free account at [huggingface.co](https://huggingface.co) if you don't have one.

Then, get your access token:
1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Create a new token (or use an existing one)
3. Copy the token

Set it up in your terminal:

```bash
# Option 1: Export as environment variable
export HF_TOKEN="your_token_here"

# Option 2: Use Hugging Face CLI
pip install huggingface-hub
huggingface-cli login
# Paste your token when prompted
```

### 6️⃣ Accept Model Licenses

Before using FLUX models, you need to accept their licenses on Hugging Face:

- **FLUX.1-schnell**: [Accept here](https://huggingface.co/black-forest-labs/FLUX.1-schnell)
- **FLUX.1-dev**: [Accept here](https://huggingface.co/black-forest-labs/FLUX.1-dev)

Just click "Accept" on each model page while logged into your Hugging Face account.

## 🎨 Running MFLUX-UI

Fire up the Streamlit interface:

```bash
streamlit run runner.py
```

Your browser should automatically open to `http://localhost:8501`. If not, just click the link in your terminal!

## 🎮 Using MFLUX-UI

### Basic Workflow

1. **Choose Your Model**:
   - **Schnell**: Super fast, great for prototyping
   - **Dev**: Best quality, more control
   - **Kontext**: Upload an image and transform it!

2. **Write Your Prompt**: Be creative! The more descriptive, the better.

3. **Tweak Settings** (optional):
   - Adjust steps for speed vs quality
   - Play with guidance scale (Dev/Kontext only)
   - Set custom dimensions
   - Use a fixed seed for reproducible results

4. **Click Generate** and watch the magic happen!

## 📁 Output Organization

Your creations are saved in the `outputs/` directory with descriptive filenames:
- `schnell_20250702_143022.png` - Schnell model output
- `dev_20250702_143022.png` - Dev model output  
- `kontext_20250702_143022.png` - Kontext model output

## 🚨 Troubleshooting

### "Model not found" error
Make sure you've:
1. Set up your Hugging Face token
2. Accepted the model licenses
3. Have enough disk space for downloads

### Out of memory errors
Try:
- Enabling "Low-RAM mode" in the sidebar
- Using higher quantization (6 or 8)
- Reducing image dimensions
- Closing other applications

### Slow first run
The first time you use each model, MFLUX downloads it (~30GB each). This is normal! Subsequent runs will be much faster.

## 🌟 Examples

### Text-to-Image (Schnell)
```
Prompt: "A cozy coffee shop on Mars with Earth visible through the window, digital art style"
Steps: 4
Dimensions: 1024x1024
```

### Text-to-Image (Dev)
```
Prompt: "A majestic dragon made of northern lights dancing across a starry sky"
Steps: 20
Guidance: 3.5
Dimensions: 1024x1024
```

### Image-to-Image (Kontext)
Upload a photo of your pet and try:
```
Prompt: "Transform into a renaissance painting with ornate golden frame"
Steps: 20
Guidance: 2.5
```

## 🔗 Links & Resources

- **MFLUX Project**: [github.com/filipstrand/mflux](https://github.com/filipstrand/mflux)
- **FLUX Models**: [Black Forest Labs](https://blackforestlabs.ai)
- **Hugging Face**: [huggingface.co](https://huggingface.co)
- **Streamlit Docs**: [streamlit.io](https://streamlit.io)

## 🤝 Contributing

Found a bug? Have an idea? Feel free to:
- Open an issue
- Submit a pull request
- Share your coolest generated images!

## 📄 License

This project wraps MFLUX, which is based on FLUX models. Please respect all applicable licenses:
- MFLUX is under MIT License
- FLUX models have their own licenses (check Hugging Face pages)
- This wrapper is provided as-is for educational and creative purposes

## 🎉 Happy Creating!

Now go forth and create some amazing images! Remember, the only limit is your imagination (and maybe your GPU memory 😄).

---

*Made with ❤️ for the AI art community*