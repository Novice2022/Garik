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

        private void closeGarik(object sender, MouseEventArgs e)
        {
            Close();
        }
    }
}
