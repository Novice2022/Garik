import speech_recognition
from vosk import Model, KaldiRecognizer, SetLogLevel
import pyaudio
import json
from typing import overload, Any

from voice.output import Output
from metaclasses.singleton import MetaSingleton


class OnlineVoiceInput(metaclass=MetaSingleton):
	def __init__(self) -> None:
		self.__recogniser = speech_recognition.Recognizer()
		self.__microphone = speech_recognition.Microphone()


	async def listen(
		self,
		voice_output: Output,
		first_run: bool = True
	) -> dict[str, Any]:

		response = {
			"success": True,
			"error": None,
			"transcription": None
		}

		print("Starting online listening")

		with self.__microphone as source:
			self.__recogniser.adjust_for_ambient_noise(source)
			if first_run:
				await voice_output.say("I\'m listening you")
			
			audio = self.__recogniser.listen(source)

			try:
				response["transcription"] = str(self.__recogniser.\
					recognize_google(audio, language="ru-RU")).\
						lower().replace("гарик ", "", 1)
			except speech_recognition.RequestError:
				response["success"] = False
				response["error"] = "unavailable"
			except speech_recognition.UnknownValueError:
				response["success"] = False
				response["error"] = "doesn\'t understand"

			return response


class OfflineVoiceInput(metaclass=MetaSingleton):
	def __init__(self) -> None:
		self.__model_path = "C:/Projects/Garik/Model/models/offline_recognition/vosk-model-small-ru-0.22"

		SetLogLevel(-1)

		self.__model = Model(self.__model_path)
		self.__rec = KaldiRecognizer(self.__model, 16000)
		self.__p = pyaudio.PyAudio()


	async def listen(
		self,
		voice_output: Output,
		first_run: bool = True
	) -> dict[str, Any]:
		stream = self.__p.open(
			format=pyaudio.paInt16, 
			channels=1, 
			rate=16000, 
			input=True, 
			frames_per_buffer=16000
		)
		stream.start_stream()

		print("Starting offline listening")

		if first_run:
			await voice_output.say("I\'m listening")

		while True:
			data = stream.read(16000)

			if self.__rec.AcceptWaveform(data):
				data: str = dict(json.loads(self.__rec.FinalResult()))["text"]

				stream.close()

				return {
					"success": True,
					"error": None,
					"transcription": data.replace("гарик ", "", 1)
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
