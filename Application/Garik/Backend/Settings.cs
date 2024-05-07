using Newtonsoft.Json;
using System.IO;

namespace Garik.Backend
{
	internal class Settings
	{
		private Dictionary<string, string> json;
		public string FastRecognition;
		public string Voice;

        public string NotFastRecognition
		{
			get
			{
				if (FastRecognition == "True")
					return "False";
				return "True";
			}
		}

		public Settings() {
			json = GetJSON();
			UpdateSettings();
		}
		
		public static Dictionary<string, string> GetJSON(string filepath = "C:\\Projects\\Garik\\Model\\user_settings.json")
		{
			using (StreamReader sr = new StreamReader(filepath))
				return JsonConvert.DeserializeObject<Dictionary<string, string>>(sr.ReadLine());
		}

		public void UpdateSettings()
		{
			json = GetJSON();

			FastRecognition = json["fast-recognition"];
			Voice = json["voice"];
        }
	}
}
