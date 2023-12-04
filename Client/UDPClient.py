import socket
import datetime

class UDPClient:
    def __init__(self, server_address=('localhost', 20001), buffer_size=1024):
        self.server_address = server_address
        self.buffer_size = buffer_size
        self.setup_socket()

    def setup_socket(self):
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def send_message(self, data_type, protocol, status, client_id):
        current_time = datetime.datetime.now().strftime("%y%m%d%H%M%S")
        message = f">DATA{data_type},{protocol},{current_time},{status};ID={client_id}<"
        bytes_to_send = str.encode(message)

        print(f"Enviando mensagem para o servidor: {message}")
        self.UDPClientSocket.sendto(bytes_to_send, self.server_address)

    def receive_message(self):
        msg_from_server = self.UDPClientSocket.recvfrom(self.buffer_size)
        return msg_from_server[0].decode()

if __name__ == "__main__":
    udp_client = UDPClient()

    # Envia mensagem para o servidor no formato desejado
    data_type = 1
    protocol = 66
    status = 1
    client_id = 123
    udp_client.send_message(data_type, protocol, status, client_id)

    # Recebe a resposta do servidor
    msg_from_server = udp_client.receive_message()

    print(f"Resposta do servidor: {msg_from_server}")
