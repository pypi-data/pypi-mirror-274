#!/usr/bin/env python3
# This software is distributed under the terms of the MIT License.
# Copyright (c) 2024 Dmitry Ponomarev.
# Author: Dmitry Ponomarev <ponomarevda96@gmail.com>
import os
import sys
import subprocess
# pylint: disable=no-member
import dronecan
import pytest
import pandas as pd

from raccoonlab_tools.dronecan.global_node import DronecanNode
from raccoonlab_tools.common.protocol_parser import CanProtocolParser, Protocol
from raccoonlab_tools.dronecan.utils import NodeFinder

import time

node = DronecanNode()

# Создаем список временных меток
messages_timestamps = []

def messages_count(msg):
    # Добавляем текущую временную метку в список
    messages_timestamps.append(time.time())

# длительность подсчета сообщений (например, 10 секунд)
count_time = 10  # секунды
start_time = time.time()

while time.time() - start_time < count_time:
    # Получаем сообщение
    msg = node.sub_once(dronecan.uavcan.equipment.power.BatteryInfo)
    if msg is not None:
        # Обрабатываем сообщение
        messages_count(msg)


# Вычисляем частоту публикации сообщений в Hz
num_messages = len(messages_timestamps)
if num_messages > 1:
    # время, прошедшее между последним и первым сообщением
    duration_time = messages_timestamps[-1] - messages_timestamps[0]
    message_frequency_hz = num_messages / duration_time
    print("Частота публикации сообщений: {:.2f} Hz".format(message_frequency_hz))
    print(num_messages)
    print(duration_time)
    print(messages_timestamps)
else:
    print("Не получено ни одного сообщения.")

# Устанавливаем формат отображения для чисел в DataFrame
pd.set_option('display.float_format', lambda x: '%.10f' % x)    

# Создаем DataFrame с переменной messages_timestamps в одном столбце

df = pd.DataFrame({'messages_timestamps': messages_timestamps})

# Устанавливаем столбец num_messages как порядковый номер сообщения
df['num_messages'] = df.reset_index().index + 1

# Добавляем столбец с разницей между текущим значением и предыдущим значением
df['frequency_time'] = df['messages_timestamps'] - df['messages_timestamps'].shift(1)

# Задаем значение первой строки в новом столбце равным 0
df.at[0, 'frequency_time'] = 0

# Добавляем столбец с разницей между frequency_time и 0.2
df['deviations from 5Hz (in seconds)'] = 0.2 - df['frequency_time']

# Добавляем столбец 'Hz' со значениями 1/frequency_time
df['Hz'] = 1 / df['frequency_time']

print(df)


node = DronecanNode()

# Создаем список временных меток
messages_timestamps = []

def messages_count(msg):
    # Добавляем текущую временную метку в список
    messages_timestamps.append(time.time())

while len(messages_timestamps) < 4:
    # Получаем сообщение
    msg = node.sub_once(dronecan.uavcan.equipment.power.BatteryInfo)
    if msg is not None:
        # Обрабатываем сообщение
        messages_count(msg)

#что ниже просто вывожу на печать смотрю как меняется точность от кол-ва сообщений (если 3 подряд близко к 5 то 5 Hz, если окно смещено частота выше или ниже)     

# Вычисляем частоту публикации сообщений в Hz
num_messages = len(messages_timestamps) - 1 # -1 чтобы делить на количество интервалов, а не кол-во сообщений (переменную нужно назвать интервал между сообщениями)
if num_messages > 1:
    # время, прошедшее между последним и первым сообщением
    duration_time = messages_timestamps[-1] - messages_timestamps[0]
    message_frequency_hz = num_messages / duration_time
    print("Частота публикации сообщений: {:.2f} Hz".format(message_frequency_hz))
    print(num_messages)
    print(duration_time)
    print(messages_timestamps)
else:
    print("Не получено ни одного сообщения.")


node = DronecanNode()

# Создаем список временных меток
messages_timestamps = []

def messages_count(msg):
    # Добавляем текущую временную метку в список
    messages_timestamps.append(time.time())

while len(messages_timestamps) < 3:
    # Получаем сообщение
    msg = node.sub_once(dronecan.uavcan.equipment.power.BatteryInfo)
    if msg is not None:
        # Обрабатываем сообщение
        messages_count(msg)

# Вычисляем частоту публикации сообщений в Hz
num_messages = len(messages_timestamps) - 1 # -1 чтобы делить на количество интервалов, а не кол-во сообщений (переменную нужно назвать интервал между сообщениями)
if num_messages > 1:
    # время, прошедшее между последним и первым сообщением
    duration_time = messages_timestamps[-1] - messages_timestamps[0]
    message_frequency_hz = num_messages / duration_time
    print("Частота публикации сообщений: {:.2f} Hz".format(message_frequency_hz))
    print(num_messages)
    print(duration_time)
    print(messages_timestamps)
else:
    print("Не получено ни одного сообщения.")
