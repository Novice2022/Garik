import asyncio
from os import system

async def tcp_client():
    system("cls")
    while True:
        reader, writer = await asyncio.\
            open_connection('127.0.0.1', 8888)

        message = input("[in]\t")

        while message in (
            "cls",
            "clear"
        ):
            system("cls")
            message = input("[in]\t")

        writer.write(message.encode())

        data = await reader.read(100)
        print(f'[out]\t{data.decode()}')

        writer.close()

asyncio.run(tcp_client())

"""
python "C:/Projects/Garik/Model/testing/client_testing_socket.py"
"""
