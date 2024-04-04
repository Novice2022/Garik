from os import system
from vosk import Model, KaldiRecognizer, SetLogLevel
import pyaudio, json

SetLogLevel(-1)

while True:
    model = Model(
        "C:/Code/Garik/models/offline_recognition/vosk-model-small-ru-0.22"
    )
    rec = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16, 
        channels=1, 
        rate=16000, 
        input=True, 
        frames_per_buffer=16000,
        output=False
    )
    stream.start_stream()

    while True:
        data = stream.read(16000)
        if len(data) == 0:
            break

    if dict(
        json.loads(rec.FinalResult())
    )["text"] == "гарик проснись":
        system("python C:/Code/Garik/run.py")
