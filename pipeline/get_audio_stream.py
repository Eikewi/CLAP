import serial
import numpy as np
from pydub import AudioSegment
import platform

# Einstellungen für die serielle Verbindung
SERIAL_PORT = '/dev/cu.usbmodem1401' if platform.system() == "Darwin" else "/dev/ttyACM0" # Passe dies an deinen COM-Port an (z.B. /dev/ttyUSB0 für Linux/Mac)
BAUD_RATE = 115200
DURATION = 100  
OUTPUT_FILE = "output.mp3"
NUM_TIMEOUT_SAMPLES = 30000 # Number of samples needed to trigger a timeout

def stop_recording():
    print("Recording stopped")
    send_number(b'\x01')

def start_recording():
    print("Recording started")
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

def record_audio():
    print("start recording...")
    start_recording()

    audio_data = []
    count_TIMEOUT = 0

    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        while True:
            try:
                # Lese 2 Bytes für ein 16-Bit Sample
                data = ser.read(2)
                if len(data) == 2:
                    sample = int.from_bytes(data, byteorder='little', signed=True)
                    audio_data.append(sample*30) # make the audio 30 x loader
                    print(sample)
                    count_TIMEOUT +=1
                    #count_TIMEOUT = 0
                    if abs(sample) > 100:
                        # Someone is speaking
                        print("LOUD!!!!!")
                        count_TIMEOUT = 0
                    if count_TIMEOUT > NUM_TIMEOUT_SAMPLES:
                        stop_recording()
                        print(count_TIMEOUT)
                        break

            except Exception as e:
                print(f"Fehler: {e}")
                break

    print(f"Aufnahme beendet. {len(audio_data)} Samples gesammelt.")

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
