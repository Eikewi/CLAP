from audio_2_txt import init_a2t, a2t
from txt_llm import run_llm, init_llm
from txt_2_audio import create_audio, init_audio
from get_audio_stream import record_audio, clean_serial

'''
TODO:
---------------------------------------------------
[ ] multithreading for txt2speech (faster answers)
---------------------------------------------------
[x] using ChatGPT API
    [x] test ChatGPT API key
---------------------------------------------------
[ ] Chat history for llm (context based answers)
---------------------------------------------------
[ ] be able to interrupt CLAP
---------------------------------------------------
[ ] support english txt2audio
---------------------------------------------------
'''
# Should OpenAI be used (Note: an API-Key needed)
useOpenAI = False

# ---------Choose an available model---------------
# OpenAI model list: https://openai.com/api/pricing/
if useOpenAI:
    model = "gpt-4o-mini"
else:
# Ollama model list: https://ollama.com/library (or https://huggingface.co/docs/hub/ollama)
    model = "llama3.1"

def init_all_models(model, useOpenAI=False):
    '''
    preload all the models in the cache
    '''
    #clean_serial()
    a2t_model = init_a2t()
    init_llm(model, useOpenAI)
    return a2t_model, init_audio() #audio engine

def main(audio_engine, a2t_model, model, useOpenAI=False):

    while True:
        record_audio()
        print("Audio was recorded")
        txt_audio = a2t(a2t_model, "output.mp3")
        print(f"Text from Audio: {txt_audio}")

        audio_lambda = lambda x: create_audio(x, audio_engine)
        run_llm(txt_audio, audio_lambda, 1, model, useOpenAI)
        print("Audioengine and llm finished")

        #create_audio(llm_answer, audio_engine)



if __name__ == "__main__":

    a2t_model, audio_engine = init_all_models(model, useOpenAI)
    input("Init finished, press enter to continue:")
    main(audio_engine, a2t_model, model, useOpenAI)
    #audio_lambda = lambda x: create_audio(x, audio_engine)
    #print(run_llm("Was ist der unterschied zwischen einer Matrix und einem Tensor?", audio_lambda, 1, True))