import json
from llama_cpp import Llama
from textwrap import indent
import time



# Cargar el mododelo
print("Cargado el modelo...")

#vicuna = Llama(model_path="/home/mcim/Descargas/Vicuna/llama-2-7b-chat.ggmlv3.q4_0.bin", verbose= True, n_ctx=2048)
vicuna = Llama(model_path="/home/mcim/Descargas/Vicuna/luna-ai-llama2-uncensored.ggmlv3.q4_0.bin", verbose= True, n_ctx=2048)
#Samantha 7B
#vicuna = Llama(model_path="/home/mcim/Descargas/Vicuna/NewCuantization/Samantha-7B.ggmlv3.q4_0.bin")


print("Modelo cargado...")


def VicunaInference(userQuestion):
    #promt = "Answer the next in spanish. Question: " + userQuestion + " Answer:"
    user = "User: " + userQuestion 
    promt = "System: Responde completamente en español""" + user + " Assistant:"


    '''promt ="""
    System: Eres un asistente servicial, respetuoso y honesto. Responde siempre de la forma más útil posible, sin dejar de ser seguro.
    Tus respuestas no deben incluir ningún contenido dañino, poco ético, racista, sexista, tóxico, peligroso o ilegal.
    Asegúrese de que sus respuestas sean socialmente imparciales y de naturaleza positiva.
    Si una pregunta no tiene sentido o no es coherente con los hechos, explica por qué en lugar de responder algo que no es correcto.
    Si no sabes la respuesta a una pregunta, por favor, no compartas información falsa. Responde completamente en español""" + user'''
    

    output = vicuna(promt, max_tokens = 300, temperature = 0.4, stop = ["User:", "U:"], echo = True)
    #print(json.dumps(output, indent = 2))
    resp = output["choices"][0]["text"]
    #print(resp)
    resp = resp.split('Assistant: ')[1]
    return resp

while(True):
    userQuestion = input("Escribe una pregunta: ")
    inicio = time.time() # tiempo al iniciar la funcion 
    answer = VicunaInference(userQuestion)
    print(answer)
    fin = time.time()
    print("Tiempo total: ", fin-inicio) #Mostrar el tiempo total de procesamiento
    '''
    try:
        inicio = time.time() # tiempo al iniciar la funcion 
        answer = VicunaInference(userQuestion)
        print(answer)
        fin = time.time()
        print("Tiempo total: ", fin-inicio) #Mostrar el tiempo total de procesamiento
    except:
        print("No entendi tu pregunta")'''
    