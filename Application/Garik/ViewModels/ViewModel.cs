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

		private ClientSocket client;
		private DataBase database = new DataBase();
		
		private bool maximised = false;
		private int lastMessageIndex = 0;

		private string inputContent;

        public string InputContent
		{
			get { return inputContent; }
			set
			{
                inputContent = value;

				if (value.EndsWith("\n") && SendCommand.CanExecute(null))
					SendCommand.Execute(inputContent);
			}
		}

		// <>------------------------------<> MVVM <>------------------------------<>

		public ObservableCollection<Message> Messages;

		public event PropertyChangedEventHandler PropertyChanged;

		public void OnPropertyChanged([CallerMemberName]string prop = "")
		{
			PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(prop));
		}

		public ViewModel()
		{
			Messages = database.getMessages();
			lastMessageIndex = Messages.Count();

			Process process = new Process();
			
			process.StartInfo.FileName = "python";
			process.StartInfo.Arguments = "\"C:/Projects/Garik/Model/manager.py\" start";
			
			process.StartInfo.UseShellExecute = false;
			// process.StartInfo.UseShellExecute = true;
			// process.StartInfo.RedirectStandardOutput = true;
			
			process.Start();
			
			client = new ClientSocket();
			
			process.WaitForExit();

		}

		private RelayCommand sendCommand;

		public RelayCommand SendCommand
		{
			get
			{
				return sendCommand ??
					(sendCommand = new RelayCommand(obj =>
					{
						MessageBox.Show($"Called SendCommand with {inputContent} parameter");
					},
					(obj => inputContent is not null && inputContent != "")
					));
			}
		}


		//              private void SendCommand(object sender, RoutedEventArgs e)
		//              {
		//                  string command = new string(CommandTextBox.Text);
		//                  bool is_user_message = true;
		//              
		//                  if (command == "" || command == "/")
		//                  {
		//                      CommandTextBox.Text = "";
		//                      return;
		//                  }
		//              
		//                  if (command[0] == '/')
		//                  {
		//                      command = command.Substring(1);
		//                      is_user_message = false;
		//                  }
		//              
		//                  database.messagesInsert(command, is_user_message, "text", -1);
		//              
		//                  messages.Add(
		//                      new Message(
		//                          last_message_index,
		//                          command,
		//                          is_user_message,
		//                          DateTime.Now,
		//                          "text",
		//                          -1
		//                      )
		//                  );
		//              
		//                  last_message_index++;
		//              
		//                  CommandTextBox.Text = "";
		//              
		//                  // client.SendMessage(CommandTextBox.Text);
		//              }
		//              
		//              private void CommandTextBox_KeyDown(object sender, KeyEventArgs e)
		//              {
		//                  if (e.Key == Key.Enter)
		//                      SendCommand(sender, new RoutedEventArgs());
		//              }

		private RelayCommand textInputCheckBoxClick;

        public RelayCommand TextInputCheckBoxClick 
		{
			get
			{
				return new RelayCommand(obj => 
				{
					MessageBox.Show("TextBox");
				});
			}
		}

		private RelayCommand voiceInputCheckBoxClick;

		public RelayCommand VoiceInputCheckBoxClick
		{
			get
			{
				return new RelayCommand(obj => 
				{
					MessageBox.Show("TextBox");
				});
			}
		}

		private RelayCommand textOutputCheckBoxClick;

		public RelayCommand TextOutputCheckBoxClick
		{
			get
			{
				return new RelayCommand(obj => 
				{
					MessageBox.Show("TextBox");
				});
			}
		}

		private RelayCommand voiceOutputCheckBoxClick;

		public RelayCommand VoiceOutputCheckBoxClick
		{
			get
			{
				return new RelayCommand(obj => 
				{
					MessageBox.Show("TextBox");
				});
			}
		}

		private RelayCommand offlineCheckBoxClick;

		private RelayCommand OfflineCheckBoxClick
		{
			get
			{
				return new RelayCommand(obj => 
				{
					MessageBox.Show("TextBox");
				});
			}
		}

		private RelayCommand onlineCheckBoxClick;

		private RelayCommand OnlineCheckBoxClick
		{
			get
			{
				return new RelayCommand(obj => {
					MessageBox.Show("TextBox");
				});
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
						database.setDefaultHistory();
						Messages.Clear();

						foreach (var message in database.getMessages())
							Messages.Add(message);

						lastMessageIndex = 4;
					}));

			}
		}
	}
}
