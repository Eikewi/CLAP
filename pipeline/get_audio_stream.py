import serial
import numpy as np
from pydub import AudioSegment
import platform

# Einstellungen für die serielle Verbindung
SERIAL_PORT = '/dev/cu.usbmodem11101' if platform.system() == "Darwin" else "/dev/ttyACM0" # Passe dies an deinen COM-Port an (z.B. /dev/ttyUSB0 für Linux/Mac)
BAUD_RATE = 115200
START_DURATION = 100  
OUTPUT_FILE = "output.mp3"
NUM_TIMEOUT_SAMPLES = 30000 # Number of samples needed to trigger a timeout

def stop_recording():
    print("Keyword detection stopped")
    send_number(b'\x01')

def start_recording():
    print("Keyword detection started")
    send_number(b'\x02')

def clean_serial():
    '''
    Offload all the data that was recorded during the init step
    '''
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        pass
    stop_recording()

def send_number(num=b'\x01'):
    """
    Send a byte string to the serial.
    """
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            ser.write(num) 
    except Exception as e:
        print(f"Error while sending a number: {e}")

def record_audio(tolerance=1.0):
    print("start recording...")
    start_recording()

    audio_data = []
    count_TIMEOUT = 0

    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        while True:
            try:
                # read 2 bytes for a 16-bit sample
                data = ser.read(2)
                if len(data) == 2:
                    sample = int.from_bytes(data, byteorder='little', signed=True)
                    audio_data.append(sample*30) # make the audio 30 x loader
                    print(f"{sample}    ", end="\r")
                    count_TIMEOUT +=1
                    if abs(sample) > START_DURATION:
                        # someone is speaking
                        print("LOUD!!", end="\r")
                        count_TIMEOUT = 0
                    
                    '''
                    Calculate the ending threshold 
                    (-> speaking a long time results in less samples needed without loud noice to stop recording)

                        Alpha is a value that decreases from 1 to 0.5 in a reciprocal manner.
                            -> set Alpha to 1 for no convergence
                        Increase the scale for slower convergence.
                        end_val indicates the target value to which we are converging.
                    '''
                    scale = 16000
                    end_val = 0.1
                    alpha = min(1, (tolerance*scale / len(audio_data)) + end_val)

                    if count_TIMEOUT > NUM_TIMEOUT_SAMPLES * alpha:
                        stop_recording()
                        print(count_TIMEOUT)
                        break

            except Exception as e:
                print(f"Fehler: {e}")
                break

    print(f"Aufnahme beendet. {len(audio_data)} Samples gesammelt.")

    audio_data = np.clip(audio_data, -32768, 32767) #make sure we do not get a overflow
    audio_array = np.array(audio_data, dtype=np.int16)

    # create AudioSegment (Mono, 16 kHz, 16-bit PCM)
    audio_segment = AudioSegment(
        audio_array.tobytes(),
        frame_rate=16000,
        sample_width=2,
        channels=1
    )

    # save as MP3
    audio_segment.export(OUTPUT_FILE, format="mp3")
    print(f"Audio gespeichert als '{OUTPUT_FILE}'.")

    return audio_segment


if __name__ == "__main__":
    record_audio()
    if input("Trigger word (enter)") == "":
        record_audio()
