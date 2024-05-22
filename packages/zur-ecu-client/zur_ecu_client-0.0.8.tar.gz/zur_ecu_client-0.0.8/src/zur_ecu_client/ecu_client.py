import json
import logging
import sched
import time
from threading import Thread

from .senml import SenmlNames, Dv, Ecu
from .udp_server import UdpServer


class EcuClient:

    def __init__(
        self, listener, ecu_ip: str, ecu_port: int, calls_per_second: int
    ) -> None:
        logging.basicConfig(level=logging.DEBUG)
        self.listener = listener
        self.requestInterval = 1.0 / calls_per_second
        self.subscriptions: dict[SenmlNames, list[callable]] = {}
        self.compiledMessages = []

        self.ecuIP = ecu_ip
        self.ecuPort = ecu_port

        self.udpServer = UdpServer("127.0.0.1", 9000, ecu_ip, ecu_port)

        self.thread1 = Thread(target=self.__receive_msg)
        # self.thread1.daemon = True
        self.thread2 = Thread(target=self.__schedule_requests)
        # self.thread2.daemon = True

    def start(self):
        self.thread1.start()
        self.thread2.start()

    def subscribe(self, data_field: SenmlNames, subscriber: callable):
        if data_field in self.subscriptions:
            self.subscriptions.get(data_field).append(subscriber)
        else:
            self.subscriptions[data_field] = [subscriber]
        self.__compile_subscriptions()

    def unsubscribe(self, data_field: SenmlNames, subscriber: callable):
        if data_field in self.subscriptions:
            self.subscriptions.get(data_field).remove(subscriber)
            if not self.subscriptions[data_field]:
                self.subscriptions.pop(data_field)
            self.__compile_subscriptions()

    def send_msg(self, msg):
        msg = json.dumps(msg)
        self.udpServer.send_data(msg)

    def __compile_subscriptions(self):
        for msg in self.subscriptions:
            self.compiledMessages.append({"bn": "ECU", "n": msg, "v": "request"})

    def __receive_msg(self):
        while True:
            data = self.udpServer.receive_data()
            if data:
                logging.info(f"Received -> {data}")

    def __request_messages(self):
        bn_request = []

        self.send_msg(self.compiledMessages)

    def __schedule_requests(self):
        scheduler = sched.scheduler(time.time, time.sleep)
        while True:
            scheduler.enter(self.requestInterval, 1, self.__request_messages, ())
            scheduler.run()


def __main__():
    mock_ecu = EcuClient(None, "127.0.0.1", 9001, 1)
    # msg = Ecu.Pedal(0, 0, 0).get()
    msg = Dv.Ctrl(0, 0, 0, "Hello World!").get()

    try:
        mock_ecu.start()
        # mock_ecu.subscribe("ECU:accu:sensor", None)  # Send a request to server
        for item in msg:
            mock_ecu.compiledMessages.append(item)  # for sending data to server
        # mock_ecu.send_msg(msg)

    except KeyboardInterrupt:
        mock_ecu.udpServer.close()


if __name__ == "__main__":
    __main__()
