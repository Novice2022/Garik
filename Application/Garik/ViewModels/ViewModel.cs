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

		private int lastMessageIndex = 0;

		private string inputContent = "";
		private string sendButtonEnabled = "Hidden";

		private string windowState = "Normal";
		private string windowStateButtonIcon = "M 30 30 L 70 30 L 70 70 L 30 70 M 35 35 L 65 35 L 65 65 L 35 65 Z";

		private string previousVoiceModel = "";

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

		public ObservableCollection<Message> Messages { get; set; }

		public ViewModel()
		{
			Messages = database.SelectMessages();
			Messages.Last().MarginBottom = "10";

			lastMessageIndex = Messages.Count();

			process.StartInfo.FileName = "python";
			process.StartInfo.Arguments = "C:\\Projects\\Garik\\Model\\manager.py start";
			process.StartInfo.UseShellExecute = true;
			// process.StartInfo.WindowStyle = ProcessWindowStyle.Hidden;

			process.Start();

			voiceCheckBoxState = settings.Voice;
			isEnabledOfflineVoice = settings.FastRecognition;
			isEnabledOnlineVoice = settings.NotFastRecognition;

			if (isEnabledOfflineVoice == "True")
				previousVoiceModel = "offline";
			else
				previousVoiceModel = "online";

			for (int i = 0; i < 2; i++)
				SendCommand.Execute("custom voice");
		}


		// <>------------------------------<> MVVM <>------------------------------<>

		public event PropertyChangedEventHandler PropertyChanged;
		public void OnPropertyChanged([CallerMemberName] string prop = "")
		{
			PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(prop));
		}


		// <>----------------------------<> Actions  <>----------------------------<>

		private RelayCommand sendCommand;
		public RelayCommand SendCommand
		{
			get
			{
				return sendCommand ??
					(sendCommand = new RelayCommand(obj =>
					{
						string? parameter = obj as string;

						if (parameter == "shutdown" || parameter.StartsWith("custom"))
							Task.Run(async () => await client.SendMessage(parameter));
						else if (parameter.StartsWith("text"))
						{
							Messages.Last().MarginBottom = "0";
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

							lastMessageIndex++;
							inputContent = $"{parameter} {inputContent}";

							database.InsertMessage(inputContent, true, "text", -1);

							string responseMessage = Task.Run(async () => await client.SendMessage(inputContent)).GetAwaiter().GetResult();

							Messages.Last().MarginBottom = "0";
							Messages.Add(
								new Message(
									lastMessageIndex,
									responseMessage,
									false,
									DateTime.Now,
									"text",
									-1  // Change lately to replying message ID
								)
							);
							Messages.Last().MarginBottom = "10";

							InputContent = "";
						}
						else if (parameter == "voice")
						{

						}
					}));
			}
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

						foreach (var message in database.SelectMessages())
							Messages.Add(message);

						lastMessageIndex = 4;
					}));

			}
		}


		private RelayCommand custom;
		public RelayCommand Custom
		{
			get
			{
				return custom ??
					(custom = new RelayCommand(obj =>
					{
						string? parameter = obj as string;

						//MessageBox.Show(parameter, $"\'custom {parameter.Substring(parameter.IndexOf(' ') + 1)}\'");

						if (parameter == "voice")
						{
							sendCommand.Execute("custom voice");
							return;
						}

                        string? suffix = parameter.Substring(0, parameter.IndexOf(' '));

						if (
							(suffix == "to-offline" && previousVoiceModel == "online") ||
							(suffix == "to-online" && previousVoiceModel == "offline")
						)
						{
							previousVoiceModel = suffix.Split("-").ToList()[1];
							sendCommand.Execute("custom switch");
						}
					}));
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


		private RelayCommand closeGarik;
		public RelayCommand CloseGarik
		{
			get
			{
				return closeGarik ??
					(closeGarik = new RelayCommand(obj =>
					{
						database.CloseConnection();
						SendCommand.Execute("shutdown");
						process.Close();
						Application.Current.Shutdown();
					}));
			}
		}
	}
}
