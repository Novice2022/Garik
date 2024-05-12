from typing import Coroutine
import asyncio
from datetime import datetime as dt


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

			message_owner = writer.get_extra_info('peername')

			print(
				f"[in <-- {message_owner}]\t<{dt.now()}>\t{\
					message + '\t' if message == "listen"\
						else message}" if message != "красный" else ""
			)

			process_result = await self.__processing_method(
				message,
				message_owner
			)

			writer.write(process_result.encode(encoding="utf-8"))

			await writer.drain()
			writer.close()
		except OSError:
			print(
				"Excepting \"OSError: [WinError 64]\" - Client process closed"
			)
			await self.__processing_method("shutdown")
		except AttributeError:
			await self.__processing_method("shutdown")


	async def serve(self) -> None:
		self.__server = await asyncio.start_server(
			self.__async_processing,
			"127.0.0.1",
			8888
		)

		addr = self.__server.sockets[0].getsockname()
		print(f"[finish_init]\t<{dt.now()}>\tServing on {addr}")

		async with self.__server:
			await self.__server.serve_forever()
	

	async def __echo(self, message: str) -> str:
		print(f"got: \"{message}\" | recieved: \"{message.upper()}\"")
		return message.upper()
