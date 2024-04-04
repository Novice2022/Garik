using System.Windows;
using System.Windows.Input;
using System.Windows.Navigation;

namespace Garik
{
    public class MyCommand
    {
        private Action<object> action;

        public MyCommand(Action<object> action)
        {
            this.action = action;
        }

        public void Execute()
        {
            this.action(null);
        }
    }

    public struct MessagesTable
	{
		public int message_id { get; }
		public int response_for_message_id { get; }
		public bool from_client { get; }
		public string content { get; }
		public string handling_model_type { get; }
		public DateTime sending_datetime { get; }

		public MessagesTable(int message_id = -1, string content = "", bool from_client = true, DateTime sending_datetime = new DateTime(), string handling_model_type = "", int response_for_message_id = -1)
		{
			this.message_id = message_id;
			this.response_for_message_id = response_for_message_id;
			this.from_client = from_client;
			this.content = content;
			this.handling_model_type = handling_model_type;
			this.sending_datetime = sending_datetime;
		}
	}

	public class Message
	{
		private int response_for_message_id { get; }

		public string content { get; }
		public string sending_datetime { get; }
		public string handling_model_type { get; }
		public string alignment { get { return (from_client ? "Right" : "Left"); } }
		public bool from_client { get; }
		public int message_id { get; }
		public int indent { get { return (from_client ? 2 : 1); } }

		public delegate void CopyMessage();

        public Message(
			int message_id,
			string content,
			bool from_client,
			DateTime sending_datetime,
			string handling_model_type,
			int response_for_message_id
		) {
			this.message_id = message_id;
			this.content = content;
			this.from_client = from_client;
			this.sending_datetime = sending_datetime.ToString();
			this.handling_model_type = handling_model_type;
			this.response_for_message_id = response_for_message_id;
		}

		public Message(MessagesTable obj)
		{
			message_id = obj.message_id;
			content = obj.content;
			from_client = obj.from_client;
			sending_datetime = obj.sending_datetime.ToString();
			handling_model_type = obj.handling_model_type;
			response_for_message_id = obj.response_for_message_id;
		}

        public void copy(string content)
        {
            MessageBox.Show($"Copying to clipboard: \"{content}\"", $"Previous value: {Clipboard.GetText()}");
            Clipboard.SetText(content);
        }
    }
}
