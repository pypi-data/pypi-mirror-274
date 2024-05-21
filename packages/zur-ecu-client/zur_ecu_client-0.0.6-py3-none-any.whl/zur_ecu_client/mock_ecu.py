import logging
import time

from src.zur_ecu_client.udp_server import UdpServer


class MockECU:

    def __init__(self, mock_ecu_ip: str, mock_ecu_port: int, dv_ip: str, dv_port: int):
        logging.basicConfig(level=logging.DEBUG)
        self.mock_ecu_ip = mock_ecu_ip
        self.mock_ecu_port = mock_ecu_port
        self.dv_ip = dv_ip
        self.dv_port = dv_port
        self.udp_server = UdpServer(mock_ecu_ip, mock_ecu_port, dv_ip, dv_port)


def __main__():
    CLIENT_IP = "127.0.0.1"
    CLIENT_PORT = 9000
    MOCK_ECU_IP = "127.0.0.1"
    MOCK_ECU_PORT = 9001

    mock_ecu = MockECU(MOCK_ECU_IP, MOCK_ECU_PORT, CLIENT_IP, CLIENT_PORT)
    try:
        while True:
            data = '[{"bn":"DV", "n":"acc", "vs":""},{"n":"X","u":"m/s2","v":0},{"n":"Y","u":"m/s2","v":0},{"n":"Z","u":"m/s2","v":0}]'
            mock_ecu.udp_server.send_data(data)
            time.sleep(2)
    except KeyboardInterrupt:
        mock_ecu.udp_server.close()


if __name__ == "__main__":
    __main__()
