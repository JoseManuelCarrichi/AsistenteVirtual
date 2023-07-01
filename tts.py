from TTS.api import TTS
from pydub import AudioSegment
from pydub.playback import play

def load_tts(model_voice_name):
    tts = TTS(model_voice_name)
    return tts

def text_to_speech(tts,answer,file_path,speed):
    # Text to speech
    tts.tts_to_file(text=answer,file_path=file_path, emotion = "happy",speed0=speed)
    # Play audio
    song = AudioSegment.from_wav("output.wav")
    play(song)