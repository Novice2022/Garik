skills = """
Пока я могу следующее:
    * открывать браузер по определённому запросу
    * запускать приложения
    * эмулировать работу мышки и клавиатуры
"""

how_to = """
Правила общения со мной:
    * ("найди", "включи", "покажи") [запрос]:
        - я открою браузер по твоему запросу
    * ("запусти", "открой") [название приложения]:
        - я открою приложение
    * ("перемести курсор", "скопируй", "вырежи", "вставь", "нажми",
       "введи", "удали", "выдели", "...") [текст/клавиша]:
        - я сэмулирую действие на клавиатуре соответственно запросу
    * ("подними", "опусти", "перемести мышку", "кликни", "...") [дополнение команды]:
        - я сэмулирую работу мышки
    * "красный":
        - я выключусь и пожелаю всего доброго
        
"""

# class GarikInfo:
#     def __init__(self, status: str) -> None:
#         if status == "offline":
#             self.status = "offline"
#             self.__skills_property = offline_skills
#             self.__how_to_property = offline_how_to
#         else:
#             self.status = "online"
#             self.__skills_property = online_skills
#             self.__how_to_property = online_how_to
    
#     def switch_status(self) -> None:
#         if self.status == "offline":
#             self.status == "online"
#             self.__skills_property = online_skills
#             self.__how_to_property = online_how_to
#         else:
#             self.status == "offline"
#             self.__skills_property = offline_skills
#             self.__how_to_property = offline_how_to

#     @property
#     def skills(self) -> str:
#         return self.__skills_property
    
#     @property
#     def how_to(self) -> str:
#         return self.__how_to_property
