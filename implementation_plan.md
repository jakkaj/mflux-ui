# Simple FLUX Streamlit Interface Implementation Plan

## Overview
Update the Streamlit interface to support three FLUX models: Dev and Schnell for text-to-image, and Kontext for image-to-image.

## 1. Model Selection System
- Add a model selector radio button with exactly 3 options:
  - **Text-to-Image (Schnell)** - Fast generation without reference image
  - **Text-to-Image (Dev)** - High quality generation without reference image
  - **Image-to-Image (Kontext)** - Style-preserving generation with required reference image
- Dynamically show/hide UI elements based on selected model

## 2. Dynamic UI Components

### Base Components (all models):
- Prompt field
- Output directory/filename
- Quantization selector
- Low-RAM/VAE tiling options

### Conditional Components:
- Reference image upload(s) - shown for models that require images
- Mask upload - for Fill model
- Multiple image uploads - for Redux
- Model-specific parameters (guidance, strength, etc.)

## 3. Model-Specific Configurations

### Model Configurations
- **Schnell (Text-to-Image)**: 
  - Steps: 2-4 (optimized for speed)
  - No guidance parameter
  - No image required
  - CLI: `mflux-generate --model schnell`
  
- **Dev (Text-to-Image)**: 
  - Steps: 20-25 (higher quality)
  - Guidance scale: 3.5 default
  - No image required
  - CLI: `mflux-generate --model dev`

- **Kontext (Image-to-Image)**: 
  - Required: reference image
  - Steps: 20 default
  - Guidance: 2.0-4.0 (default 2.5)
  - CLI: `mflux-generate-kontext`

## 4. Command Generation Logic
Build appropriate CLI command based on:
- Selected model type
- Model-specific executable
- Required vs optional parameters
- User inputs

## 5. File Structure
- Keep `runner.py` as main file
- Add model configurations dictionary
- Implement dynamic UI rendering based on selection

## 6. Implementation Steps

1. **Add Model Selector**
   - Place at top of UI
   - Use selectbox with grouped options
   
2. **Create Model Configuration Dictionary**
   ```python
   MODEL_CONFIGS = {
       "schnell": {
           "cli": "mflux-generate",
           "model_flag": "--model schnell",
           "requires_image": False,
           "steps_range": (1, 10),
           "default_steps": 4,
           "has_guidance": False
       },
       "dev": {
           "cli": "mflux-generate",
           "model_flag": "--model dev",
           "requires_image": False,
           "steps_range": (10, 40),
           "default_steps": 20,
           "has_guidance": True,
           "guidance_range": (0.5, 8.0),
           "default_guidance": 3.5
       },
       "kontext": {
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
   ```

3. **Implement Dynamic UI Rendering**
   - Show/hide components based on model requirements
   - Update parameter ranges and defaults
   
4. **Update Command Builder**
   - Switch between different CLI commands
   - Handle model-specific flags
   
5. **Test Each Model Type**
   - Verify correct command generation
   - Test with appropriate parameters

## 7. UI Layout Structure
```
[Model Selector]
[Prompt Field - always visible]
[Reference Image Upload - conditional]
[Additional Image Uploads - conditional]
[Parameter Sliders - model specific]
[Advanced Options - sidebar]
[Generate Button]
[Output Display]
```

## 8. Error Handling
- Validate required inputs per model
- Show appropriate error messages
- Disable generate button until requirements met