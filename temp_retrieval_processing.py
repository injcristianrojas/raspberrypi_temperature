#!/usr/bin/env python3

import sys
import time
import threading
from datetime import date, timedelta
from lcd_control import LCDControl
from viz_generator import generate_image, generate_image_for_date
from temp_sensor_handler import measure_insert_getdata
from owmapi import get_owmapi_data
from pid import PidFile

# Times for operations in seconds
TIME_BETWEEN_VIZ_GENERATION = 600

def generate_visualization():
    while True:
        generate_image()
        current_time = time.localtime()
        if current_time.tm_hour == 0 and current_time.tm_min >= 0 and current_time.tm_min <= 5:
            create_visualization_for_yesterday()
        time.sleep(TIME_BETWEEN_VIZ_GENERATION)

def create_visualization_for_yesterday():
    yesterday = date.today() - timedelta(days=1)
    generate_image_for_date(yesterday.strftime('%Y%m%d'))

def measure():
    int_temp, ext_temp, owm_temp, owm_feels_like, condition = measure_insert_getdata()
    lcd = LCDControl(int_temp, ext_temp, owm_temp, owm_feels_like, condition)
    while True:
        if int(time.strftime('%S')) % 60 == 0:
            lcd.set_time_data()
            int_temp, ext_temp, owm_temp, owm_feels_like, condition = measure_insert_getdata()
            lcd.set_current_data(int_temp, ext_temp, owm_temp, owm_feels_like, condition)
        time.sleep(1)

if __name__ == "__main__":
    with PidFile(piddir='.'):
        threads = []
        thr_measurement = threading.Thread(target=measure, daemon=True)
        thr_visualization = threading.Thread(target=generate_visualization, daemon=True)
        thr_measurement.start()
        threads.append(thr_measurement)
        thr_visualization.start()
        threads.append(thr_measurement)
        for t in threads:
            t.join()