#!/usr/bin/env python3

import os
import glob
import time
from datetime import datetime
from db import insert_temperature

os.system('/sbin/modprobe w1-gpio')
os.system('/sbin/modprobe w1-therm')

TIME_BETWEEN_MEASUREMENTS_SECONDS = 60
DEVICE0_FILE = '/sys/bus/w1/devices/28-01191bb88a82/w1_slave'
DEVICE1_FILE = '/sys/bus/w1/devices/28-3c01b556c9c2/w1_slave'

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def measure_and_insert():
    temp0 = read_temp(DEVICE0_FILE)
    insert_temperature(0, temp0)
    temp1 = read_temp(DEVICE1_FILE)
    insert_temperature(1, temp1)

if __name__ == "__main__":
    while True:
        measure_and_insert()
        time.sleep(TIME_BETWEEN_MEASUREMENTS_SECONDS)
