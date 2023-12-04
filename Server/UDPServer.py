import socket
import json
import datetime
from firebase_admin import firestore
from firebase_admin import credentials


class UDPServer:
    def __init__(self, config_path='server/config.json'):
        self.load_config(config_path)
        self.setup_socket()
        self.connect_to_firebase()

    def load_config(self, config_path):
        with open(config_path) as config_file:
            config = json.load(config_file)

        self.localIP = config['localIP']
        self.localPort = config['localPort']
        self.bufferSize = config['bufferSize']

    #configura o socket
    def setup_socket(self):
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((self.localIP, self.localPort))
        print("Servidor UDP pronto e ouvindo")

    def run(self):
        while True:
            bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            client_msg = f"\nMensagem do Cliente: {message.decode()}"
            client_ip = f"Endereço IP do Cliente: {address}"

            print(client_msg)
            print(client_ip)

            parsed_data = self.parse_message(message)
            self.connect_to_firebase(parsed_data)

            if parsed_data:
                json_data = self.create_json_response(parsed_data)
                self.UDPServerSocket.sendto(json_data.encode(), address)
                print(f"Resposta enviada para o cliente: {json_data}")
            else:
                print("Erro ao processar a mensagem. Formato inválido.")

    def parse_message(self, message):
        message_str = message.decode()
        message_str = self.remove_angle_brackets(message_str)

        # Separar a mensagem em duas partes com base no ponto e vírgula
        parts = message_str.split(';')

        if len(parts) > 1:
            before_semicolon, after_semicolon = parts
            
            # Separar os dados em quatro variáveis diferentes usando a vírgula como delimitador
            data_type, protocol, utc, status = self.extract_data_from_before_semicolon(before_semicolon)

            data_type = self.remove_data_type(data_type)

            # Extrair o valor do ID de after_semicolon
            client_id = self.extract_client_id(after_semicolon)

            try:
                return {
                    "type": int(data_type),
                    "protocolo": int(protocol),
                    "utc": datetime.datetime.strptime(utc, "%y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S"),
                    "status": int(status),
                    "id": client_id
                }
            except ValueError as e:
                print(f"Erro ao converter valores para int: {e}")
                return None
        else:
            print("Erro ao separar a mensagem.")
            return None

    def remove_angle_brackets(self, input_string):
        return input_string.replace(">", "").replace("<", "")
    
    def remove_data_type(self, data):
        return data.replace("DATA", "")

    def extract_data_from_before_semicolon(self, before_semicolon):
        data_parts = before_semicolon.split(',')
        
        if len(data_parts) == 4:
            data_type, protocol, utc, status = data_parts
            return data_type, protocol, utc, status
        else:
            print("Erro ao extrair dados.")
            return None, None, None, None

    def extract_client_id(self, after_semicolon):
        # Extrair o valor do ID de after_semicolon
        return after_semicolon.split('=')[1]

    def create_json_response(self, parsed_data):
        return json.dumps(parsed_data)

if __name__ == "__main__":
    udp_server = UDPServer()
    udp_server.run()
