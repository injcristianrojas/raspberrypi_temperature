#!/usr/bin/env python3

import time
import pytz

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, AutoDateLocator

from datetime import datetime, timedelta
from dateutil import tz

from io import StringIO

from db import get_last_24hours_csv

def generate_image():
    temps = pd.read_csv(StringIO(get_last_24hours_csv()))
    temps['time'] = temps['time'].apply(lambda t: datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=pytz.UTC).astimezone(tz.tzlocal()).replace(second=0,microsecond=0))
    temps['time'] = pd.to_datetime(temps['time'])

    back24hours = (datetime.now() - timedelta(days = 1)).replace(tzinfo=tz.gettz())
    inside_last24hours = temps.loc[(temps['sensor'] == 0) & (temps['time'] > back24hours)]
    outside_last24hours = temps.loc[(temps['sensor'] == 1) & (temps['time'] > back24hours)]

    full = pd.merge(inside_last24hours, outside_last24hours, on='time', how='inner')
    full = full.drop(['sensor_x', 'sensor_y'], 1)
    full.columns = ['time', 'inside_temps', 'outside_temps']
    full = full.set_index(pd.DatetimeIndex(data=full['time'], tz=tz.tzlocal()))
    full = full.resample('5Min').agg('mean')

    f, ax = plt.subplots(figsize=(8,5))
    sns.lineplot(data=full, ax=ax, dashes=False)
    ax.set_ylim(0,35)
    ax.tick_params(labelrotation=45)
    ax.set_title('Temperatures in the last 24 hours (Last updated: {})'.format(datetime.now().strftime('%H:%M')))
    ax.legend(labels=['Internal', 'External'])
    dateformatter = DateFormatter('%H:%M', tz=full.index.tz)
    ax.xaxis.set_major_formatter(dateformatter)

    plt.tight_layout()
    f.savefig('static/latest.png')
    plt.clf()
    print('Graph generated at {}'.format(datetime.now()))

if __name__ == "__main__":
    generate_image()
