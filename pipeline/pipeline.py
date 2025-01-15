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
    [ ] test ChatGPT API key
---------------------------------------------------
[ ] Chat history for llm (context based answers)
---------------------------------------------------
'''
useOpenAI = False

def init_all_models(useOpenAI=False):
    #clean_serial()
    init_a2t()
    init_llm(useOpenAI)
    return init_audio() #audio engine

def main(audio_engine, useOpenAI=False):

    while True:
        record_audio()
        txt_audio = a2t("output.mp3")
        print(f"Debug: {txt_audio}")

        audio_lambda = lambda x: create_audio(x, audio_engine)
        run_llm(txt_audio, audio_lambda, 1, useOpenAI)

        #print(f"Answer of the llm: {llm_answer}\n")
        #create_audio(llm_answer, audio_engine)

        input("press Enter to get new Input:")



if __name__ == "__main__":

    audio_engine = init_all_models(useOpenAI)
    input("Init finished, press enter to continue:")
    #record_audio()
    main(audio_engine)
    #print(run_llm("Was ist der unterschied zwischen einer Matrix und einem Tensor?", audio_engine, 1, True))