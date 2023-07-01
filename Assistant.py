
from LogicEngine import ModelInference
from LogicEngine import loadModel
from tts import text_to_speech
from tts import load_tts

import time

class Assistant:
    def __init__(self, model_name, model_path, max_tokens, temperature,model_voice_name,file_path,voice_speed):
        self.model_name = model_name
        self.model_path = model_path
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.user_question = ""
        self.answer = ""
        self.LLM = ""

        self.model_voice_name = model_voice_name
        self.file_path = file_path
        self.speed = voice_speed
        self.tts = ""

    def load(self):
        self.LLM = loadModel(self.model_name, self.model_path)
        self.tts = load_tts(self.model_voice_name)

    def listen(self):
        try:
            self.user_question = input("Escribe una pregunta: ")
        except:
            print("Ocurrio un error al procesar la pregunta escrita.")

    def think(self):
        print(f"Pregunta leida: {self.user_question}")
        self.answer = ModelInference(self.LLM,self.user_question)
        print(self.answer)
        '''try:
            print(self.user_question)
            self.answer = ModelInference(self.user_question)
            print(self.answer)
        except:
            print("No entendi tu pregunta")'''

    def speak(self):
        text_to_speech(self.tts,self.answer,self.file_path,self.speed)
        