#!/usr/bin/env python3

import os
import requests
from flask import jsonify
from dotenv import load_dotenv

LOCATION_ID = 3875139 # Providencia, CL

def dekelvinize(temp):
    return temp - 273.15

def get_owmapi_data():
    load_dotenv()
    OWMAPI_KEY = os.getenv('OWMAPI_KEY')
    url = "https://api.openweathermap.org/data/2.5/weather?id=%s&appid=%s" % (LOCATION_ID, OWMAPI_KEY)
    r = requests.get(url)
    data = r.json()
    feels_like = dekelvinize(data['main']['feels_like'])
    return feels_like

if __name__ == "__main__":
    print(get_owmapi_data())