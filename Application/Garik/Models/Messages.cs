using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace Garik.Models
{
	public struct MessagesTable
	{
		public int MessageID { get; }
		public int ResponseForMessageID { get; }
		public bool FromClient { get; }
		public string Content { get; }
		public string HandlingModelType { get; }
		public DateTime SendingDatetime { get; }

		public MessagesTable(
			int message_id = -1,
			string content = "",
			bool from_client = true,
			DateTime sending_datetime = new DateTime(),
			string handling_model_type = "",
			int response_for_message_id = -1
		) {
			MessageID = message_id;
			ResponseForMessageID = response_for_message_id;
			FromClient = from_client;
			Content = content;
			HandlingModelType = handling_model_type;
			SendingDatetime = sending_datetime;
		}
	}

	public class Message : INotifyPropertyChanged
	{
        private string content;
        private int responseForMessageID;
		private string sendingDatetime;
		private string handlingModelType;
		private bool fromClient;
		private int messageID;
		
        public string Content 
		{ 
			get { return content; }
			set 
			{
				content = value;
				OnPropertyChanged("Content");
			}
		}

        public string SendingDatetime
		{
			get { return sendingDatetime; }
			set
			{
				sendingDatetime = value;
				OnPropertyChanged("SendingDatetime");
			}
		}

		public int ResponseForMessageID
		{
			get { return responseForMessageID; }
			set 
			{
				responseForMessageID = value; 
				OnPropertyChanged("ResponseForMessageID"); 
			}
		}

        public string HandlingModelType
		{
			get { return handlingModelType; }
			set
			{
				handlingModelType = value;
				OnPropertyChanged("HandlingModelType");
			}
		}

        public bool FromClient 
		{ 
			get { return fromClient; }
			set
			{
				fromClient = value;
				OnPropertyChanged("FromClient");
			}
		}

        public int MessageID
		{
			get { return messageID; }
			set
			{
				messageID = value;
				OnPropertyChanged("Value");
			}
		}

        public string Alignment 
		{ 
			get { return (fromClient ? "Right" : "Left"); }
		}

        public int Indent 
		{ 
			get { return (fromClient ? 2 : 1); }
		}

		public Message(
			int message_id,
			string content,
			bool from_client,
			DateTime sending_datetime,
			string handling_model_type,
			int response_for_message_id
		) {
			messageID = message_id;
            this.content = content;
			fromClient = from_client;
			sendingDatetime = sending_datetime.ToString();
			handlingModelType = handling_model_type;
			responseForMessageID = response_for_message_id;
		}

		public Message(MessagesTable obj)
		{
			messageID = obj.MessageID;
			content = obj.Content;
			fromClient = obj.FromClient;
			sendingDatetime = obj.SendingDatetime.ToString();
			handlingModelType = obj.HandlingModelType;
			responseForMessageID = obj.ResponseForMessageID;
		}

		private RelayCommand copy;
		public RelayCommand Copy
		{
			get
			{
				return copy ??
					(copy = new RelayCommand(obj =>
					{
                        MessageBox.Show($"Copying to clipboard: \"{content}\"", $"Previous value: {Clipboard.GetText()}");
                        Clipboard.SetText(content);
                    }));
			}
		}

		public event PropertyChangedEventHandler PropertyChanged;

		public void OnPropertyChanged([CallerMemberName] string prop = "")
		{
			PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(prop));
		}
	}
}
