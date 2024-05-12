using Garik.Backend;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace Garik.Models
{
	public class ApplicationsSettings : INotifyPropertyChanged
	{
		private static ClientSocket client = new ClientSocket();

		public static ObservableCollection<ApplicationHandler> Applications { get; set; } = new ObservableCollection<ApplicationHandler>();  //  = [new ApplicationHandler("Яндекс Музыка"), new ApplicationHandler("Binance")];

        public static void ShowApplication(ApplicationHandler app)
		{
			Applications.Add(app);
        }

		public static void AddApplication(ApplicationHandler app)
		{
			Task.Run(async () => await client.SendMessage($"custom add-app {app.AppName} ~ {app.FilePath}"));
			Applications.Remove(app);
        }

		public static void RemoveApplication(ApplicationHandler app)
		{
			Applications.Remove(app);
        }

		public event PropertyChangedEventHandler PropertyChanged;

		public void OnPropertyChanged([CallerMemberName] string prop = "")
		{
			PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(prop));
		}
	}
}
