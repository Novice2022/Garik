from sys import argv
import asyncio
from models.loops import LoopsManager
from api_server.server import ServerSocket
from datetime import datetime as dt
from os import system


class Garik:
    def __init__(self) -> None:
        print(f"[start__init]\t<{dt.now()}>")
        self.__loops_manager = LoopsManager()
        self.__server_socket = ServerSocket(
            self.__loops_manager.processing_method
        )
    
    async def run(self) -> None:
        await self.__server_socket.serve()


# async def main(args: list[str]) -> None:
#     if args[0] == "start":
#         garik = Garik()

#         await garik.run()


# if __name__ == "__main__":
#     asyncio.run(main(argv[1:]))


async def main() -> None:
    system("cls")
    garik = Garik()
    await garik.run()


if __name__ == "__main__":
    asyncio.run(main())

# python manager.py start
