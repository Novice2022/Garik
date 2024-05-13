using System.Net.Sockets;
using System.Reflection.Metadata;
using System.Text;
using System.Windows;

namespace Garik.Backend
{
    public partial class ClientSocket
    {
        private string serverAddress = "127.0.0.1";
        private int port = 8888;

        async public Task<string> SendMessage(string message)
        {
            string responseMessage;

            using (TcpClient client = new TcpClient())
            {
                await client.ConnectAsync(serverAddress, port);
                NetworkStream stream = client.GetStream();

                byte[] data = Encoding.UTF8.GetBytes(message);

                await stream.WriteAsync(data, 0, data.Length);

                byte[] responseData = new byte[4096];
                int bytesRead = await stream.ReadAsync(responseData, 0, responseData.Length);
                responseMessage = Encoding.UTF8.GetString(responseData, 0, bytesRead);
            }

            return responseMessage;
        }
    }
}
