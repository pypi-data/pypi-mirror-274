from src.zur_ecu_client.senml.senml import Senml
from src.zur_ecu_client.senml.senml_msg import SenmlMessage
from src.zur_ecu_client.senml.senml_unit import SenmlUnit
from src.zur_ecu_client.senml.senml_zur_names import SenmlNames


class Dv:
    class Cfg(SenmlMessage):
        def __init__(
            self,
            ass: str = None,
            ebss: str = None,
            asms: str = None,
        ) -> None:
            super().__init__(
                SenmlNames.DV_CFG,
                [
                    Senml.Record(
                        SenmlNames.DV_CFG_AS,
                        v=ass,
                    ),
                    Senml.Record(
                        SenmlNames.DV_CFG_EBS,
                        v=ebss,
                    ),
                    Senml.Record(
                        SenmlNames.DV_CFG_AMI,
                        v=asms,
                    ),
                ],
            )

    class Ctrl(SenmlMessage):
        def __init__(
            self,
            brake: str = None,
            steering: str = None,
            throttle: str = None,
            status: str = None,
        ) -> None:
            super().__init__(
                SenmlNames.DV_CTRL,
                [
                    Senml.Record(
                        SenmlNames.DV_CTRL_BRAKE,
                        SenmlUnit.PERCENTAGE,
                        brake,
                    ),
                    Senml.Record(
                        SenmlNames.DV_CTRL_STEERING,
                        SenmlUnit.PERCENTAGE,
                        steering,
                    ),
                    Senml.Record(
                        SenmlNames.DV_CTRL_THROTTLE,
                        SenmlUnit.PERCENTAGE,
                        throttle,
                    ),
                    Senml.Record(
                        SenmlNames.DV_CTRL_STATUS,
                        v=status,
                    ),
                ],
            )

    class Stat(SenmlMessage):
        def __init__(
            self,
            laps: int = None,
            cones_actual: int = None,
            cones_all: int = None,
        ) -> None:
            super().__init__(
                SenmlNames.DV_STAT,
                [
                    Senml.Record(
                        SenmlNames.DV_STAT_LAPS,
                        v=laps,
                    ),
                    Senml.Record(
                        SenmlNames.DV_STAT_CONESACT,
                        v=cones_actual,
                    ),
                    Senml.Record(
                        SenmlNames.DV_STAT_CONESALL,
                        v=cones_all,
                    ),
                ],
            )

    class Acc(SenmlMessage):
        def __init__(
            self,
            x: str = None,
            y: str = None,
            z: str = None,
        ) -> None:
            super().__init__(
                SenmlNames.DV_ACC,
                [
                    Senml.Record(
                        SenmlNames.DV_ACC_X,
                        SenmlUnit.ACCELERATION,
                        x,
                    ),
                    Senml.Record(
                        SenmlNames.DV_ACC_Y,
                        SenmlUnit.ACCELERATION,
                        y,
                    ),
                    Senml.Record(
                        SenmlNames.DV_ACC_Z,
                        SenmlUnit.ACCELERATION,
                        z,
                    ),
                ],
            )
