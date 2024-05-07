using Npgsql;
using System.Collections.ObjectModel;
using Garik.Models;
using System.Windows;

namespace Garik.Backend
{
    class DataBase
    {
        private NpgsqlConnection connection;

        public DataBase()
        {
            string connString = "Host=127.0.0.1;Username=postgres;Password=VPS-Ser;Database=garik";
            connection = new NpgsqlConnection(connString);
            connection.Open();
        }

        public ObservableCollection<Message> SelectMessages(string request = "SELECT * FROM messages")
        {
            ObservableCollection<Message> result = new ObservableCollection<Message> ();

            using (var cmd = new NpgsqlCommand(request, connection))
            using (var reader = cmd.ExecuteReader())
                while (reader.Read())
                    result.Add(
                        new Message(
                            reader.GetInt32(0),
                            reader.GetString(1),
                            reader.GetBoolean(2),
                            reader.GetDateTime(3),
                            reader.GetString(4),
                            reader.GetInt32(5)
                        )
                    );

            return result;
        }

        public void InsertMessage(string content, bool fromClient, string handlingModelType, int responseForMessageID)
        {
            using (
                var cmd = new NpgsqlCommand(
                    $"INSERT INTO messages (message_content, from_client, handling_model_type, response_for_message_id) VALUES ('{content}', {fromClient}, '{handlingModelType}', {responseForMessageID})",
                    connection
                )
            )
                cmd.ExecuteNonQuery();
        }

        public void SetDefaultHistory()
        {
            using (
                var cmd = new NpgsqlCommand(
                    "DELETE FROM messages WHERE message_id > 4;",
                    connection
                )
            )
                cmd.ExecuteNonQuery();
        }

        public Dictionary<string, string> GetSettings()  // TODO: read settings table and convert tuples to dict<str, str>
        {
            Dictionary<string, string> settings = new Dictionary<string, string>();

            return settings;
        }

        public void CloseConnection() { connection.Close(); }
    }
}
