from flask import Flask
from flask import render_template, make_response
from flask import jsonify

from datetime import datetime

import csv

from db_v2 import get_latest_temperatures, get_last_24hours_csv

app = Flask(__name__)


@app.after_request
def set_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = '0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' ajax.googleapis.com;"
    return response


@app.route('/')
def hello():
    latest = get_latest_temperatures()
    return render_template(
        'index.html',
        temp0='{0:0.1f}'.format(latest[1]),
        temp1='{0:0.1f}'.format(latest[2]),
        latest=latest[0].strftime('%A, %B %d, %H:%M')
    )


@app.route('/api/v1/last24hours/csv')
def last24():
    resp = make_response(get_last_24hours_csv())
    resp.headers['Content-Type'] = 'text/csv'
    return resp


@app.route('/api/v1/latest/')
def latest_json():
    latest_temp_data = get_latest_temperatures()
    return jsonify(
        latest=latest_temp_data[0],
        latest_formatted=latest_temp_data[0].strftime('%A, %B %d, %H:%M'),
        inside=latest_temp_data[1],
        outside=latest_temp_data[2],
        owm_temp=latest_temp_data[3],
        owm_feels=latest_temp_data[4],
        owm_condition=latest_temp_data[5]
    )
