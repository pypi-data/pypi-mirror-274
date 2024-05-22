import logging

from .udp_server import UdpServer


class MockECU:

    def __init__(self, mock_ecu_ip: str, mock_ecu_port: int, dv_ip: str, dv_port: int):
        logging.basicConfig(level=logging.DEBUG)
        self.mock_ecu_ip = mock_ecu_ip
        self.mock_ecu_port = mock_ecu_port
        self.dv_ip = dv_ip
        self.dv_port = dv_port
        self.udp_server = UdpServer(mock_ecu_ip, mock_ecu_port, dv_ip, dv_port)
