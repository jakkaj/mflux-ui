#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set HF_TOKEN from the hf variable in .env
export HF_TOKEN="$hf"

# Check if HF_TOKEN is set
if [ -z "$HF_TOKEN" ]; then
    echo "Error: Hugging Face token not found!"
    echo ""
    echo "To get your Hugging Face token:"
    echo "1. Go to https://huggingface.co/settings/tokens"
    echo "2. Create a new token or copy an existing one"
    echo "3. Create a .env file in this directory with:"
    echo "   hf=your_token_here"
    echo ""
    echo "Make sure you've also accepted the model terms at:"
    echo "- https://huggingface.co/black-forest-labs/FLUX.1-dev"
    echo "- https://huggingface.co/black-forest-labs/FLUX.1-schnell"
    echo "- https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev"
    exit 1
fi

# Check if mflux is installed
if ! command -v mflux-generate &> /dev/null; then
    echo "mflux-generate not found. Installing mflux..."
    
    # Check if uv is installed
    if ! command -v uv &> /dev/null; then
        echo "Error: uv is not installed. Please install uv first:"
        echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
    
    # Install mflux using uv
    uv tool install --upgrade mflux
    echo "mflux installed successfully!"
fi

# Run streamlit with debug output and light theme
# Use --logger.level info for less verbose output
streamlit run runner.py --logger.level debug --theme.base light