# Slazzer CLI

A CLI tool for removing backgrounds from images using the Slazzer API.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/slazzer-cli.git
cd slazzer-cli
```

## Install the package:

```bash
pip install .
```
Create a .env file in the root directory and add your Slazzer API key:

```bash
SLAZZER_API_KEY=your_api_key_here
```

Usage
```bash
slazzer-cli <input> [output] [options]
```

## Examples

1. Remove background from a single image file:

`slazzer-cli path/to/image.jpg --bg-color-code "#ffffff"`

Remove background from all images in a directory:

`slazzer-cli path/to/directory --bg-color-code "#ffffff"`

For more options, use the `--help` flag:

`slazzer-cli --help`


## Options

--bg-image-file: Background image file
--bg-image-url: Background image URL
--bg-image-base64: Background image in base64
--bg-color-code: Background color in hex (e.g., #ffffff)
--format: Output image format (choices: png, jpg, zip)
--crop: Crop extra transparent pixels (type: bool)
--crop-margin: Crop margin (e.g., 20px, 10%, 10px,20px)
--scale: Scale the subject (e.g., 50%)
--position: Position the subject within the canvas (e.g., 10%,10%)
--preview: Resize image to 0.25 megapixel for preview (type: bool)
--channel: Return image channel (choices: rgba, alpha)
--roi: Region of interest (e.g., 200px,320px,400px,230px)
--car-shadow: Include artificial car shadow (type: bool)


### 4. **Create a `.env.example`**

Provide an example `.env` file to guide users on how to set up their environment variables.

`SLAZZER_API_KEY=your_api_key_here`


### 5. **Create a `requirements.txt`**

List the dependencies in a `requirements.txt` file for easy installation.

- requests
- python-dotenv

