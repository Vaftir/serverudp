import socket
import datetime
import random
import time

class UDPSimulator:
    def __init__(self, server_address=('localhost', 20001), buffer_size=1024):
        self.server_address = server_address
        self.buffer_size = buffer_size
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def generate_random_data(self):
        data_type = random.choice([1, 2])
        protocol = random.choice([66, 67, 68])
        current_time = datetime.datetime.now().strftime("%y%m%d%H%M%S")
        status = random.choice([0, 1])
        client_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=3))

        return f">DATA{data_type},{protocol},{current_time},{status};ID={client_id}<"

    def send_random_data(self):
        random_data = self.generate_random_data()
        bytes_to_send = str.encode(random_data)
        print(f"Enviando pacote para o servidor: {random_data}")
        self.UDPClientSocket.sendto(bytes_to_send, self.server_address)

    def run(self):
        while True:
            self.send_random_data()
            time.sleep(5)

if __name__ == "__main__":
    udp_simulator = UDPSimulator()

    try:
        udp_simulator.run()
    except KeyboardInterrupt:
        print("Simulador interrompido.")
