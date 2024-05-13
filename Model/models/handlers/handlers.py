import webbrowser
import pyautogui
import pyperclip
import keyboard
import json

from .text_analysers import (
	normalise_punctuation,
	hot_keys,
	to_integer
)


class AppStarter:
	programs: dict[str, str]

	def __init__(self) -> str:
		AppStarter.update()
		
	@staticmethod
	def update() -> None:
		with open(
			"C:/Projects/Garik/Model/applications.json",
			encoding="utf-8",
			mode='r'
		) as file:
			AppStarter.programs = dict(json.loads(
				''.join(file.readlines()).lower()
			))

	async def start(self, name: str) -> str:
		program_path = AppStarter.programs.get(
			name.lower()
		)
		
		if program_path:
			normalised_path = ""
			quotes = False

			for char in program_path:
				if char == "\"":
					quotes = not quotes
					normalised_path += "\""
				elif char == " " and not quotes:
					normalised_path += " ~ "
				else:
					normalised_path += char

			return f"start-app {name} ~ {normalised_path}"
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
	async def emulate(self, command: str) -> None:
		if command.lower().startswith(("введи", "напиши")):
			for task in ("введи", "напиши"):
				if command.lower().startswith(task):
					await KeyboardEmulator._enter_text(
						command[len(task) + 1:],
					)
		else:
			command = command.lower()
			if command.startswith("перемести курсор на "):
				await KeyboardEmulator._move_cursor(command[22:])
			elif command.startswith("выдели все"):
				await KeyboardEmulator._select_all()
			elif command.startswith("скопируй"):
				await KeyboardEmulator._copy_selected()
			elif command.startswith("вырежи"):
				await KeyboardEmulator._cut_selected()
			elif command.startswith((
				"вставь",
				"помести"
			)):
				await KeyboardEmulator._paste()
			elif command.startswith("верни"):
				await KeyboardEmulator._turn_back()
			elif command.startswith("сохрани"):
				await KeyboardEmulator._save()
			elif command.startswith("нажми"):
				await KeyboardEmulator._press(command[6:])
			elif command.startswith((
				"сотри",
				"удали"
			)):
				await KeyboardEmulator._delete()
		
		return f"Выполнил: \"{command}\""

	@staticmethod
	async def _enter_text(text: str) -> None:
		pyperclip.copy(normalise_punctuation(text))
		keyboard.press_and_release("ctrl + v")

	@staticmethod
	async def _cut_selected() -> None:
		keyboard.press_and_release("ctrl + x")

	@staticmethod
	async def _copy_selected() -> None:
		keyboard.press_and_release("ctrl + c")
	
	@staticmethod
	async def _select_all() -> None:
		keyboard.press_and_release("ctrl + a")
	
	@staticmethod
	async def _turn_back() -> None:
		keyboard.press_and_release("ctrl + z")

	@staticmethod
	async def _press(command: str) -> None:
		keyboard.press_and_release(hot_keys(command))

	@staticmethod
	async def _move_cursor(command: str) -> None:
		if command.startswith(("вверх")):
			pyautogui.press("up")
		elif command.startswith(("направо", "вправо")):
			pyautogui.press("right")
		elif command.startswith("вниз"):
			pyautogui.press("down")
		else:
			pyautogui.press("left")

	@staticmethod
	async def _save() -> None:
		keyboard.press_and_release("ctrl + s")
	
	@staticmethod
	async def _paste() -> None:
		keyboard.press_and_release("ctrl + v")
	
	@staticmethod
	async def _delete():
		keyboard.press_and_release("\b")
	

class MouseEmulator:
	async def emulate(self, command: str) -> None:
		if command.startswith((
			"подвинь мышку",
			"сдвинь мышку",
			"подними мышку",
			"опусти мышку"
		)):
			"""
			command pattern:

			подвинь or
			сдвинь  or
			подними or
			опусти
				мышку <orientation> [на] <number> [пикселей]

			"""

			for task in (
				"подвинь мышку ",
				"сдвинь мышку ",
				"подними мышку ",
				"опусти мышку "
			):
				if command.startswith(task):
					orientation = ""

					if command.startswith("подними мышку "):
						orientation = "вверх"
					elif command.startswith("опусти мышку "):
						orientation = "вниз"

					await MouseEmulator._move_cursor(
						command.replace(task, "", 1)\
							.replace("на ", "", 1),
						orientation
					)
		elif command.startswith(
			("опусти", "подними")
		):
			for task in ("опусти ", "подними "):
				if command.startswith(task):
					await MouseEmulator._scroll_window(
						command.replace(task, "", 1)
					)
		elif command.startswith("кликни"):
			await MouseEmulator._click(
				command.replace("кликни", "", 1)
			)

		return f"Выполнил: \"{command}\""

	@staticmethod
	async def _move_cursor(
		data: str,
		orientation: str
	) -> None:
		if "пикс" in data:
			data = ' '.join(data.split()[:-1])

		if orientation != "":
			data = data.replace("наверх ", "", 1)\
                .replace("вверх ", "", 1)\
                .replace("вниз ", "", 1)

		orientations = {
			"наверх": (0, -1),
			"вверх": (0, -1),
			"направо": (1, 0),
			"вправо": (1, 0),
			"вниз": (0, 1),
			"налево": (-1, 0),
			"влево": (-1, 0)
		}

		orientation = data[ : data.index(" ")]\
			if orientation == "" else orientation

		value_as_words = data

		if any([
			axis in data for axis in\
				orientations.keys()
		]):
			value_as_words = ' '.join(data.split()[1:])

		value_as_number = to_integer(value_as_words)

		move_vector = [
			value_as_number * coord\
				for coord in orientations\
					.get(orientation)
		]

		pyautogui.moveRel(*move_vector)

	@staticmethod
	async def _scroll_window(clicks: int) -> None:
		pyautogui.scroll(clicks)

	@staticmethod
	async def _click(command: str) -> None:
		command = command.split()[:-1] if\
			"раз" in command else command

		if "правой" in command:
			command = command.replace(
                "правой ", "", 1
            )
			button = "right"
		else:
			command = command.replace(
				"левой ", "", 1
			)
			button = "left"
		
		amount = 1 if command == ""\
			else to_integer(command)

		for _ in range(to_integer(amount)):
			pyautogui.click(button=button)
