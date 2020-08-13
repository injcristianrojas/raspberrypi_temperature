#!/usr/bin/env python3

from datetime import datetime
from RPi_I2C_driver import Lcd

class LCDControl:
    
    def __init__(self):
        self.lcd = Lcd()

    def __init__(self, internal_temp, external_temp, owmapi_temp, owmapi_feels_like, condition):
        self.lcd = Lcd()
        self.set_initial_data(internal_temp, external_temp, owmapi_temp, owmapi_feels_like, condition)

    def set_initial_data(self, internal_temp, external_temp, owmapi_temp, owmapi_feels_like, condition):
        now_cl = datetime.now().strftime('%H:%M')
        now_utc = datetime.utcnow().strftime('%H:%M')
        self.lcd.lcd_display_string('SCL {} UTC {}'.format(now_cl, now_utc)[:20], 1)
        self.lcd.lcd_display_string('In/out: {}/{} C'.format(f'{internal_temp:4.1f}', f'{external_temp:4.1f}')[:20], 2)
        self.lcd.lcd_display_string('T/Feel: {}/{} C'.format(f'{owmapi_temp:4.1f}', f'{owmapi_feels_like:4.1f}')[:20], 3)
        self.lcd.lcd_display_string(condition.capitalize()[:20], 4)
        #self.lcd.lcd_write(0xD1)
        #self.lcd.lcd_write_char(0xDF)
        #self.lcd.lcd_write(0xA6)
        #self.lcd.lcd_write_char(0xDF)
        #self.lcd.lcd_write(0xE4)
        #self.lcd.lcd_write_char(0xDF)

    def set_time_data(self):
        now_cl = datetime.now().strftime('%H:%M')
        now_utc = datetime.utcnow().strftime('%H:%M')
        self.lcd.lcd_display_string_pos(now_cl, 1, 4)
        self.lcd.lcd_display_string_pos(now_utc, 1, 14)
    
    def set_current_data(self, internal_temp, external_temp, owmapi_temp, owmapi_feels_like, condition):
        self.lcd.lcd_display_string_pos(f'{internal_temp:4.1f}', 2, 8)
        self.lcd.lcd_display_string_pos(f'{external_temp:4.1f}', 2, 13)
        self.lcd.lcd_display_string_pos(f'{owmapi_temp:4.1f}', 3, 8)
        self.lcd.lcd_display_string_pos(f'{owmapi_feels_like:4.1f}', 3, 13)
        self.lcd.lcd_display_string_pos(condition.capitalize()[:20], 4, 0)
