from os import system
import speech_recognition
from vosk import Model, KaldiRecognizer, SetLogLevel
import pyaudio
import json
from typing import overload

from voice.output import Output


class OnlineVoiceInput:
    @staticmethod
    def listen(
        voice_output: Output,
        empty_previous: bool = False,
        first_run: bool = True
    ) -> dict:
        recogniser = speech_recognition.Recognizer()
        microphone = speech_recognition.Microphone()

        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        print("перед with")
        with microphone as source:
            recogniser.adjust_for_ambient_noise(source)
            if empty_previous or first_run:
                print(f"\n{"=" * 70}\n\nСлушаю тебя, дружище")
                voice_output.say("I\'m listening you")
            
            audio = recogniser.listen(source)

            try:
                response["transcription"] = str(recogniser.\
                    recognize_google(audio, language="ru-RU")).\
                        lower().replace("гарик ", "", 1)
            except speech_recognition.RequestError:
                response["success"] = False
                response["error"] = "unavailable"
            except speech_recognition.UnknownValueError:
                response["success"] = False
                response["error"] = "doesn\'t understand"

            return response


class OfflineVoiceInput:
    @staticmethod
    def listen(
        voice_output: Output,
        empty_previous: bool = False,
        first_run: bool = True
    ) -> dict:
        while True:
            with open(
                "settings.json",
                encoding="utf-8",
                mode='r'
            ) as file:
                data = dict(json.load(file))
                model_path = data["offline-recognition-model-path"]

            SetLogLevel(-1)

            model = Model(model_path)
            rec = KaldiRecognizer(model, 16000)
            p = pyaudio.PyAudio()

            stream = p.open(
                format=pyaudio.paInt16, 
                channels=1, 
                rate=16000, 
                input=True, 
                frames_per_buffer=16000
            )
            stream.start_stream()

            if empty_previous or first_run:
                print(f"\n{"=" * 70}\n\nСлушаю тебя, дружище")
                voice_output.say("I\'m listening")

            while True:
                data = stream.read(16000)

                if rec.AcceptWaveform(data):
                    return {
                    "success": True,
                    "error": None,
                    "transcription": dict(json.loads(rec.FinalResult()))["text"]
                }

class TextScriptRecogniser:
    @overload
    def read_script(self, text_script: list[str]) -> None:
        self.__script = text_script

    @overload
    def read_script(self, file_path: str) -> None:
        self.__script = open(
            file_path,
            'r',
            encoding='"utf-8'
        ).readlines()

    @property
    def script(self) -> list[str]:
        return self.__script
