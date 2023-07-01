from Assistant import Assistant
from LogicEngine import loadModel

model_name = "Wizard-Vicuna-7B-Uncensored.ggmlv3.q4_0.bin"
model_path = "/home/mcim/Descargas/VirtualAssistant/"

max_tokens = 180
temperature = 0.9
#Speech
model_voice_name = "tts_models/es/css10/vits"
voice_speed = 1.5
file_path = "output.wav"


robotito = Assistant(model_name, model_path, max_tokens, temperature, model_voice_name, file_path, voice_speed)

while(True):
    robotito.load()
    robotito.listen()
    robotito.think()
    robotito.speak()
