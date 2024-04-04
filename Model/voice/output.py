import pyttsx3


class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if not (cls in cls._instances):
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Output(metaclass=MetaSingleton):
    def __init__(self) -> None:
        self._engine = pyttsx3.init()
        self._engine.setProperty(
            "voice",
            self._engine.getProperty('voices')[2].id
        )

    def say(self, text: str) -> None:
        self._engine.say(text)
        self._engine.runAndWait()

    def exit(self) -> None:
        self._engine.stop()
