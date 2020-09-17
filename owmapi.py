#!/usr/bin/env python3

import os
import requests
from urllib3.exceptions import ProtocolError
from requests.exceptions import ConnectionError
from http.client import RemoteDisconnected
from flask import jsonify
from dotenv import load_dotenv

def dekelvinize(temp):
    return temp - 273.15

def get_owmapi_data():
    load_dotenv()
    OWMAPI_KEY = os.getenv('OWMAPI_KEY')
    OWMAPI_LOCATION_ID = os.getenv('OWMAPI_LOCATION_ID')
    try:
        url = "https://api.openweathermap.org/data/2.5/weather?id=%s&appid=%s" % (OWMAPI_LOCATION_ID, OWMAPI_KEY)
        r = requests.get(url)
        data = r.json()
        feels_like = dekelvinize(data['main']['feels_like'])
        temp = dekelvinize(data['main']['temp'])
        condition = data['weather'][0]['description']
        return temp, feels_like, condition
    except (ConnectionError, ProtocolError) as e:
        print(str(e) + ' ' + str(e.__traceback__))
        return dekelvinize(0), dekelvinize(0), 'OWMAPI error'

if __name__ == "__main__":
    print(get_owmapi_data())