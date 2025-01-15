import whisper_mps.whisper # whisper with mps support

def init_a2t():
    whisper_mps.whisper.load_models.load_model("medium")

def a2t(audio_file='unterschied_tensor_matrix.wav'):
    txt_audio =  whisper_mps.whisper.transcribe(audio_file, model="medium")
    print(f"Extracted audio: {txt_audio}\n")
    return txt_audio['text']

