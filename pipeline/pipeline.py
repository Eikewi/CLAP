from audio_2_txt import init_a2t, a2t
from txt_llm import run_llm, init_llm
from txt_2_audio import create_audio, init_audio, tts_process
from get_audio_stream import record_audio, clean_serial

from multiprocessing import Process, Queue
from time import time

'''
TODO:
---------------------------------------------------
[x] multithreading for txt2speech (faster answers)
---------------------------------------------------
[x] using ChatGPT API
    [x] test ChatGPT API key
---------------------------------------------------
[x] Chat history for llm (context based answers)
    [x] history for OpenAI
    [x] history for Ollama
---------------------------------------------------
[ ] be able to interrupt CLAP
---------------------------------------------------
[ ] support english in txt2audio (currently only german)
---------------------------------------------------
FIXME:
[ ] Sometimes activates 
    without waiting for the activation word
=> i think it happens when the audio buffer gets cut off 
    before everything was send
Recrate: 1. start clap and do not say anything
         2. Wait for answer and see that it restarts instant after that
'''
# Should OpenAI be used (Note: an API-Key needed)
useOpenAI = False

# NOTE: NOT YET FULLY TESTED
# Change if used in an loud environment to f.e. 0.5
#   (high values -> wait longer for a response)
tolerance = 3.0

# ---------Choose an available model---------------
# OpenAI model list: https://openai.com/api/pricing/
if useOpenAI:
    model = "gpt-4o-mini"
    n_remember_msg = 10 
else:
# Ollama model list: https://ollama.com/library 
#                    (or https://huggingface.co/docs/hub/ollama)
    model = "llama3.1"

    # How many messages should be remembered 
    #    (large numbers reduce the answer quality)
    n_remember_msg = 3 

def init_all_models(model, useOpenAI=False):
    '''
    preload all the models in the cache
    '''
    a2t_model = init_a2t()
    init_llm(model, useOpenAI)
    return a2t_model

def main(a2t_model, model, tolerance, n_remember_msg, useOpenAI=False):

    while True:
        # use multithreading for the txt2audio processing
        tts_queue = Queue()
        tts_proc = Process(target=tts_process, args=(tts_queue,))


        record_audio(tolerance)
        print("Audio was recorded")
        a2t_time1 = time()
        txt_audio = a2t(a2t_model, "output.mp3")
        a2t_time2 = time()
        print(f"Text from Audio: {txt_audio}")
        print(f"--------t2a took {round(a2t_time2 - a2t_time1, 2)}s--------")
        #txt_audio = input("Frage:") # If you want to use llm without Arduino (uncomment above)

        audio_lambda = lambda x: create_audio(x, tts_queue)

        llm_time1 = time()
        tts_proc.start()
        run_llm(txt_audio, audio_lambda, 1, model, n_remember_msg, useOpenAI)

        tts_queue.put(None)
        tts_proc.join()
        llm_time2 = time()
        print("Audioengine and llm finished")
        print(f"--------llm and audio took {round(llm_time2-llm_time1, 2)}s--------")



if __name__ == "__main__":

    init_time1 = time()
    a2t_model= init_all_models(model, useOpenAI)
    init_time2 = time()
    input(f"--------Init finished and took {round(init_time2-init_time1, 2)}s,--------\n press ENTER to continue:")
    main(a2t_model, model, tolerance, n_remember_msg, useOpenAI)