from abc import ABC, abstractmethod
from os import system
from subprocess import check_output, CalledProcessError

from models.handlers.info import skills, how_to
from voice import input, output

from models.handlers.handlers import (
	AppStarter,
	Searcher,
	KeyboardEmulator,
	MouseEmulator
)

from voice.output import Output
from models.scripting.main import Core

import json


class BaseModel(ABC):
	""" Don\'t use this class. It is just interface \
		for (on/off)line models """

	# @abstractmethod
	def manage_command(self, command: str) -> None: ...

	# @abstractmethod
	def __run_application(
		self,
		application_name: str
	) -> None: ...

	# @abstractmethod
	def __search(self, request: str) -> None: ...

	# @abstractmethod
	def __immitate_keyboard(self, data: str) -> None: ...

	# @abstractmethod
	def __immitate_mouse(self, data: str) -> None: ...

	# @abstractmethod
	def __execute_script(self, script: list[str]): ...

	# @abstractmethod
	def __close_garik(self, command: str) -> None: ...


class OfflineVoiceModel(BaseModel):
	def __init__(self) -> None:
		system("cls")
		
		print("<>--------- offline ---------<>\n")
		print("Для перехода на online режим скажи: \
\"смени режим\"\n\n"
		)

		self._activate()

	def _activate(self) -> None:
		self.applications = AppStarter()
		self.searcher = Searcher()
		self.keyboard = KeyboardEmulator()
		self.mouse = MouseEmulator()
		self.voice_output = output.Output()

	def manage_command(self, command: str) -> None:
		if self.__search(command): return
		if self.__run_application(command): return
		if self.__immitate_keyboard(command): return
		if self.__immitate_mouse(command): return
		self.__close_garik(command)

	@staticmethod
	def listen(
		voice_output: Output,
		previous_empty: bool = False,
		first_run: bool = True
	) -> str:
		if previous_empty:
			print("Перевожу (самостоятельно)")
		return input.OfflineVoiceInput.listen(
			voice_output,
			previous_empty
		)

	def __search(self, request: str) -> None:
		if request.startswith((
			"найди",
			"включи",
			"покажи"
		)):
			self.voice_output.say(
				"What should I do to load a web-page without \
				internet connection in Your opinion?"
			)
			print("Как я, по-твоему, без интернета загружу \
				  страницу в браузере?"
			)
			return True

	def __run_application(
		self,
		application_name: str
	) -> None:
		for task in (
			"запусти",
			"открой"
		):
			if application_name.startswith(task):
				self.applications.start(
					application_name[len(task) + 1:]
				)
				return True
	
	def __immitate_keyboard(self, data: str) -> None:
		for task in ("напиши",
			"перемести курсор на",
			"скопируй",
			"вырежи",
			"вставь",
			"нажми",
			"введи",
			"напиши",
			"удали",
			"выдели все",
			"сохрани",
			"верни",
			"сотри"
		):
			if data.startswith(task):
				self.keyboard.emulate(task)
				return True
	
	def __immitate_mouse(self, data: str) -> None:
		for task in (
			"подними",
			"опусти",
			"перемести мышку",
			"кликни",
			"..."
		):
			if data.startswith(task):
				self.mouse.emulate(task)
				return True
	
	def __execute_script(self, script: list[str]):
		Core.execute(script)

	def __close_garik(self, command: str) -> None:
		if command.startswith("красный"):
			self.voice_output.say("See you later")
			self.voice_output.exit()
			print("\nДавай, Бро, удачи!")
			exit()
	
	def __str__(self) -> str:
		return "OfflineVoiceModel"


