using Garik.ViewModels;
using System.Windows;
using System.Windows.Input;
using System.Windows.Media.Imaging;

namespace Garik
{
	public partial class MainWindow : Window
	{   
        private bool maximised = false;

        public MainWindow()
		{
			InitializeComponent();
			DataContext = new ViewModel();
        }

        private void windowDragDrop(object sender, MouseButtonEventArgs e)
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
            Close();
        }
    }
}
