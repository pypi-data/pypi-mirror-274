import logging

from .messages import Acknowledgment, Data, Messages
from .senml import Senml

from .udp_server import UdpServer
from .senml import Ecu


class MockECU:

    def __init__(self, mock_ecu_ip: str, mock_ecu_port: int, dv_ip: str, dv_port: int):
        logging.basicConfig(level=logging.DEBUG)
        self.mock_ecu_ip = mock_ecu_ip
        self.mock_ecu_port = mock_ecu_port
        self.dv_ip = dv_ip
        self.dv_port = dv_port
        self.udp_server = UdpServer(mock_ecu_ip, mock_ecu_port, dv_ip, dv_port)

    def response_msg(self, mock_data: list):
        while True:
            data = self.udp_server.receive_data()
            if data:

                data = Messages.parse2(data)

                for element in data:
                    if type(element) is Acknowledgment:
                        base: Senml.Base = element.base
                        result = get_mock_data(mock_data, base.n)
                        self.udp_server.send_data(str(result))

                    elif type(element) is Data:
                        base: Senml.Base = element.base
                        send = {
                            "bn": str(base.bn).replace(":", ""),
                            "n": str(base.n).replace(":", ""),
                            "vs": str(base.v).replace(":", ""),
                        }
                        self.udp_server.send_data(str(send))


def get_mock_data(mock_data, search_name):
    empty, bn, n, vs = search_name.split(":")

    matching_records = []

    for record in mock_data:
        for record in mock_data:
            first_entry = record[0]
            if (
                first_entry.get("bn") == bn
                and first_entry.get("n") == n
                and first_entry.get("vs") == vs
            ):
                matching_records.append(record)
        return matching_records
    print("No matching record found")
    return None


def __main__():
    # egal was hier steht
    CLIENT_IP = "127.0.0.1"
    CLIENT_PORT = 9000
    # ab hier nicht mehr egal
    MOCK_ECU_IP = "127.0.0.1"
    MOCK_ECU_PORT = 9001
    msgs = []

    accu1 = Ecu.Accu(100, 10, 0, 0, 0).get()
    accu2 = Ecu.Accu(90, 20, 0, 0, 0).get()
    accu3 = Ecu.Accu(80, 30, 0, 0, 0).get()
    accu4 = Ecu.Accu(70, 40, 0, 0, 0).get()
    pedal = Ecu.Pedal(0, 0, 0, 0).get()

    msgs.append(accu1)
    msgs.append(accu2)
    msgs.append(accu3)
    msgs.append(accu4)
    msgs.append(pedal)

    mock_ecu = MockECU(MOCK_ECU_IP, MOCK_ECU_PORT, CLIENT_IP, CLIENT_PORT)
    try:
        while True:
            mock_ecu.response_msg(msgs)
    except KeyboardInterrupt:
        mock_ecu.udp_server.close()


if __name__ == "__main__":
    __main__()
