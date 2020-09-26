#!/usr/bin/env python3

import time

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, AutoDateLocator

from datetime import datetime, timedelta
from dateutil import tz

from io import StringIO

from db_v2 import get_last_24hours_csv

def generate_image():
    temps = pd.read_csv(StringIO(get_last_24hours_csv()))
    temps['time'] = temps['time'].apply(lambda t: datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal()))
    temps['time'] = pd.to_datetime(temps['time'])
    temps = temps.set_index('time')
    temps = temps.drop('condition', axis=1).drop('temp_owm', axis=1).drop('temp_owm_feels', axis=1)

    f, ax = plt.subplots(figsize=(8,5))
    sns.lineplot(data=temps, ax=ax, dashes=False)
    ax.set_ylim(0,35)
    ax.tick_params(labelrotation=45)
    ax.set_title('Temperatures in the last 24 hours (Last updated: {})'.format(datetime.now().strftime('%H:%M')))
    ax.legend(labels=['Internal', 'External'])
    dateformatter = DateFormatter('%H:%M', tz=tz.tzlocal())
    ax.xaxis.set_major_formatter(dateformatter)

    plt.tight_layout()
    f.savefig('static/latest.png')
    plt.clf()
    print('Graph generated at {}'.format(datetime.now()))

if __name__ == "__main__":
    generate_image()
