from src.zur_ecu_client.messages import Acknowledgment, Data, Messages
from src.zur_ecu_client.senml.senml import Senml


def test_incoming_parser():
    msg = Messages.parse2(
        """[
            {"bn": "DV", "n": "ctrl", "v": "sensor"},
            {"bn": "ECU", "n": "accu", "vs": "sensor"},
            {"n": "charge", "u": "%", "v": 0},
            {"n": "temp", "u": "Cel", "v": 0},
            {"n": "AIRPos", "u": "V", "v": 0},
            {"n": "AIRNeg", "u": "V", "v": 0},
            {"n": "preRelay", "u": "V", "v": 0}
        ]"""
    )

    assert type(msg[0]) is Acknowledgment
    assert type(msg[0].base) is Senml.Base
    assert type(msg[1]) is Data
    assert type(msg[1].base) is Senml.Base
