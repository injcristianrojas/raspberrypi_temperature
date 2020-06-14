from flask import Flask
from flask import render_template, make_response

from datetime import datetime

import csv

from db import get_latest_temperatures, get_last_24hours_csv

app = Flask(__name__)

@app.route('/')
def hello():
    latest = get_latest_temperatures()
    return render_template(
        'index.html',
        temp0='{0:0.1f}'.format(latest[1]),
        temp1='{0:0.1f}'.format(latest[2]),
        latest=latest[0].strftime('%A, %B %d, %H:%M')
    )

@app.route('/api/v1/csv/last24hours')
def last24():
    resp = make_response(get_last_24hours_csv())
    resp.headers['Content-Type'] = 'text/csv'
    return resp