#!/usr/bin/env python3
# This software is distributed under the terms of the MIT License.
# Copyright (c) 2024 Dmitry Ponomarev.
# Author: Dmitry Ponomarev <ponomarevda96@gmail.com>

import json

with open('res.json', 'r') as file:
    json_data = json.load(file)
    tests = json_data['report']['tests']
    for test in tests:
        short_name = test['name'].split("::")[-1]
        outcome = test['outcome']
        print(short_name, outcome)
