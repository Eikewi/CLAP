import requests
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from time import time

'''
Local models: Use Ollama API for an Mac optimize local models.
'''

# API-URL
# Ollama local-API:
url = "http://localhost:11434/api/generate"
conversation_history = []

def init_llm(model, useOpenAI):
    if not useOpenAI:
        data = {
            "model": f"{model}",
            "prompt": ""
        }
        requests.post(url, json=data, stream=True)


def run_llm(input: str, audio_lambda, threshold:int, model, n_remember_msg=1, useOpenAI=False):
    """
    Executes a large language model (LLM) process with the given input.

    Args:
        `input` (str): Input text the model should process.
        `audio_lambda` (function): A lambda function for processing audio.
        `threshold` (int): Indicates how many sentences should be used for the audio processing at once.
        `OpenAI` (bool, optional): Indicates whether to use OpenAI models. Defaults to False.

    Returns:
        str: Processed output from the LLM.
    """
    global conversation_history

    if n_remember_msg < 1:
        raise ValueError(f"Invalid value: {n_remember_msg}. Value <1 is not allowed.")

    # use OpenAI model
    if useOpenAI: 
        load_dotenv()
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        conversation_history.append({"role": "user", "content": input})

        completion = client.chat.completions.create(
            model=f"{model}",
            store=True,
            messages=conversation_history[-n_remember_msg:]
        )

        response = completion.choices[0].message.content
        print("ChatGPT answer:")
        print(response)
        conversation_history.append({"role": "assistant", "content": response})
        audio_lambda(response)
        return response
    
    # Use local model
    else: 
        conversation_history.append({"role": "user", "content": input})

        prompt = ""
        for message in conversation_history[-n_remember_msg:]:
            if message["role"] == "user":
                prompt += f"User: {message['content']}\n"
            elif message["role"] == "assistant":
                prompt += f"Assistant: {message['content']}\n"

        data = {
        "model": f"{model}",
        "prompt": f"{prompt}", 
        "system": f"Du bist ein Sprachassistent. Antworte nur in 2-3 Sätzen. Bitte vermeide Stichpunkte oder Ähnliches, das schwer lesbar ist."
        }
        print(conversation_history)
        response = requests.post(url, json=data, stream=True)

        message = ""
        start_pos = 0
        skip = False

        print("Local LLM answer:")

        # work with the stream
        for line in response.iter_lines():
            if line:  
                try:
                    json_data = json.loads(line.decode('utf-8'))
                    message += json_data.get('response', '') 

                    #try to find sentences
                    positions = [i for i, char in enumerate(message) if char == '.']

                    #start with the first sentences to get a faster answer 
                    if len(positions) > threshold and not skip:
                        end_pos = positions[-1]+1
                        print(message[start_pos:end_pos])
                        audio_lambda(message[start_pos:end_pos])
                        start_pos = end_pos
                        skip = True
                    if json_data.get('done', False):
                        break
                except json.JSONDecodeError:
                    print("ERROR: json error occurred, but ignoring it")
                    continue
        if start_pos < len(message):
            print(message[start_pos:])
            audio_lambda(message[start_pos:])

        conversation_history.append({"role": "assistant", "content": message})
        return message