import platform
if platform.system() == 'Darwin':
    import whisper_mps.whisper # whisper with mps support
else:
    import whisper 

def init_a2t():
    if platform.system() == 'Darwin':
        return whisper_mps.whisper.load_models.load_model("medium")
    else: 
        return whisper.load_model("medium")

def a2t(a2t_model, audio_file):
    if platform.system() == 'Darwin':
        txt_audio = whisper_mps.whisper.transcribe(audio_file, model="medium")
    else:
        txt_audio =  whisper.transcribe(a2t_model, audio=audio_file)
        
    #print(f"Extracted audio: {txt_audio}\n")
    return txt_audio['text']

