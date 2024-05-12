from abc import ABC
from subprocess import check_output, CalledProcessError

from datetime import datetime as dt

from typing import Any

from models.handlers.info import skills, how_to
# from models.scripting.main import Core

from voice.interaction import VoiceInteraction

from voice.input import OnlineVoiceInput, OfflineVoiceInput

from voice.output import Output

from models.handlers.handlers import (
	AppStarter,
	Searcher,
	KeyboardEmulator,
	MouseEmulator
)


import json


class AbstractModel(ABC):
	""" Don\'t use this class. It is just interface \
		for (on/off)line models """

	# @abstractmethod
	async def manage_command(self, command: str) -> None: ...

	# @abstractmethod
	async def __run_application(
		self,
		application_name: str
	) -> None: ...

	# @abstractmethod
	async def __search(self, request: str) -> None: ...

	# @abstractmethod
	async def __immitate_keyboard(self, data: str) -> None: ...

	# @abstractmethod
	async def __immitate_mouse(self, data: str) -> None: ...

	# # @abstractmethod
	# async def __execute_script(self, script: list[str]): ...

	# @abstractmethod
	def __close_garik(self) -> None: ...


class TextModel(AbstractModel):
	def __init__(self) -> None:
		self._activate()


	def _activate(self) -> None:
		self.applications = AppStarter()
		self.searcher = Searcher()
		self.keyboard = KeyboardEmulator()
		self.mouse = MouseEmulator()
		self.voice_output = Output()


	async def manage_command(self, command: str) -> None:
		if command == "shutdown":
			await self.__close_garik()

		for action in (
			self.__search,
			self.__run_application,
			self.__immitate_keyboard,
			self.__immitate_mouse
		):
			result = await action(command)
			
			if result:
				return result

		return "can't understand"


	async def __search(self, request: str) -> None:
		for task in (
			"открой",
			"найди",
			"включи",
			"покажи"
		):
			if request.startswith(task):
				return self.searcher.search(request[len(task) + 1:])


	async def __run_application(
		self,
		application_name: str
	) -> None:
		for task in (
			"запусти",
		):
			if application_name.startswith(task):
				return await self.applications.start(
					application_name.replace(f"{task} ", '', 1)
				)
	

	async def __immitate_keyboard(self, data: str) -> None:
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
				return self.keyboard.emulate(task)
	

	async def __immitate_mouse(self, data: str) -> None:
		for task in (
			"подними",
			"опусти",
			"перемести мышку",
			"кликни",
			"..."
		):
			if data.startswith(task):
				return self.mouse.emulate(task)
	

	# async def __execute_script(self, script: list[str]):
	# 	Core.execute(script)


	async def __close_garik(self) -> None:
		await self.voice_output.say("See you later")
		await self.voice_output.exit()
		exit()
	

	def __str__(self) -> str:
		return "TextModel"


class OfflineVoiceModel(TextModel):
	def __init__(self) -> None:
		self.input = OfflineVoiceInput()
		self._activate()


	def _activate(self) -> None:
		return super()._activate()


	async def manage_command(self, command: str) -> None:
		return await super().manage_command(command)


	async def listen(
		self,
		voice_output: Output,
		first_run: bool = True
	) -> dict[str, Any]:
		return await self.input.listen(
			voice_output,
			first_run
		)
	
	async def __search(self, request: str) -> None:
		return await super().__search(request)
	

	async def __run_application(self, application_name: str) -> None:
		return await super().__run_application(application_name)
	

	async def __immitate_keyboard(self, data: str) -> None:
		return await super().__immitate_keyboard(data)
	

	async def __immitate_mouse(self, data: str) -> None:
		return await super().__immitate_mouse(data)
	

	# async def __execute_script(self, script: list[str]):
	# 	return await super().__execute_script(script)
	

	async def __close_garik(self) -> None:
		return await super().__close_garik()


	def __str__(self) -> str:
		return "OfflineVoiceModel"


