import webbrowser
import pyautogui
import pyperclip
import keyboard
import json
from os import system

from .text_analysers import (
	normalise_punctuation,
	hot_keys
)


class AppStarter:
	def __init__(self) -> str:
		with open(
			"C:\\Projects\\Garik\\Model\\settings.json",
			encoding="utf-8",
			mode='r'
		) as file:
			self.__settings = dict(json.load(file))
			self.__programs = dict(self.__settings["programs"])

	def start(self, name: str) -> str:
		program_path = self.__programs.get(name)

		print(f"{program_path = } | {name = }")
		
		if program_path:
			system(program_path)
			return f"start-app ok {name}"
		else:
			return f"start-app add-to-settings {name}"


class Searcher:
	@staticmethod
	def search(request: str) -> str:
		webbrowser.open(
			url=f"https://yandex.ru/search/?text={
				"+".join(request.split(' '))
			}"
		)

		return f"browse ok {request}"


class KeyboardEmulator:
	def emulate(self, command: str) -> None:
		if command.startswith("перемести курсор на "):
			KeyboardEmulator._move_cursor(command[22:])
		elif command.startswith(("введи", "напиши")):
			for task in ("введи", "напиши"):
				if command.startswith(task):
					KeyboardEmulator._enter_text(
						command[len(task) + 1:]
					)
		elif command.startswith("выдели все"):
			KeyboardEmulator._select_all()
		elif command.startswith("скопируй"):
			self._copy_selected()
		elif command.startswith("вырежи"):
			self._cut_selected()
		elif command.startswith("вставь"):
			self._paste()
		elif command.startswith("верни"):
			KeyboardEmulator._turn_back()
		elif command.startswith("сохрани"):
			KeyboardEmulator._save()
			print("Сохранил")
		elif command.startswith("нажми"):
			KeyboardEmulator._press(command[6:])
		elif command.startswith("сотри", "удали"):
			KeyboardEmulator._delete()

	@staticmethod
	def _enter_text(text: str) -> None:
		pyperclip.copy(normalise_punctuation(text))
		keyboard.press_and_release("ctrl + v")

	@staticmethod
	def _cut_selected() -> None:
		keyboard.press_and_release("ctrl + c")
		keyboard.press_and_release("\b")

	@staticmethod
	def _copy_selected() -> None:
		keyboard.press_and_release("ctrl + c")
	
	@staticmethod
	def _select_all() -> None:
		keyboard.press_and_release("ctrl + a")
	
	@staticmethod
	def _turn_back() -> None:
		keyboard.press_and_release("ctrl + z")

	@staticmethod
	def _press(command: str) -> None:
		keyboard.press_and_release(hot_keys(command))

	@staticmethod
	def _move_cursor(command: str) -> None:
		if command.startswith(("вверх")):
			pyautogui.press("up")
		elif command.startswith(("направо", "вправо")):
			pyautogui.press("right")
		elif command.startswith("вниз"):
			pyautogui.press("down")
		else:
			pyautogui.press("left")

	@staticmethod
	def _save() -> None:
		keyboard.press_and_release("ctrl + s")
	
	@staticmethod
	def _paste() -> None:
		keyboard.press_and_release("ctrl + v")
	
	@staticmethod
	def _delete():
		keyboard.press_and_release("\b")
	

class MouseEmulator:
	def emulate(self, command: str) -> None:
		if command.startswith("подвинь мышку на "):
			MouseEmulator._move_cursor(
				command[18:]
			)
		elif command.startswith(
			("опусти", "подними")
		):
			for task in ("опусти", "подними"):
				if (command.startswith(task)):
					MouseEmulator._scroll_window(
						task[len(task) + 1:]
					)
		elif command.startswith("кликни"):
			print(f"кликаю: {command[7:]}")
			MouseEmulator._click(command[7:])

	@staticmethod
	def _move_cursor(data: str) -> None:
		orientations = {
			"наверх": (0, -1),
			"направо": (1, 0),
			"вниз": (0, 1),
			"налево": (-1, 0)
		}

		forces = {
			"слабо": 25,
			"средне": 350,
			"сильно": 700
		}

		orientation, force = data.split(' ')

		coords = (coord * forces.get(force) for coord in \
				orientations.get(orientation))

		pyautogui.moveRel(
			*(coord * forces.get(force) for coord in \
				orientations.get(orientation))
		)

	@staticmethod
	def _scroll_window(clicks: int) -> None:
		pyautogui.scroll(clicks)

	@staticmethod
	def _click(command: str) -> None:
		if command == "левой":
			pyautogui.click(button="left")
		elif command == "правой":
			pyautogui.click(button="right")
