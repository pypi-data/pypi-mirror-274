#!/usr/bin/env python3
# This software is distributed under the terms of the MIT License.
# Copyright (c) 2024 Dmitry Ponomarev.
# Author: Dmitry Ponomarev <ponomarevda96@gmail.com>
import os
import sys
import secrets
import subprocess
import pytest
import dronecan
from enum import IntEnum

from raccoonlab_tools.dronecan.global_node import DronecanNode
from raccoonlab_tools.common.protocol_parser import CanProtocolParser, Protocol
from raccoonlab_tools.dronecan.utils import Parameter, ParametersInterface, NodeCommander

PARAM_PWM_FB_1_TYPE                 = 'pwm.fb_1_type'
PARAM_PWM_FB_2_TYPE                 = 'pwm.fb_2_type'


class ThisNode:
    def __init__(self) -> None:
        self.node = DronecanNode()

    def send_single_light_command(self, red: int, green: int, blue: int, id: int = 0) -> None:
        msg = dronecan.uavcan.equipment.indication.LightsCommand(commands=[
            dronecan.uavcan.equipment.indication.SingleLightCommand(
                light_id=id,
                color=dronecan.uavcan.equipment.indication.RGB565(
                    red=red,
                    green=green,
                    blue=blue
        ))])
        self.node.publish(msg)

    def recv_color(self, timeout_sec=0.03):
        res = self.node.sub_once(dronecan.uavcan.equipment.indication.LightsCommand, timeout_sec)
        color = res.message.commands[0].color
        return color

    def send_raw_command(self, cmd : list) -> None:
        msg = dronecan.uavcan.equipment.esc.RawCommand(cmd=cmd)
        self.node.publish(msg)

    def configure(self, config):
        params = ParametersInterface()
        commander = NodeCommander()

        params.set(config)
        commander.store_persistent_states()
        commander.restart()

def compare_colors(first, second):
    return first.red == second.red and first.green == second.green and first.blue == second.blue


@pytest.mark.dependency()
def test_transport():
    """
    This test is required just for optimization purposes.
    Let's skip all tests if we don't have an online Cyphal node.
    """
    assert CanProtocolParser.verify_protocol(white_list=[Protocol.DRONECAN])


@pytest.mark.dependency(depends=["test_transport"])
class TestSomething:
    config = [
        Parameter(name=PARAM_PWM_FB_1_TYPE, value=1),
        Parameter(name=PARAM_PWM_FB_2_TYPE, value=1),
    ]

    @staticmethod
    def test_something():
        """
        After the initialization, the node must have the configured color.
        """
        node = ThisNode()
        node.configure(TestSomething.config)


def main():
    cmd = ["pytest", os.path.abspath(__file__), "--tb=no", "-v", '-W', 'ignore::DeprecationWarning']
    cmd += sys.argv[1:]
    sys.exit(subprocess.call(cmd))

if __name__ == "__main__":
    main()