class OnlineVoiceModel(OfflineVoiceModel):
	def __init__(self) -> None:
		self.input = OnlineVoiceInput()
		self._activate()


	def _activate(self) -> None:
		return super()._activate()
	

	async def listen(
		self,
		voice_output: Output,
		first_run: bool = True
	) -> dict[str, Any]:
		return await super().listen(
			voice_output,
			first_run
		)
	

	async def manage_command(self, command: str) -> None:
		return await super().manage_command(command)


	async def __search(self, request: str) -> None:
		return await super().__search(request)
	

	async def __run_application(self, application_name: str) -> None:
		return await super().__run_application(application_name)
	

	async def __immitate_keyboard(self, data: str) -> None:
		return await super().__immitate_keyboard(data)


	async def __immitate_mouse(self, data: str) -> None:
		return await super().__immitate_mouse(data)
	

	# async def __execute_script(self, script: list[str]):
	# 	return await super().__execute_script(script)
	

	async def __close_garik(self) -> None:
		return await super().__close_garik()
	

	def __str__(self) -> str:
		return "OnlineVoiceModel"


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
		self.output_voice = Output()
		self.first_run = True


	@staticmethod
	async def _get_internet_connection_status() -> bool:
		responses = []

		for IP in (
			"142.251.40.164",
			"104.21.54.180",
			"5.255.255.242"
		):
			try:
				responses.append("(0% " in check_output(
					f'ping -n 1 -w 500 {IP}',
					shell=True,
					encoding=str(
						check_output('chcp', shell=True)
					).split(':')[-1][1:].split('\\')[0]
				))
			except CalledProcessError as CPE:
				responses.append(False)

		return any(responses)
	

	async def __process_voice_model(self) -> str:
		current_model: OnlineVoiceModel | OfflineVoiceModel = None

		fast_recognition_state =\
			VoiceInteraction.get_fast_recognition()
		inet_connection =\
			await LoopsManager._get_internet_connection_status()

		if (fast_recognition_state or not inet_connection):
			current_model = self.models["voice"]["offline"]
		else:
			current_model = self.models["voice"]["online"]

		voice = await current_model.listen(
			self.output_voice,
			self.first_run
		)

		self.first_run = False
		
		if voice["success"]:
			if voice["transcription"].startswith((
				"что ты умеешь",
				"что ты можешь",
				"..."
			)):
				return f"{voice["transcription"]} ~ {skills}"
			elif voice["transcription"].startswith((
				"список команд",
				"что тебе говорить",
				"как с тобой говорить",
				"как с тобой разговаривать",
				"..."
			)):
				return f"{voice["transcription"]} ~ {how_to}"
			elif voice["transcription"] in (
				"прислушивайся",
				"работаем",
				"слушай пока не остановлю"
			):
				print("Listening until stop")
				return f"{voice["transcription"]} ~ listening-until-stop"
			elif voice["transcription"] in (
				"отдыхай"
			):
				print("Stop listen")
				return f"{voice["transcription"]} ~ stop-listen"
			else:
				result = await current_model.\
					manage_command(voice["transcription"])
				return f"{voice["transcription"]} ~ {result}"
		else:
			error_text = f"Online recogniser doesn\'t work because of {
				voice["error"]}"
			
			await self.output_voice.say(error_text)

			return f"voice-error {voice['error']}"


	async def __process_text_model(self, text: str) -> str:
		return await self.models["text"].manage_command(text)


	def __customise(
		self,
		target: str
	) -> str:
		"""
		* switch:
			- switch to opposite voice model (online or offline)
		* voice:
			- on/off Garik's voice
		* add-app <name> <path>:
			- add application to applications.json file
		"""

		if target in ("switch", "voice"):
			VoiceInteraction.switch_voice_setting(target)
		elif target.startswith("add-app"):
			json_file_path = "C:/Projects/Garik/Model/applications.json"

			programs: dict[str, str] = {}

			with open(json_file_path, encoding="utf-8", mode='r') as file:
				programs = json.load(file)

			new_app_info = target[8:].split(" ~ ")

			programs[new_app_info[0]] =\
				f"\"{new_app_info[1].replace("\\", "/")}\""

			with open(
				json_file_path,
				encoding="utf-8",
				mode='w'
			) as file:
				json.dump(
					obj=programs,
					fp=file,
					indent=4,
					ensure_ascii=False
				)
				AppStarter.update()
				return f"customise ok add-app {
					new_app_info[0]} {new_app_info[1]}"

		return f"customise ok {\
			VoiceInteraction.get_fast_recognition()} {\
				VoiceInteraction.get_voice()}"


	async def processing_method(
		self,
		command: str,
		message_owner: str = ""
	) -> str:
		if command == "shutdown":
			await self.__process_text_model(command)
			return

		if command.startswith("listen"):
			print(f"[out -> {message_owner}]\t<{\
				dt.now()}>\t[listen]\t")
			return await self.__process_voice_model()
		elif command.startswith("text"):
			print(f"[out -> {message_owner}]\t<{\
				dt.now()}>\t[text]\t{command[5:]}")
			return await self.__process_text_model(command[5:])
		elif command.startswith("custom"):
			print(f"[out -> {message_owner}]\t<{\
				dt.now()}>\t[customise]\t{command[7:]}")
			return self.__customise(command[7:])
		
		return "can't understand"