class OnlineVoiceModel(OfflineVoiceModel):
	def __init__(self) -> None:
		system("cls")

		print("<>--------- online ---------<>\n")
		print("Для перехода на offline режим скажи: \
\"смени режим\"\n\n"
		)

		self._activate()

	def _activate(self) -> None:
		super()._activate()

	@staticmethod
	def listen(
		voice_output: Output,
		previous_empty: bool = False,
		first_run: bool = True
	) -> str:
		if previous_empty:
			print("Перевожу (с помощью google API)")
		return input.OfflineVoiceInput.listen(
			voice_output,
			previous_empty
		)
	
	def manage_command(self, command: str) -> None:
		return super().manage_command(command)

	def __search(self, request: str) -> None:
		for task in (
			"найди",
			"включи",
			"покажи"
		):
			if request.startswith(task):
				self.searcher.search(request[len(task) + 1:])
				return True
	
	def __run_application(self, application_name: str) -> None:
		return super().__run_application(application_name)
	
	def __immitate_keyboard(self, data: str) -> None:
		return super().__immitate_keyboard(data)

	def __immitate_mouse(self, data: str) -> None:
		return super().__immitate_mouse(data)
	
	def __execute_script(self, script: list[str]):
		return super().__execute_script(script)
	
	def __close_garik(self, command: str) -> None:
		return super().__close_garik(command)
	
	def __str__(self) -> str:
		return "OnlineVoiceModel"


class TextModel(BaseModel):
	def __init__(self) -> None:
		system("cls")
		
		print("<>--------- text ---------<>\n")

		self.__activate()
	
	def __activate(self) -> None:
		self.applications = AppStarter()
		self.searcher = Searcher()
		self.keyboard = KeyboardEmulator()
		self.mouse = MouseEmulator()
		self.voice_output = output.Output()

	def manage_command(self, command: str) -> None:
		if self.__search(command): return
		if self.__run_application(command): return
		if self.__immitate_keyboard(command): return
		if self.__immitate_mouse(command): return
		self.__close_garik(command)

	def __search(self, request: str) -> None:
		if request.startswith((
			"найди",
			"включи",
			"покажи"
		)):
			self.voice_output.say(
				"What should I do to load a web-page without \
				internet connection in Your opinion?"
			)
			print("Как я, по-твоему, без интернета загружу \
				  страницу в браузере?"
			)
			return True

	def __run_application(self, application_name: str) -> None:
		for task in (
			"запусти",
			"открой"
		):
			if application_name.startswith(task):
				self.applications.start(
					application_name[len(task) + 1:]
				)
				return True
	
	def __immitate_keyboard(self, data: str) -> None:
		for task in (
			"напиши",
			"перемести курсор на",
			"скопируй",
			"вырежи",
			"вставь",
			"нажми",
			"введи",
			"напиши",
			"удали",
			"выдели все",
			"сохрани",
			"верни",
			"сотри"
		):
			if data.startswith(task):
				self.keyboard.emulate(task)
				return True
	
	def __immitate_mouse(self, data: str) -> None:
		for task in (
			"подними",
			"опусти",
			"перемести мышку",
			"кликни",
			"..."
		):
			if data.startswith(task):
				self.mouse.emulate(task)
				return True
	
	def __execute_script(self, script: list[str]):
		Core.execute(script)

	def __close_garik(self, command: str) -> None:
		if command.startswith("красный"):
			self.voice_output.say("See you later")
			self.voice_output.exit()
			print("\nДавай, Бро, удачи!")
			exit()
	
	def __str__(self) -> str:
		return "TextModel"

	
