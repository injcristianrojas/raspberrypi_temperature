#!/usr/bin/env python3

import sys
import time
import threading
from lcd_control import LCDControl
from viz_generator import generate_image
from get_temp_data import measure_and_insert

# Times for operations in seconds
TIME_BETWEEN_MEASUREMENTS = 60
TIME_BETWEEN_VIZ_GENERATION = 600

def generate_visualization():
    while True:
        generate_image()
        time.sleep(TIME_BETWEEN_VIZ_GENERATION)

def measure():
    int_temp, ext_temp = measure_and_insert()
    lcd = LCDControl(int_temp, ext_temp)
    time.sleep(TIME_BETWEEN_MEASUREMENTS)
    while True:
        int_temp, ext_temp = measure_and_insert()
        lcd.set_current_data(int_temp, ext_temp)
        time.sleep(TIME_BETWEEN_MEASUREMENTS)

if __name__ == "__main__":
    thr_measurement = threading.Thread(target=measure, daemon=True)
    thr_visualization = threading.Thread(target=generate_visualization, daemon=True)
    thr_measurement.start()
    thr_visualization.start()
    thr_measurement.join()
    thr_visualization.join()