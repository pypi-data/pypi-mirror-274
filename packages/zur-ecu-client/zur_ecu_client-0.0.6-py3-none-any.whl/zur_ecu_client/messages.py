import json
from enum import Enum, IntEnum
from typing import List

from src.zur_ecu_client.senml.senml import Senml
from src.zur_ecu_client.senml.senml_zur_names import SenmlNames
from src.zur_ecu_client.senml.util import value_by_key_prefix


class Messages:
    class AmiState(Enum):
        ACCELERATION = "acceleration"
        SKIDPAD = "skidpad"
        TRACKDRIVE = "trackdrive"
        BRAKETEST = "braketest"
        INSPECTION = "inspection"
        AUTOCROSS = "autocross"

    class EbsState(IntEnum):
        UNAVAILABLE = 1
        ARMED = 2
        ACTIVATED = 3

    class AsState(IntEnum):
        OFF = 1
        READY = 2
        DRIVING = 3
        EMERGENCY_BREAK = 4
        FINISH = 5

    @staticmethod
    def parse(data: str):
        data: List = json.loads(data)
        converted_data = {}
        base: dict = data.pop(0)  # remove baseName entry to only loop over record entry
        device = base["bn"]
        topic = f':{base["n"]}' if "n" in base else ""
        msg_type = (
            f':{value_by_key_prefix(base, "v")}'
            if value_by_key_prefix(base, "v")
            else ""
        )
        header = device + topic + msg_type
        for entry in data:
            data_name = SenmlNames(header + ":" + entry["n"])
            converted_data[data_name] = value_by_key_prefix(entry, "v")
        return converted_data

    @staticmethod
    def get_from_entry(data: dict):
        if "bn" in data:
            return Senml.Base.from_json(data)
        elif "n" in data:
            return Senml.Record.from_json(data)
        return TypeError

    @staticmethod
    def parse2(data: str):
        data: List = json.loads(data)
        converted_data = []
        pack = None
        for i in data:
            entry = Messages.get_from_entry(i)
            if type(entry) is Senml.Base:
                pack = Senml.Pack(entry)
                converted_data.append(pack)
            elif type(entry) is Senml.Record:
                pack.records.append(entry)
        final_data = []
        for i in converted_data:
            if not i.records:
                final_data.append(Acknowledgment(i.base))
            elif i.records is not []:
                final_data.append(Data(i.base, i.records))
        return final_data


class Acknowledgment:
    def __init__(self, base: SenmlNames) -> None:
        self.base = base


class Data:
    def __init__(self, base: SenmlNames, data: List[SenmlNames]) -> None:
        self.base = base
        self.data = data


class Request:
    def __init__(self, base: SenmlNames) -> None:
        self.base = base
