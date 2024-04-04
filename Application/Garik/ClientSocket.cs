using System.Net.Sockets;
using System.Text;

namespace Garik
{
    public partial class ClientSocket
    {
        async public Task SendMessage(string message)
        {
            string serverAddress = "127.0.0.1";
            int port = 8888;

            TcpClient client = new TcpClient();
            await client.ConnectAsync(serverAddress, port);

            NetworkStream stream = client.GetStream();

            byte[] data = Encoding.UTF8.GetBytes(message);

            await stream.WriteAsync(data, 0, data.Length);

            byte[] responseData = new byte[1024];
            int bytesRead = await stream.ReadAsync(responseData, 0, responseData.Length);
            string responseMessage = Encoding.UTF8.GetString(responseData, 0, bytesRead);

            await HandleResponse(responseMessage);

            client.Close();
        }

        async private Task HandleResponse(string response)
        {
            Console.WriteLine($"Received: {response}");
        }
    }
}
