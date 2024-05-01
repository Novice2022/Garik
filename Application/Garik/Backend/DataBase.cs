using Npgsql;
using System.Collections.ObjectModel;
using Garik.Models;

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

        public ObservableCollection<Message> getMessages()
        {
            return [.. messagesSelect("SELECT * FROM messages")];
        }

        private List<Message> messagesSelect(string request)
        {
            List<Message> result = new List<Message>();

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

        public void messagesInsert(string content, bool from_client, string handling_model_type, int response_for_message_id)
        {
            using (
                var cmd = new NpgsqlCommand(
                    $"INSERT INTO messages (content, from_client, handling_model_type, response_for_message_id) VALUES ('{content}', {from_client}, '{handling_model_type}', {response_for_message_id})",
                    connection
                )
            )
                cmd.ExecuteNonQuery();
        }

        public void setDefaultHistory()
        {
            using (
                var cmd = new NpgsqlCommand(
                    "DELETE FROM messages WHERE message_id > 4;",
                    connection
                )
            )
                cmd.ExecuteNonQuery();
        }

        public Dictionary<string, string> getSettings()  // TODO: read settings table and convert tuples to dict<str, str>
        {
            Dictionary<string, string> settings = new Dictionary<string, string>();

            return settings;
        }

        public void closeConnection() { connection.Close(); }
    }
}
