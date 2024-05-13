using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Collections.ObjectModel;
using Garik.Models;
using Garik.Backend;
using System.Diagnostics;
using System.Windows;

namespace Garik.ViewModels
{
	class ViewModel : INotifyPropertyChanged
	{
		// <>-----------------------------<> Custom <>-----------------------------<>

		private ClientSocket client = new ClientSocket();
		private Settings settings = new Settings();
		private DataBase database = new DataBase();
		private Process process = new Process();

		public ObservableCollection<Message> Messages { get; set; }
		public ObservableCollection<ApplicationHandler> ApplicationsPanel
		{
			get { return ApplicationsSettings.Applications; }
			set
			{
				ApplicationsSettings.Applications = value;
			}
		}

		private int lastMessageIndex = 0;

		private string inputContent = "";
		private string sendButtonEnabled = "Hidden";

		private string windowState = "Normal";
		private string windowStateButtonIcon = "M 30 30 L 70 30 L 70 70 L 30 70 M 35 35 L 65 35 L 65 65 L 35 65 Z";

		private string previousVoiceModel = "";


		public string IsEnabledListenButton
		{
			get
			{
				if (interactionMode == "Текстовый режим")
					return "True";
				return "False";
			}
		}


		private string interactionMode = "Текстовый режим";
		public string InteractionMode
		{
			get { return interactionMode; }
			set
			{
				interactionMode = value;
				OnPropertyChanged("InteractionMode");
				OnPropertyChanged("IsEnabledListenButton");
			}
		}


		private string voiceNotificationContent = "Нажмите на кнопку с микрофоном слева снизу, чтобы я Вас начал слушать";
		public string VoiceNotificationContent
		{
			get { return voiceNotificationContent; }
			set
			{
				voiceNotificationContent = value;
				OnPropertyChanged("VoiceNotificationContent");
			}
		}


		private string isEnabledOnlineVoice;
		public string IsEnabledOnlineVoice
		{
			get { return isEnabledOnlineVoice; }
			set
			{
				isEnabledOnlineVoice = value;
				OnPropertyChanged("IsEnabledOnlineVoice");
			}
		}


		private string isEnabledOfflineVoice;
		public string IsEnabledOfflineVoice
		{
			get { return isEnabledOfflineVoice; }
			set
			{
				isEnabledOfflineVoice = value;
				OnPropertyChanged("IsEnabledOfflineVoice");
			}
		}


		private string voiceCheckBoxState;
		public string VoiceCheckBoxState
		{
			get { return voiceCheckBoxState; }
			set
			{
				voiceCheckBoxState = value;
				OnPropertyChanged("VoiceCheckBoxState");
			}
		}


		public string WindowState
		{
			get { return windowState; }
			set
			{
				windowState = value;
				OnPropertyChanged("WindowState");
			}
		}

		public string WindowStateButtonIcon
		{
			get { return windowStateButtonIcon; }
			set
			{
				windowStateButtonIcon = value;
				OnPropertyChanged("WindowStateButtonIcon");
			}
		}


		public string InputContent
		{
			get { return inputContent; }
			set
			{
				inputContent = value;

				if (value == "")
					SendButtonEnabled = "Hidden";
				else
					SendButtonEnabled = "Visible";

				OnPropertyChanged("InputContent");
			}
		}

		public string SendButtonEnabled
		{
			get { return sendButtonEnabled; }
			set
			{
				sendButtonEnabled = value;
				OnPropertyChanged("SendButtonEnabled");
			}
		}


		public ViewModel()
		{
			process.StartInfo.FileName = "python";
			process.StartInfo.Arguments = "C:/Projects/Garik/Model/manager.py start";
			process.StartInfo.UseShellExecute = true;
			process.StartInfo.WindowStyle = ProcessWindowStyle.Hidden;

			process.Start();
			Thread.Sleep(2500);

			Messages = database.SelectMessages();
			Messages.Last().MarginBottom = "10";

			lastMessageIndex = Messages.Count();

			voiceCheckBoxState = settings.Voice;
			isEnabledOfflineVoice = settings.FastRecognition;
			isEnabledOnlineVoice = settings.NotFastRecognition;

			if (isEnabledOfflineVoice == "True")
				previousVoiceModel = "offline";
			else
				previousVoiceModel = "online";
		}


