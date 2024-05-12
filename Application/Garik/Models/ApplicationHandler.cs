using System.ComponentModel;
using System.IO;
using System.Runtime.CompilerServices;

namespace Garik.Models
{
	public class ApplicationHandler : INotifyPropertyChanged
	{
		string appName;
		string filePath;

		public string PathChekerIco
		{
			get
			{
				if (File.Exists(filePath))
					return "M 15 68 L 45 88 L 85 18 L 70 12 L 42 75 L 25 57 Z";
				else
					return "M 15 25 L 25 15 L 50 45 L 75 15 L 85 25 L 55 50 L 85 75 L 75 85 L 50 55 L 25 85 L 15 75 L 45 50 Z";
			}
		}

		public string PathChekerIcoColor
		{
			get
			{
				if (File.Exists(filePath))
					return "ForestGreen";
				else
					return "Tomato";
			}
		}

		public string AppName
		{
			get { return appName; }
			set
			{
				appName = value;
				OnPropertyChanged("AppName");
			}
		}

		public string FilePath
		{
			get { return filePath; }
			set
			{
				filePath = value;
				OnPropertyChanged("FilePath");
				OnPropertyChanged("PathChekerIco");
				OnPropertyChanged("PathChekerIcoColor");
			}
		}

		private RelayCommand addApplication;
		public RelayCommand AddApplication
		{
			get
			{
				return addApplication ?? (
					addApplication = new RelayCommand(obj =>
					{
						ApplicationsSettings.AddApplication(this);
					},
					obj => File.Exists(filePath) && appName != "")
				);
			}
		}

		private RelayCommand skipApplication;
		public RelayCommand SkipApplication
		{
			get
			{
				return skipApplication ?? (
					skipApplication = new RelayCommand(obj => {
						ApplicationsSettings.RemoveApplication(this);
					}
				));
			}
		}

		public ApplicationHandler(string applicationName = "", string applicationPath = "")
		{
			appName = applicationName;
			if (applicationPath == "")
				filePath = "D://efault/pat.h";
			else
				filePath = applicationPath;
		}

		public event PropertyChangedEventHandler PropertyChanged;

		public void OnPropertyChanged([CallerMemberName] string prop = "")
		{
			PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(prop));
		}
	}
}

// C:\Projects\Garik\Application\Garik\App.xaml
