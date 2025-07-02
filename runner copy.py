# app.py
"""
Minimal Streamlit front‑end for all **Kontext** functionality in MFLUX.
Assumes:
    • `mflux` is already installed and on your PATH  
    • you are running on macOS/Apple‑silicon with enough disk/RAM for the Kontext model  
Run with:
    streamlit run app.py
"""

import os
import subprocess
import tempfile
import uuid
from datetime import datetime

import streamlit as st

# ----------  UI  ----------
st.title("MFLUX Kontext")
st.markdown(
    "Generate / edit images with Black Forest Labs’ **Kontext** model through "
    "the `mflux-generate-kontext` CLI."
)

# ----  REQUIRED ARGS  ----
prompt = st.text_area("Prompt ✏️ (required)", height=120)
ref_image = st.file_uploader(
    "Reference image 📸 (required – becomes the left‑hand image)",
    type=["png", "jpg", "jpeg", "webp"],
)

# ----  COMMON OPTIONS ----
with st.sidebar:
    st.header("Generation parameters")
    steps = st.slider("Steps", 1, 40, 20)
    guidance = st.slider("Guidance scale", 0.5, 8.0, 2.5, 0.1)
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
    default_name = f"kontext_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    out_name = st.text_input("File name", default_name)

generate_btn = st.button("Generate 🚀", disabled=not (prompt and ref_image))


# ----------  GENERATION LOGIC  ----------
def run_kontext():
    os.makedirs(out_dir, exist_ok=True)

    # save uploaded reference image to a temp file
    tmp_dir = tempfile.mkdtemp()
    ref_path = os.path.join(tmp_dir, ref_image.name)
    with open(ref_path, "wb") as f:
        f.write(ref_image.read())

    # build CLI command
    cmd = [
        "mflux-generate-kontext",
        "--image-path",
        ref_path,
        "--prompt",
        prompt,
        "--steps",
        str(steps),
        "--guidance",
        str(guidance),
        "--width",
        str(width),
        "--height",
        str(height),
        "--output",
        os.path.join(out_dir, out_name),
    ]

    if quantize != "None":
        cmd += ["-q", str(quantize)]
    if seed is not None:
        cmd += ["--seed", str(seed)]
    if low_ram:
        cmd.append("--low-ram")
    if vae_tiling:
        cmd += ["--vae-tiling", "--vae-tiling-split", vae_split]

    # run and stream stderr/stdout to the Streamlit console
    st.info("Running mflux… this may take a while the first time (model download)")
    
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
        st.error("mflux failed!")
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
    run_kontext()