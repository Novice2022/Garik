from abc import ABC, abstractmethod
from typing import overload


class Output:
    def __init__(self) -> None: ...

    def say(
        self,
        text: str
    ) -> None: ...

    def exit(self) -> None: ...


class OnlineVoiceInput:
    @staticmethod
    def listen(
        voice_output: Output,
        empty_previous: bool = False,
        first_run: bool = True
    ) -> dict: ...


class OfflineVoiceInput:
    @staticmethod
    def listen(
        voice_output: Output,
        empty_previous: bool = False,
        first_run: bool = True
    ) -> dict: ...


class TextScriptRecogniser:
    @overload
    def read_script(
        self,
        text_script: list[str]
    ) -> None: ...

    @overload
    def read_script(
        self,
        file_path: str
    ) -> None: ...

    @property
    def script(self) -> list[str]: ...


class AppStarter:
    def __init__(self) -> None: ...

    def start(
        self,
        name: str
    ) -> None: ...


class Searcher:
    @staticmethod
    def search(request: str) -> None: ...


class KeyboardEmulator:
    def emulate(
        self,
        command: str
    ) -> None: ...

    @staticmethod
    def _enter_text(text: str) -> None: ...

    @staticmethod
    def _cut_selected() -> None: ...

    @staticmethod
    def _copy_selected() -> None: ...
    
    @staticmethod
    def _select_all() -> None: ...
    
    @staticmethod
    def _turn_back() -> None: ...

    @staticmethod
    def _press(command: str) -> None: ...

    @staticmethod
    def _move_cursor(command: str) -> None: ...

    @staticmethod
    def _save() -> None: ...
    
    @staticmethod
    def _paste() -> None: ...
    
    @staticmethod
    def _delete() -> None: ...
    

class MouseEmulator:
    def emulate(
        self,
        command: str
    ) -> None: ...

    @staticmethod
    def _move_cursor(data: str) -> None: ...

    @staticmethod
    def _scroll_window(clicks: int) -> None: ...

    @staticmethod
    def _click(command: str) -> None: ...


class Output:
    def __init__(self) -> None: ...

    def say(self, text: str) -> None: ...

    def exit(self) -> None: ...


class BaseModel(ABC):
	""" Don\'t use this class. It is just interface \
		for (on/off)line models """

	@abstractmethod
	def manage_command(self, command: str) -> None: ...

	@abstractmethod
	def __run_application(
		self,
		application_name: str
	) -> None: ...

	@abstractmethod
	def __search(self, request: str) -> None: ...

	@abstractmethod
	def __immitate_keyboard(self, data: str) -> None: ...

	@abstractmethod
	def __immitate_mouse(self, data: str) -> None: ...

	@abstractmethod
	def __execute_script(self, script: list[str]): ...

	@abstractmethod
	def __close_garik(self, command: str) -> None: ...


class OfflineVoiceModel(BaseModel):
	def __init__(self) -> None: ...

	def __activate(self, voice_output: Output) -> None: ...

	def manage_command(self, command: str) -> None: ...

	@staticmethod
	def listen(
		voice_output: Output,
		previous_empty: bool = False,
		first_run: bool = True
	) -> str: ...

	def __search(self, request: str) -> None: ...

	def __run_application(
        self,
        application_name: str
    ) -> None: ...
	
	def __immitate_keyboard(self, data: str) -> None: ...
	
	def __immitate_mouse(self, data: str) -> None: ...
	
	def __execute_script(self, script: list[str]): ...

	def __close_garik(self, command: str) -> None: ...
	
	def __str__(self) -> str: ...


class OnlineVoiceModel(OfflineVoiceModel):
	def __init__(self) -> None: ...

	def __activate(self, voice_output: Output) -> None: ...

	@staticmethod
	def listen(
		voice_output: Output,
		previous_empty: bool = False,
		first_run: bool = True
	) -> str: ...
	
	def manage_command(self, command: str) -> None: ...

	def __search(self, request: str) -> None: ...
	
	def __run_application(
        self,
        application_name: str
    ) -> None: ...
	
	def __immitate_keyboard(self, data: str) -> None: ...

	def __immitate_mouse(self, data: str) -> None: ...
	
	def __execute_script(self, script: list[str]): ...
	
	def __close_garik(self, command: str) -> None: ...
	
	def __str__(self) -> str: ...


class TextModel(BaseModel):
	def __init__(self) -> None: ...
	
	def __activate(self) -> None: ...

	def manage_command(self, command: str) -> str: ...

	def __search(self, request: str) -> None: ...

	def __run_application(
        self,
        application_name: str
    ) -> None: ...
	
	def __immitate_keyboard(self, data: str) -> None: ...
	
	def __immitate_mouse(self, data: str) -> None: ...
	
	def __execute_script(self, script: list[str]): ...

	def __close_garik(self, command: str) -> None: ...
	
	def __str__(self) -> str: ...


class LoopsManager:
	def __init__(self) -> None: ...
	
	def __get_settings(self) -> dict[
          str,
          str | dict[str, str]
    ]: ...

	@staticmethod
	def _get_internet_connection_status() -> bool: ...
	
	def __process_voice_model(self) -> str: ...
	
	def __process_text_model(self, text: str) -> str: ...

	def __customise(
		self,
		setting_name: str,
		*parametrs: str
	) -> str: ...

	async def processing_method(
        self,
        command: str
    ) -> str: ...


class GarikInfo:
    def __init__(
        self,
        status: str
    ) -> None: ...
    
    def switch_status(self) -> None: ...

    @property
    def skills(self) -> str: ...
    
    @property
    def how_to(self) -> str: ...


def normalise_punctuation(text: str) -> str: ...

def hot_keys(data: str) -> str: ...
