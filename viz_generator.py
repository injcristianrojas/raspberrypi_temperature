#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from datetime import datetime
from dateutil import tz


from db_v2 import get_24hour_data_last24, get_24hour_data_from_day

def generate_image_last24():
    last_24_list = get_24hour_data_last24()
    temps = pd.DataFrame(last_24_list[1:], columns=last_24_list[0])
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

def generate_image_for_date(date):
    list_24hrs = get_24hour_data_from_day(date)
    temps = pd.DataFrame(list_24hrs[1:], columns=list_24hrs[0])
    temps['time'] = temps['time'].apply(lambda t: datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal()))
    temps['time'] = pd.to_datetime(temps['time'])
    temps = temps.set_index('time')
    temps = temps.drop('condition', axis=1).drop('temp_owm', axis=1).drop('temp_owm_feels', axis=1)

    f, ax = plt.subplots(figsize=(8,5))
    sns.lineplot(data=temps, ax=ax, dashes=False)
    ax.set_ylim(0,35)
    ax.tick_params(labelrotation=45)
    ax.set_title('24-hour temperatures for {}'.format(date))
    ax.legend(labels=['Internal', 'External'])
    dateformatter = DateFormatter('%H:%M', tz=tz.tzlocal())
    ax.xaxis.set_major_formatter(dateformatter)

    plt.tight_layout()
    f.savefig('static/{}.png'.format(date.replace('-', '')))
    plt.close(f)
    print('Graph for {} generated at {}'.format(date, datetime.now()))

if __name__ == "__main__":
    generate_image_last24()
