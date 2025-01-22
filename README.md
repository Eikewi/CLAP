# CLAP

An awesome voice assistant with a keyword-detection-neural-network running on an Arduino and a configurable AI-Pipeline!

## Arduino 

What you need: 
- CLAP_inferencing.zip included as ZIP-Library in Arduino IDE
- A working Arduino Nano 33 BLE Sense Rev2
- A USB-to-Micro-USB cable
- A working computer with USB ports

### Keyword-Detection

Transition: Starts automatically at first

LED: Green

Serial: Empty, when SHOW_RESULTS is false

### Stream-Audio

Transition: When keyword was detected starts automatically

LED: Red

Serial: All the info

### Audio-Stopped

Transition: Starts when it receives 1 or '1' in serial

LED: Blue

Serial: Empty

### Restart Keyword-Detection

Transition: Starts when it receives 2 or '2' in serial

LED: Green again

Serial: Empty, when SHOW_RESULTS is false

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
