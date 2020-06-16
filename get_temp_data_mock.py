#!/usr/bin/env python3

import os
import glob
import time
import random

from datetime import datetime
from db import insert_temperature
from lcd_control import show_data_mock

TIME_BETWEEN_MEASUREMENTS_SECONDS = 60
DEVICE0_FILE = 0
DEVICE1_FILE = 1

def read_temp(device):
    return random.uniform(18.0, 23.0) if device is DEVICE0_FILE else random.uniform(9.0, 25.0)

def measure_and_insert():
    temp0 = read_temp(DEVICE0_FILE)
    insert_temperature(0, temp0)
    temp1 = read_temp(DEVICE1_FILE)
    insert_temperature(1, temp1)
    show_data_mock(temp0, temp1)

if __name__ == "__main__":
    while True:
        measure_and_insert()
        time.sleep(TIME_BETWEEN_MEASUREMENTS_SECONDS)
