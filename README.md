# CLAP

## Arduino 
What you need: CLAP_inferencing.zip included as ZIP-Library in Arduino IDE
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
