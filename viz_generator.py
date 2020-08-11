#!/usr/bin/env python3

import time

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
    temps['time'] = temps['time'].apply(lambda t: datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal()))

    back24hours = (datetime.now() - timedelta(days = 1)).replace(tzinfo=tz.gettz())
    inside_last24hours = temps.loc[(temps['sensor'] == 0) & (temps['time'] > back24hours)]
    outside_last24hours = temps.loc[(temps['sensor'] == 1) & (temps['time'] > back24hours)]

    f, ax = plt.subplots(figsize=(8,5))
    sns.lineplot(x='time', y='temperature', data=inside_last24hours, ax=ax)
    sns.lineplot(x='time', y='temperature', data=outside_last24hours, ax=ax)
    ax.set_ylim(0,35)
    ax.tick_params(labelrotation=45)
    ax.set_title('Temperatures in the last 24 hours (Last updated: {})'.format(datetime.now().strftime('%H:%M')))
    ax.legend(labels=['Internal', 'External'])
    dateformatter = DateFormatter('%H:%M')
    dateformatter.set_tzinfo(tz.tzlocal())
    ax.xaxis.set_major_formatter(dateformatter)

    plt.tight_layout()
    f.savefig('static/latest.png')
    plt.clf()
    print('Graph generated at {}'.format(datetime.now()))

if __name__ == "__main__":
    generate_image()
