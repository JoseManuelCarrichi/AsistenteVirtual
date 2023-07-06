import whisper
import speech_recognition as sr
from queue import Queue
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
import io
'''
def trasncript(file_name):
    wake_word = "Atomo"
    model = whisper.load_model("base")
    result = model.transcribe(file_name)
    print(result["text"])

    if wake_word in result["text"]:
        prompt = result["text"].replace(wake_word+", ", "")
        print(f"Promt final: {prompt}")
        return prompt
    else:
        print("No encontre la frase")
        return "Hola"

'''
class transcription_function():
    def __init__(self):
        self.wake_word = ["atom", "¡atom!", "¿atom?", "atomo", "a tom"]
        self.model = whisper.load_model("base")
        self.transcription = [""]
        self.record_timeout = 3
        self.phrase_timeout = 3
        self.energy_threshold = 1000
        self.phrase_time = None
        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = self.energy_threshold
        self.recorder.dynamic_energy_threshold = False
        self.last_sample = bytes()
        self.data_queue = Queue()
        self.prompt = ""
        self.temp_file = NamedTemporaryFile().name
        
    def whisper_listen(self):
        # Tasa de muestreo en 16 KHz
        self.source = sr.Microphone(sample_rate=16000)
        with self.source:
            # Se ajusta el nivel de ruido ambiente para que no se tome como voz
            self.recorder.adjust_for_ambient_noise(self.source)
            # Funcion que se ejecuta en un hilo secundario para grabar el microfono
            # El parametro audio es un objeto AudioData que contiene los Bytes grabados
            def record_callback(_, audio:sr.AudioData) -> None:
                # Se obtienen los bytes del objeto AudioData y se agregan a la cola thread-safe.
                data = audio.get_raw_data()
                self.data_queue.put(data)
            
        # Se deja el microfono en segundo plano y se establece una tiempo limite para cada grabacion
        self.recorder.listen_in_background(self.source, record_callback, phrase_time_limit=self.record_timeout)
        start = datetime.utcnow()
        
        while True:
            try:
                now = datetime.utcnow()
                # Se escribe la transcripción cada 8 segundos
                if ((now - start).total_seconds()%8) == 0:
                    #print("Entro a escribir el trasncrit")
                    print(self.transcription)
                    #print("Salgo de imprimir")
                # Se verifica si hay nuevos datos de audio en la cola thread-safe
                if not self.data_queue.empty():
                    phrase_complete = False
                    # Se verifica si la grabación actual ha superado el tiempo límite
                    if self.phrase_time and now - self.phrase_time > timedelta(seconds=self.phrase_timeout):
                        self.last_sample = bytes()
                        phrase_complete = True
                    # Si esta es la última vez que recibimos datos de audio nuevos de la cola.
                    self.phrase_time = now
                    while not self.data_queue.empty():
                        data = self.data_queue.get()
                        self.last_sample += data
                    # Se crea un objeto AudioData con los datos de audio recibidos
                    audio_data = sr.AudioData(self.last_sample, self.source.SAMPLE_RATE, self.source.SAMPLE_WIDTH)
                    # Se convierte el objeto AudioData a formato wav
                    wav_data = io.BytesIO(audio_data.get_wav_data())
                    # Se guarda el archivo temporalmente para poder transcribirlo 
                    with open(self.temp_file, 'w+b') as f:
                        f.write(wav_data.read())
                    # Se llama a whisper para transcribir el audio
                    print("voy a transcribir con whisper")
                    result = self.model.transcribe(self.temp_file, fp16=False, language='es')
                    text = result['text'].strip()
                    print(text)
                    # Se agrega la transcripción a la lista de transcripciones.
                    if phrase_complete:
                        self.transcription.append(text)
                    else:
                        self.transcription[-1] = text
                    # Si la palabra clave ("wake word") se encuentra en la última transcripción, se activa el asistente virtual.
                    for i in range (5):
                        if self.wake_word[i] in self.transcription[-1].lower():
                            print("Encontre la palabra :)")
                            prompt = self.transcription[-1].lower().replace(self.wake_word[i],"").replace(",", "").strip()
                            print("USER: ",prompt)
                            self.transcription = [""]
                            return prompt       
                            
                            
            except KeyboardInterrupt:
                break
    

'''listener = transcription_function()
frase = listener.listen()

print(f"La frase es: {frase}")'''