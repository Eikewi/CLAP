import requests
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

'''
Local models: Use Ollama API for an Mac optimize local models.
'''

# API-URL
# Ollama API:
url = "http://localhost:11434/api/generate"

def init_llm(useOpenAI):
    if useOpenAI:
        load_dotenv() # get API key for OpenAI
    else:
        data = {
            "model": "llama3.1",
            "prompt": ""
        }
        requests.post(url, json=data, stream=True)


def run_llm(input: str, audio_lambda, threshold:int, useOpenAI=False):
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
    # Funktionslogik hier

    # use OpenAI model
    if useOpenAI: 
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "user", "content": f"{input}"}
            ]
        )
        print(completion)
        return
    
    # Use local model
    else: 

        data = {
        "model": "llama3.1",
        "prompt": f"{input}"
        }

        response = requests.post(url, json=data, stream=True)

        message = ""
        start_pos = 0
        skip = False

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
                        end_pos = positions[-1]
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

        return message