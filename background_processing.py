#!/usr/bin/env python3

import sys
import time
import threading

dev_mode = False
if len(sys.argv) > 1:
    dev_mode = sys.argv[1] == '--development'

from viz_generator import generate_image
if dev_mode is True:
    from get_temp_data_mock import measure_and_insert
else:
    from get_temp_data import measure_and_insert

# Times for operations in seconds
TIME_BETWEEN_MEASUREMENTS = 60
TIME_BETWEEN_VIZ_GENERATION = 600

def measure():
    while True:
        generate_image()
        time.sleep(TIME_BETWEEN_MEASUREMENTS)

def generate_visualization():
    while True:
        measure_and_insert()
        time.sleep(TIME_BETWEEN_VIZ_GENERATION)

if __name__ == "__main__":
    thr_measurement = threading.Thread(target=measure, daemon=True)
    thr_visualization = threading.Thread(target=generate_visualization, daemon=True)
    thr_measurement.start()
    thr_visualization.start()
    thr_measurement.join()
    thr_visualization.join()