class LoopsManager:
	def __init__(self) -> None:
		self.models: dict[
			str,
			OnlineVoiceModel | OfflineVoiceModel | TextModel
		] = {
			"voice": {
				"online": OnlineVoiceModel(),
				"offline": OfflineVoiceModel()
			},
			"text": TextModel()
		}

		self.settings = self.__get_settings()

		self.first_run = True
		self.previous_empty = False
	
	def __get_settings(self) -> dict[str, str | dict[str, str]]:
		with open(
			"C:/Projects/Garik/Model/user_settings.json",
			mode='r',
			encoding='utf-8'
		) as settings:
			return json.load(settings)

	"""
	# def _switch_model(
	# 	self,
	# 	new_model_name: Literal["text", "voice-online", "voice-offline"]
	# ) -> None:
	# 	self.garik_info.switch_status()

	# 	if self.state == "online":
	# 		self.current_model = OfflineVoiceModel()
	# 		self.state = "offline"
	# 		self.current_model.__activate(self.output_voice)

	# 		return self.output_voice.say(
	# 			f"Mode switched to {self.state} successfuly"
	# 		)
		
	# 	self.current_model = OnlineVoiceModel()
	# 	self.state = "online"
	# 	self.current_model.__activate(self.output_voice)
		
	# 	self.output_voice.say(
	# 		f"Mode switched to {self.state} successfuly"
	# 	)

	# 	self.first_run = True
	"""
	
	@staticmethod
	def _get_internet_connection_status() -> bool:
		try:
			return any([
				"получено = 1" in\
				check_output(
					'ping -n 1 -w 1000 142.251.40.164',
					shell=True,
					encoding=str(
						check_output('chcp', shell=True)
					).split(':')[-1][1:].split('\\')[0]
				),
				"получено = 1" in\
				check_output(
					'ping -n 1 -w 1000 104.21.54.180',
					shell=True,
					encoding=str(
						check_output('chcp', shell=True)
					).split(':')[-1][1:].split('\\')[0]
				),
				"получено = 1" in\
				check_output(
					'ping -n 1 -w 1000 5.255.255.242',
					shell=True,
					encoding=str(
						check_output('chcp', shell=True)
					).split(':')[-1][1:].split('\\')[0]
				)
			])
		except CalledProcessError:
			return False
	
	def __process_voice_model(self) -> str:
		response = ""

		current_model: OnlineVoiceModel | OfflineVoiceModel = None

		if LoopsManager._get_internet_connection_status() and (
			self.settings["models"]["voice-online"] != "False" or\
			self.settings["fast-recognition"] != "True"
		):
			current_model = self.models["voice"]["online"]
		else:
			current_model = self.models["voice"]["offline"]
		
		print(f"{self.previous_empty = }")
		voice = current_model.listen(
			self.output_voice,
			self.previous_empty,
			self.first_run
		)

		self.first_run = False

		if self.previous_empty:
			print(f"{voice["transcription"] = }")
		
		if voice["success"]:
			self.previous_empty = bool(voice["transcription"])

			if voice["transcription"].startswith((
				"что ты умеешь",
				"что ты можешь",
				"..."
			)):
				response = skills
				print(response)
			elif voice["transcription"].startswith((
				"список команд",
				"что тебе говорить",
				"как с тобой говорить",
				"как с тобой разговаривать",
				"..."
			)):
				response = how_to
				print(response)
			else:
				current_model.\
					manage_command(voice["transcription"])
				response =\
					f"Выполняю следующую команду: {
						voice["transcription"]}"
		else:
			self.output_voice.say(
				f"Online recogniser doesn\'t work because of {
				voice["error"]}"
			)
			print(
				f"Online recogniser doesn\'t work because of {
				voice["error"]}"
			)

			response = f"Catched error: {voice["error"]}"
		
		print(f"Sending response: {response}")
		return response
	
	def __process_text_model(self, text: str) -> str:
		self.models["text"].manage_command(text)
		return f"Выполняю следующую команду: {text}"

	def __customise(
		self,
		setting_name: str,
		*parametrs: str
	) -> str:
		if parametrs[0] == "models":
			self.settings["models"][parametrs[0]] = parametrs[1]
		else:
			self.settings["fast-recognition"] = parametrs[0]

		with open(
			"C:/Projects/Garik/Model/user_settings.json",
			mode='w',
			encoding='utf-8'
		) as file:
			json.dump(self.settings, file)

		return 'settings were changed'

	async def processing_method(self, command: str) -> str:
		if command.startswith("listen"):
			return self.__process_voice_model()
		elif command.startswith("read"):
			return self.__process_text_model(command[5:])
		elif command.startswith("custom"):
			return self.__customise(*command[7:].split())
