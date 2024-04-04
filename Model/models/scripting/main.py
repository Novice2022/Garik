from project_typing import OfflineVoiceModel, OnlineVoiceModel

class Core:
    def __init__(self, instanse: OfflineVoiceModel | OnlineVoiceModel) -> None:
        self.__parent_instanse = instanse

    def execute(self, script: list[str]) -> None:
        for command in script:
            self.__parent_instanse.manage_command(command)
