#!/usr/bin/env python3

from RPi_GPIO_i2c_LCD import lcd as l

from datetime import datetime

def get_strings(internal_temp, external_temp):
    now_cl = datetime.now().strftime('%H:%M')
    now_utc = datetime.utcnow().strftime('%H:%M')
    return [
        'SCL {} UTC {}'.format(now_cl, now_utc)[:20],
        'Inside temp: {0:0.1f}°C'.format(internal_temp)[:20],
        'Outside temp: {0:0.1f}°C'.format(external_temp)[:20],
    ]

def show_data_mock(internal_temp, external_temp):
    strings = get_strings(internal_temp, external_temp)
    for i in range(0, len(strings[:4])):
        print(strings[i])

def show_data(internal_temp, external_temp):
    lcd = l.HD44780(0x27)
    lcd.clear()
    strings = get_strings(internal_temp, external_temp)
    for i in range(0, len(strings[:4])):
        lcd.display(strings[i], i+1)