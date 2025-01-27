<div align="center">
    <img alt="ollama" height="200px" src="https://github.com/Eikewi/CLAP/blob/main/clap_logo.png">
</div>

# CLAP

An awesome voice assistant with a keyword-detection-neural-network running on an Arduino and a configurable AI-Pipeline!

## Arduino

What you need:

- `ei-clap-arduino-1.0.8.zip` included as ZIP-Library in Arduino IDE
- A working Arduino Nano 33 BLE Sense Rev2
- A USB-to-Micro-USB cable
- A working computer with USB ports

### Demo Video
<video controls width="600">
  <source src="https://github.com/Eikewi/CLAP/blob/main/preview.mp4" type="video/mp4">
  Dein Browser unterstützt dieses Videoformat nicht.
</video>

### Keyword-Detection

Transition: Starts automatically at first and restarts after it receives 2 or '2' in serial

LED: ![#f03c15](https://placehold.co/15x15/00ff00/00ff00.png) Green

Serial: Empty, when SHOW_RESULTS is false

### Stream-Audio

Transition: When keyword was detected starts automatically

LED: ![#f03c15](https://placehold.co/15x15/ff0000/ff0000.png) Red

Serial: All the info

### Audio-Stopped

Transition: Starts when it receives 1 or '1' in serial

LED: ![#f03c15](https://placehold.co/15x15/0000ff/0000ff.png) Blue

Serial: Empty


## Getting Started

### Python

Tested on Python v3.12.3 [Download-Link](https://www.python.org/downloads/)

### Packages

#### For Linux and Windows

```
pip install pyserial numpy pydub openai-whisper pyttsx3 python-dotenv openai
```

#### For MacOS

```
pip install pyserial numpy pydub whisper-mps pyttsx3 python-dotenv openai
```

### Ollama

[Download-Link](https://ollama.com/download)

### ffmpeg

Linux: `sudo apt-get update && sudo apt-get install ffmpeg`

Windows: `winget install "FFmpeg (Essentials Build)"`

MacOS: `brew install ffmpeg`

### OpenAI API Key
Add that key into a `.env`-file within `CLAP` like `OPENAI_API_KEY=<secret-key-we-dont-share-on-github>`

### Running the python script

Simply run `pipeline.py` in `CLAP/pipeline`

## Things that you can modify

useOpenAI in the first lines of `pipeline.py` can be set to `True`, if you want to have ChatGPT as the LLM, it is using Ollama in case it is set to `False`.  
