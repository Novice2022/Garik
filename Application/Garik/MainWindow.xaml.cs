using System.Windows;
using System.Windows.Input;
using System.Windows.Media.Imaging;
using System.Collections.ObjectModel;

namespace Garik
{
	public partial class MainWindow : Window
	{
		// private ClientSocket client;

		private bool maximised = false;
        private int last_message_index = 0;
        private DataBase database = new DataBase();

        public ObservableCollection<Message> messages { get; set; }
        
        public MainWindow()
		{
			InitializeComponent();

            messages = database.getMessages();

			last_message_index = messages.Count();

            DataContext = this;

            // Process process = new Process();
            // 
            // process.StartInfo.FileName = "python";
            // process.StartInfo.Arguments = "C:/Projects/Garik/Model/manager.py start";
            // 
            // process.StartInfo.UseShellExecute = false;
            // // process.StartInfo.UseShellExecute = true;
            // // process.StartInfo.RedirectStandardOutput = true;
            // 
            // process.Start(); // Запускаем процесс
			// 
            // client = new ClientSocket();
			// 
            // process.WaitForExit();
        }

		private void WindowDragDrop (object sender, MouseButtonEventArgs e)
        {
			if (maximised)
				WindowState = WindowState.Normal;

			DragMove();
        }

		private void wrapGarik(object sender, MouseEventArgs e)
		{
			WindowState = WindowState.Minimized;
		}

		private void fullscreenGarik(object sender, MouseButtonEventArgs e)
		{
			if (maximised)
			{
				WindowState = WindowState.Normal;
                fullscreenImage.Source = new BitmapImage(new Uri("C:\\Projects\\Garik\\Application\\Garik\\Resources\\Logos\\fullscreen.png", UriKind.RelativeOrAbsolute));
            }
			else
			{
				WindowState = WindowState.Maximized;
                fullscreenImage.Source = new BitmapImage(new Uri("C:\\Projects\\Garik\\Application\\Garik\\Resources\\Logos\\exit-fullscreen.png", UriKind.RelativeOrAbsolute));
            }

            maximised = !maximised;
		}

		private void closeGarik(object sender, MouseEventArgs e)
		{
			database.closeConnection();
			Close();
		}
		
		private void clearHistory(object sender, MouseEventArgs e)
		{
            database.setDefaultHistory();
			messages.Clear();

			foreach (var message in database.getMessages())
				messages.Add(message);

			last_message_index = 4;
		}

        private void SendCommand(object sender, RoutedEventArgs e)
		{
			string command = new string(CommandTextBox.Text);
			bool is_user_message = true;
			
			if (command == "" || command == "/")
			{
				CommandTextBox.Text = "";
				return;
            }

			if (command[0] == '/')
			{
                command = command.Substring(1);
				is_user_message = false;
			}

			database.messagesInsert(command, is_user_message, "text", -1);

            messages.Add(
                new Message(
                    last_message_index,
                    command,
                    is_user_message,
                    DateTime.Now,
                    "text",
                    -1
                )
            );

			last_message_index++;

			CommandTextBox.Text = "";

            // client.SendMessage(CommandTextBox.Text);
        }

        private void CommandTextBox_KeyDown(object sender, KeyEventArgs e)
        {
			if (e.Key == Key.Enter)
				SendCommand(sender, new RoutedEventArgs());
        }
		
		public void textInputCheckBoxClick(object sender, RoutedEventArgs e)
		{
			MessageBox.Show("textInputCheckBoxClick");
		}

        public void voiceInputCheckBoxClick(object sender, RoutedEventArgs e)
		{
            MessageBox.Show("voiceInputCheckBoxClick");
        }

		public void textOutputCheckBoxClick(object sender, RoutedEventArgs e)
		{
            MessageBox.Show("textOutputCheckBoxClick");
        }

		public void voiceOutputCheckBoxClick(object sender, RoutedEventArgs e)
		{
            MessageBox.Show("voiceOutputCheckBoxClick");
        }

        private void offlineCheckBoxClick(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("offlineCheckBoxClick");
        }

        private void onlineCheckBoxClick(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("onlineCheckBoxClick");
        }
    }
}
