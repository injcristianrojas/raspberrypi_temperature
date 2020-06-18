#!/usr/bin/env python3

from RPi_I2C_driver import Lcd

from datetime import datetime

def get_strings(internal_temp, external_temp):
    now_cl = datetime.now().strftime('%H:%M')
    now_utc = datetime.utcnow().strftime('%H:%M')
    return [
        'SCL {} UTC {}'.format(now_cl, now_utc)[:20],
        'Inside temp: {0:0.1f} C'.format(internal_temp)[:20],
        'Outside temp: {0:0.1f} C'.format(external_temp)[:20],
    ]

def show_data_mock(internal_temp, external_temp):
    strings = get_strings(internal_temp, external_temp)
    for i in range(0, len(strings[:4])):
        print(strings[i])

def show_data(internal_temp, external_temp):
    lcd = Lcd()
    strings = get_strings(internal_temp, external_temp)
    for i in range(0, len(strings[:4])):
        lcd.lcd_display_string(strings[i], i+1)

def set_individual_data(internal_temp, external_temp):
    # BEWARE: Convert this to Object-Oriented, because Lcd() resets the display.
    # Times
    # lcd.lcd_display_string_pos('21:25', 1, 4)
    # lcd.lcd_display_string_pos('21:25', 1, 14)
    # Temps
    # lcd.lcd_display_string_pos('27.1', 2, 13)
    # lcd.lcd_display_string_pos('27.1', 3, 14)
    # lcd.lcd_write(0xD1)
    # lcd.lcd_write(0xA6)
    # lcd.lcd_write_char(0xDF)
    pass