from rclpy.node import Node
from raya.enumerations import ANGLE_UNIT, POSITION_UNIT
from raya.controllers.base_controller import BaseController

TIMEOUT_TOPIC_UNAVAILABLE = 5.0
ERROR_SERVER_DOWN = 'The raya status message was not received'


class StatusController(BaseController):

    def __init__(self, name: str, node: Node, interface, extra_info):
        pass

    async def get_raya_status(self) -> dict:
        return

    async def get_localization_status(self, ang_unit: ANGLE_UNIT,
                                      pos_unit: POSITION_UNIT) -> dict:
        return