		// <>------------------------------<> MVVM <>------------------------------<>

		public event PropertyChangedEventHandler PropertyChanged;
		public void OnPropertyChanged([CallerMemberName] string prop = "")
		{
			PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(prop));
		}


		// <>----------------------------<> Actions  <>----------------------------<>

		private AsyncRelayCommand sendMessage;
		public AsyncRelayCommand SendMessage
		{
			get
			{
				return sendMessage ?? (
					sendMessage = new AsyncRelayCommand(async (obj) => await callServer(obj as string))
				);
			}
		}

		async private Task callServer(string? parameter)
		{
			if (parameter == "shutdown" || parameter.StartsWith("custom"))
				await client.SendMessage(parameter);
			else if (parameter.StartsWith("text"))
			{
				lastMessageIndex++;

				// Messages.Last().MarginBottom = "0";
				Messages.Add(
					new Message(
						lastMessageIndex,
						inputContent,
						true,
						DateTime.Now,
						"text",
						-1
					)
				);
				Messages.Last().MarginBottom = "10";
				database.InsertMessage(lastMessageIndex, inputContent, true, "text", -1);

				string responseMessage = await client.SendMessage($"{parameter} {inputContent}");
				InputContent = "";

				await handleResponse(responseMessage);
			}
			else if (parameter == "listen")
			{
				bool listenUntilStop = false;

				do
				{
					InteractionMode = "Голосовой режим | Текстовые запросы ожидают своей очереди";
					VoiceNotificationContent = "Чтобы я слушал Вас, пока не остановите, скажите \"[Гарик,] прислушивайся\", или \"[Гарик,] работаем\", или \"[Гарик,] слушай пока не остановлю\"";
					string responseMessage = await client.SendMessage("listen");

					if (responseMessage.StartsWith("voice-error"))
					{
						await handleResponse("voice-error");
						return;
					}

					string voiceRequest = responseMessage.Substring(0, responseMessage.IndexOf(" ~ "));
					responseMessage = responseMessage.Substring(voiceRequest.Length + 3);

					if (voiceRequest != "")
						switch (responseMessage)
						{
							case "listening-until-stop":
								listenUntilStop = true;
								InteractionMode = "Голосовой режим | Текстовые запросы ожидают своей очереди";
								VoiceNotificationContent = "Слушаю, пока не скажете \"[Гарик,] отдыхай\"";
								break;
							case "stop-listen":
								listenUntilStop = false;
								break;
							default:
								lastMessageIndex++;

								Messages.Last().MarginBottom = "0";
								Messages.Add(
									new Message(
										lastMessageIndex,
										voiceRequest,
										true,
										DateTime.Now,
										"text",
										-1
									)
								);
								Messages.Last().MarginBottom = "10";
								database.InsertMessage(lastMessageIndex, voiceRequest, true, "voice", -1);

                                await handleResponse(responseMessage);
								break;
						}
				} while (listenUntilStop);

				InteractionMode = "Текстовый режим";
				VoiceNotificationContent = "Нажмите на кнопку с микрофоном слева снизу, чтобы я Вас начал слушать";
			}
		}

		async private Task handleResponse(string response)
		{
			if (response == "can\'t understand")
				response = "Не знаю как выполнить Ваш запрос :(";
			else if (response.StartsWith("start-app add-to-settings"))
			{
				string applicationName = response.Replace("start-app add-to-settings ", "");
				ApplicationsSettings.ShowApplication(new ApplicationHandler(applicationName));
				response = $"Укажите путь до приложения \"{applicationName}\", чтобы я мог его запустить.";
			}
			else if (response.StartsWith("start-app"))
			{
				string command = response.Replace("start-app ", "");
				string requestedApplication = command.Split(" ~ ")[0];
				command = command.Substring(command.IndexOf(" ~ ") + 3);

				response = $"Запустил: \"{requestedApplication}\"";

				if (command.Contains(" ~ "))
				{
					Process process = new Process();
					process.StartInfo.FileName = command.Split(" ~ ")[0];
					process.StartInfo.Arguments = command.Substring(command.IndexOf(" ~ ") + 3).Replace(" ~ ", " ");
					process.Start();
				}
				else
					Process.Start(command);
			}
			else if (response == "voice-error")
				response = "Не удалось распознать речь";
			else if (response.StartsWith("browse ok"))
				response = $"Нашёл для Вас: {response.Substring(10)}";

			lastMessageIndex++;
			database.InsertMessage(lastMessageIndex, response, false, "text", lastMessageIndex - 1);

			Messages.Last().MarginBottom = "0";
			Messages.Add(
				new Message(
					lastMessageIndex,
					response,
					false,
					DateTime.Now,
					"text",
					lastMessageIndex - 1
				)
			);
			Messages.Last().MarginBottom = "10";
		}


