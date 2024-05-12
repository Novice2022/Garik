import json

class VoiceInteraction:
	@staticmethod
	def get_voice() -> bool:
		return VoiceInteraction.get_settings().\
			get("voice") == "True"
	

	@staticmethod
	def get_fast_recognition() -> bool:
		return VoiceInteraction.get_settings().\
			get("fast-recognition") == "True"


	@staticmethod
	def switch_voice_setting(parameter: str) -> None:
		settings = VoiceInteraction.get_settings()
		parameter = "fast-recognition"\
			if parameter == "switch" else "voice"

		settings[parameter] = "True"\
			if settings[parameter] == "False" else "False"
		VoiceInteraction.save_settings(settings)


	@staticmethod
	def get_settings() -> dict[str, str]:
		with open(
			"C:/Projects/Garik/Model/user_settings.json",
			mode='r',
			encoding='utf-8'
		) as settings:
			return json.load(settings)	


	@staticmethod
	def save_settings(new_settings: dict[str, str]) -> None:
		with open(
			"C:/Projects/Garik/Model/user_settings.json",
			mode='w',
			encoding='utf-8'
		) as file:
			json.dump(new_settings, file)
