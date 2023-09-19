import json
from llama_cpp import Llama
from textwrap import indent
import time

def loadModel(model_name, model_path):
    try:
        print("Cargando el modelo...")
        LLM = Llama(model_path+model_name)
        print("Modelo cargado correctamente...")
        return LLM
        
    except:
        print("Ocurrio un error al cargar el modelo...")

def ModelInference(LLM,userQuestion):
    promt = "Answer the next in spanish. Question: " + userQuestion + " Answer:"
    #promt = "Answer in Spanish. If the answer includes numbers, write them with letters. Answer the following in Spanish. Question: " + userQuestion + " Answer:"
    output = LLM(promt, max_tokens = 180, temperature = 0.9, stop = ["Question:", "Q:"], echo = True)
    #print(json.dumps(output, indent = 2))
    resp = output["choices"][0]["text"]
    #print(resp)
    resp = resp.split('Answer: ')[1]
    return resp


