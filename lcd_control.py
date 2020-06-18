#!/usr/bin/env python3

from datetime import datetime
from RPi_I2C_driver import Lcd

class LCDControl:
    
    def __init__(self):
        self.lcd = Lcd()

    def __init__(self, internal_temp, external_temp):
        self.lcd = Lcd()
        self.set_initial_data(internal_temp, external_temp)
    
    def set_initial_data(self, internal_temp, external_temp):
        now_cl = datetime.now().strftime('%H:%M')
        now_utc = datetime.utcnow().strftime('%H:%M')
        self.lcd.lcd_display_string('SCL {} UTC {}'.format(now_cl, now_utc)[:20], 1)
        self.lcd.lcd_display_string('Inside temp: {0:0.1f} C'.format(internal_temp)[:20], 2)
        self.lcd.lcd_display_string('Outside temp: {0:0.1f} C'.format(external_temp)[:20], 3)
        self.lcd.lcd_write(0xD1)
        self.lcd.lcd_write_char(0xDF)
        self.lcd.lcd_write(0xA6)
        self.lcd.lcd_write_char(0xDF)
    
    def set_current_data(self, internal_temp, external_temp):
        now_cl = datetime.now().strftime('%H:%M')
        now_utc = datetime.utcnow().strftime('%H:%M')
        self.lcd.lcd_display_string_pos(now_cl, 1, 4)
        self.lcd.lcd_display_string_pos(now_utc, 1, 14)
        self.lcd.lcd_display_string_pos('{0:0.1f}'.format(internal_temp), 2, 13)
        self.lcd.lcd_display_string_pos('{0:0.1f}'.format(external_temp), 3, 14)