import pyttsx3
from metaclasses.singleton import MetaSingleton

from voice.interaction import VoiceInteraction


class Output(metaclass=MetaSingleton):
    def __init__(self) -> None:
        self._engine = pyttsx3.init()
        self._engine.setProperty(
            "voice",
            self._engine.getProperty('voices')[2].id
        )

    async def say(self, text: str) -> None:
        if VoiceInteraction.get_voice():
            self._engine.say(text)
            self._engine.runAndWait()

    async def exit(self) -> None:
        self._engine.stop()
