#!/usr/bin/env python3
# This software is distributed under the terms of the MIT License.
# Copyright (c) 2024 Dmitry Ponomarev.
# Author: Dmitry Ponomarev <ponomarevda96@gmail.com>

import sys
import time
import can

channel = '/dev/ttyACM3'
config = {"interface": "slcan", "channel": channel, "ttyBaudrate": 1000000, "bitrate": 1000000}

with can.Bus(**config) as bus:
    recv_counter = 0
    while True:
        try:
            can_frame = bus.recv(timeout=1.0)
            recv_counter += 1
        except (ValueError, IndexError) as err:
            print(err)
            sys.exit(1)

        print(recv_counter, can_frame)
        if can_frame is None:
            continue

