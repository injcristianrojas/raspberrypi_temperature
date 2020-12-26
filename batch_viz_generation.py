#!/usr/bin/env python3

from datetime import timedelta, date

from viz_generator import generate_image_for_date

START_DATE = date(2020,8,12)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

if __name__ == "__main__":
    for single_date in daterange(START_DATE, date.today()):
        generate_image_for_date(single_date.strftime("%Y-%m-%d"))