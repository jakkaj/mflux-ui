# app.py
"""
Minimal Streamlit front‑end for FLUX image generation models.
Assumes:
    • `mflux` is already installed and on your PATH  
    • you are running on macOS/Apple‑silicon with enough disk/RAM for the models  
Run with:
    streamlit run app.py
"""

import os
import subprocess
import tempfile
import uuid
from datetime import datetime

import streamlit as st

# ----------  MODEL CONFIGURATION  ----------
MODEL_CONFIGS = {
    "Text-to-Image (Schnell)": {
        "key": "schnell",
        "cli": "mflux-generate",
        "model_flag": "--model schnell",
        "requires_image": False,
        "steps_range": (1, 10),
        "default_steps": 4,
        "has_guidance": False
    },
    "Text-to-Image (Dev)": {
        "key": "dev",
        "cli": "mflux-generate",
        "model_flag": "--model dev",
        "requires_image": False,
        "steps_range": (10, 40),
        "default_steps": 20,
        "has_guidance": True,
        "guidance_range": (0.5, 8.0),
        "default_guidance": 3.5
    },
    "Image-to-Image (Kontext)": {
        "key": "kontext",
        "cli": "mflux-generate-kontext",
        "model_flag": None,
        "requires_image": True,
        "steps_range": (10, 40),
        "default_steps": 20,
        "has_guidance": True,
        "guidance_range": (2.0, 4.0),
        "default_guidance": 2.5
    }
}

# ----------  UI  ----------
st.title("MFLUX Image Generator")
st.markdown(
    "Generate images with Black Forest Labs' FLUX models: **Schnell** (fast), **Dev** (quality), or **Kontext** (image-to-image)."
)

# Model selector
selected_model = st.radio(
    "Select Model",
    options=list(MODEL_CONFIGS.keys()),
    horizontal=True
)
model_config = MODEL_CONFIGS[selected_model]

# ----  REQUIRED ARGS  ----
prompt = st.text_area("Prompt ✏️ (required)", height=120)

# Conditionally show reference image based on model
if model_config["requires_image"]:
    ref_image = st.file_uploader(
        "Reference image 📸 (required – becomes the left‑hand image)",
        type=["png", "jpg", "jpeg", "webp"],
    )
else:
    ref_image = None

# ----  COMMON OPTIONS ----
with st.sidebar:
    st.header("Generation parameters")
    
    # Dynamic steps range based on model
    steps = st.slider(
        "Steps", 
        model_config["steps_range"][0], 
        model_config["steps_range"][1], 
        model_config["default_steps"]
    )
    
    # Conditionally show guidance based on model
    if model_config["has_guidance"]:
        guidance = st.slider(
            "Guidance scale", 
            model_config["guidance_range"][0], 
            model_config["guidance_range"][1], 
            model_config["default_guidance"], 
            0.1
        )
    else:
        guidance = None
    
    width = st.number_input("Width (px)", 256, 2048, 1024, step=64)
    height = st.number_input("Height (px)", 256, 2048, 1024, step=64)

    seed_choice = st.radio("Seed", ("Random", "Fixed"), horizontal=True)
    seed = (
        st.number_input("Seed value", 0, 2**32 - 1, 42, step=1)
        if seed_choice == "Fixed"
        else None
    )

    quantize = st.selectbox("Quantize", ("None", 3, 4, 6, 8), index=1)
    low_ram = st.checkbox("Low‑RAM mode (--low-ram)")
    vae_tiling = st.checkbox("VAE tiling (--vae-tiling)")
    vae_split = st.selectbox(
        "VAE split direction", ("horizontal", "vertical"), disabled=not vae_tiling
    )

    st.header("Output")
    out_dir = st.text_input("Output directory", "outputs")
    model_prefix = model_config["key"]
    default_name = f"{model_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    out_name = st.text_input("File name", default_name)

# Update generate button to handle different model requirements
if model_config["requires_image"]:
    generate_btn = st.button("Generate 🚀", disabled=not (prompt and ref_image))
else:
    generate_btn = st.button("Generate 🚀", disabled=not prompt)


# ----------  GENERATION LOGIC  ----------
def run_generation():
    os.makedirs(out_dir, exist_ok=True)

    # Build base command based on model
    cmd = [model_config["cli"]]
    
    # Add model flag if needed (for schnell/dev)
    if model_config["model_flag"]:
        cmd.extend(model_config["model_flag"].split())
    
    # Handle image input if required
    if model_config["requires_image"] and ref_image:
        # save uploaded reference image to a temp file
        tmp_dir = tempfile.mkdtemp()
        ref_path = os.path.join(tmp_dir, ref_image.name)
        with open(ref_path, "wb") as f:
            f.write(ref_image.read())
        cmd.extend(["--image-path", ref_path])
    
    # Common parameters
    cmd.extend([
        "--prompt", prompt,
        "--steps", str(steps),
        "--width", str(width),
        "--height", str(height),
        "--output", os.path.join(out_dir, out_name),
    ])
    
    # Add guidance if the model supports it
    if model_config["has_guidance"] and guidance is not None:
        cmd.extend(["--guidance", str(guidance)])

    if quantize != "None":
        cmd += ["-q", str(quantize)]
    if seed is not None:
        cmd += ["--seed", str(seed)]
    if low_ram:
        cmd.append("--low-ram")
    if vae_tiling:
        cmd += ["--vae-tiling", "--vae-tiling-split", vae_split]

    # run and stream stderr/stdout to the Streamlit console
    st.info(f"Running {model_config['cli']}… this may take a while the first time (model download)")
    
    # Create a container for real-time output
    output_container = st.empty()
    output_lines = []
    
    # Run command with real-time output streaming
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    # Stream output line by line
    for line in process.stdout:
        output_lines.append(line.rstrip())
        # Keep last 50 lines to avoid UI overload
        if len(output_lines) > 50:
            output_lines.pop(0)
        # Update the output display
        output_container.code('\n'.join(output_lines))
    
    # Wait for process to complete
    process.wait()
    
    if process.returncode != 0:
        st.error(f"{model_config['cli']} failed!")
        return

    # display generated image
    out_path = os.path.join(out_dir, out_name)
    if os.path.isfile(out_path):
        st.success("Done!")
        st.image(out_path, caption=out_path, use_column_width=True)
    else:
        st.error("Generation completed but output file was not found.")


# ----------  MAIN  ----------
if generate_btn:
    run_generation()