		private RelayCommand clearHistory;
		public RelayCommand ClearHistory
		{
			get
			{
				return clearHistory ??
					(clearHistory = new RelayCommand(obj =>
					{
						database.SetDefaultHistory();
						Messages.Clear();

						lastMessageIndex = 4;
					}));

			}
		}


		private AsyncRelayCommand custom;
		public AsyncRelayCommand Custom
		{
			get
			{
				return custom ?? (
					custom = new AsyncRelayCommand(
						async obj => await sendCustomMessage(obj as string)
					)
				);
			}
		}

		async private Task sendCustomMessage(string? parameter)
		{
			if (parameter == "voice")
			{
				SendMessage.Execute("custom voice");
				return;
			}

			string? suffix = parameter.Substring(0, parameter.IndexOf(' '));

			if (
				(suffix == "to-offline" && previousVoiceModel == "online") ||
				(suffix == "to-online" && previousVoiceModel == "offline")
			)
			{
				previousVoiceModel = suffix.Split("-").ToList()[1];
				SendMessage.Execute("custom switch");
			}
		}

		private RelayCommand openSettingsFile;

		public RelayCommand OpenSettingsFile
		{
			get
			{
				return openSettingsFile ?? (
					openSettingsFile = new RelayCommand(
						obj => {
							Process.Start("notepad", "C:\\Projects\\Garik\\Model\\applications.json");
						}
					)
				);
			}
		}


		private RelayCommand createApplication;
		public RelayCommand CreateApplication
		{
			get
			{
				return createApplication ?? (
					createApplication = new RelayCommand(obj =>
					{
						ApplicationsSettings.ShowApplication(new ApplicationHandler());
					})
				);
			}
		}


		// <>-------------------------<> Window Actions <>-------------------------<>

		private RelayCommand switchWindowState;
		public RelayCommand SwitchWindowState
		{
			get
			{
				return switchWindowState ??
					(switchWindowState = new RelayCommand(obj =>
					{
						if (windowState == "Maximized")
						{
							WindowState = "Normal";
							WindowStateButtonIcon = "M 30 30 L 70 30 L 70 70 L 30 70 M 35 35 L 65 35 L 65 65 L 35 65 Z";
						}
						else
						{
							WindowState = "Maximized";
							WindowStateButtonIcon = "M 20,20 L 45,20 L 45,25 L 25,25 L 25,45 L 20,45 M 55,20 L 80,20 L 80 45 L 75 45 L 75 25 L 55 25 M 75 55 L 80 55 L 80 80 L 55 80 L 55 75 L 75 75 M 20 55 L 25 55 L 25 75 L 45 75 L 45 80 L 20 80 Z";
						}
					}));
			}
		}


		private RelayCommand wrapWindow;
		public RelayCommand WrapWindow
		{
			get
			{
				return wrapWindow ??
					(wrapWindow = new RelayCommand(obj =>
					{
						WindowState = "Minimized";
					}));
			}
		}


		private AsyncRelayCommand closeGarik;
		public AsyncRelayCommand CloseGarik
		{
			get
			{
				return closeGarik ??
					(closeGarik = new AsyncRelayCommand(async obj => await sendShutdownMessage()));
			}
		}

		async private Task sendShutdownMessage()
		{
			database.CloseConnection();
			SendMessage.Execute("shutdown");
			process.Close();
			Application.Current.Shutdown();
		}
	}
}
