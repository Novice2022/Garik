from typing import Coroutine
import asyncio
from notifypy import Notify


# def send_message(title: str = "", message: str = "") -> None:
# 	Notify().send_notification(supplied_title=title, message=message)


class ServerSocket:
	def __init__(
		self,
		command_processing_method: Coroutine = None
	) -> None:
		if command_processing_method != None:
			self.__processing_method = command_processing_method
		else:
			self.__processing_method = self.__echo


	async def __async_processing(
		self,
		reader: asyncio.StreamReader,
		writer: asyncio.StreamWriter
	) -> None:
		try:
			bytes_message = await reader.read(512)
			message = bytes_message.decode(encoding="utf-8")

			log_message = f"{message} from {writer.get_extra_info('peername')}" if message != "красный" else ""

			print(log_message)

			process_result = await self.__processing_method(message)

			writer.write(process_result.encode(encoding="utf-8"))

			await writer.drain()
			writer.close()
		except OSError:
			print("Excepting \"OSError: [WinError 64]\" - Client process closed")


	async def serve(self) -> None:
		self.__server = await asyncio.start_server(
			self.__async_processing,
			'127.0.0.1',
			8888
		)

		addr = self.__server.sockets[0].getsockname()
		print(f'Serving on {addr}')

		async with self.__server:
			await self.__server.serve_forever()
	

	async def __echo(self, message: str) -> str:
		print(f"got: \"{message}\" | recieved: \"{message.upper()}\"")
		return message.upper()
