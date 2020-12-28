#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from datetime import datetime
from dateutil import tz

from db_v2 import get_24hour_data_last24, get_24hour_data_from_day

GRAPH_LOCATION = "static/graphs/"

def generate_image_last24():
    last_24_list = get_24hour_data_last24()
    df_temps = pd.DataFrame(last_24_list[1:], columns=last_24_list[0])
    df_temps['time'] = df_temps['time'].apply(lambda t: datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal()))
    df_temps['time'] = pd.to_datetime(df_temps['time'])
    df_temps = df_temps.set_index('time')
    df_temps = df_temps.drop('condition', axis=1).drop('temp_owm', axis=1).drop('temp_owm_feels', axis=1)

    f, ax = plt.subplots(figsize=(8,5))
    sns.lineplot(data=df_temps, ax=ax, dashes=False)
    ax.set_ylim(-5,45)
    ax.tick_params(labelrotation=45)
    ax.set_title('Temperatures in the last 24 hours (Last updated: {})'.format(datetime.now().strftime('%H:%M')))
    ax.legend(labels=['Internal', 'External'])
    dateformatter = DateFormatter('%H:%M', tz=tz.tzlocal())
    ax.xaxis.set_major_formatter(dateformatter)

    plt.tight_layout()
    f.savefig('{}latest.png'.format(GRAPH_LOCATION))
    plt.clf()
    print('Graph generated at {}'.format(datetime.now()))

def generate_image_for_date(date):
    list_24hrs = get_24hour_data_from_day(date)
    df_temps = pd.DataFrame(list_24hrs[1:], columns=list_24hrs[0])
    df_temps['time'] = df_temps['time'].apply(lambda t: datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal()))
    df_temps['time'] = pd.to_datetime(df_temps['time'])
    df_temps = df_temps.set_index('time')

    textstr = '\n'.join((
        'Min/Max temperatures:',
        'Internal: {:.1f}/{:.1f} °C'.format(df_temps['temp_internal'].min(), df_temps['temp_internal'].max()),
        'External: {:.1f}/{:.1f} °C'.format(df_temps['temp_external'].min(), df_temps['temp_external'].max()),
        'OWM: {:.1f}/{:.1f} °C'.format(df_temps['temp_owm'].min(), df_temps['temp_owm'].max()),
    ))

    df_temps = df_temps.drop('condition', axis=1).drop('temp_owm', axis=1).drop('temp_owm_feels', axis=1)

    f, ax = plt.subplots(figsize=(8,5))
    sns.lineplot(data=df_temps, ax=ax, dashes=False)
    ax.set_ylim(-5,45)
    ax.tick_params(labelrotation=45)
    ax.set_title('24-hour temperatures for {}'.format(date))
    ax.legend(labels=['Internal', 'External'])
    dateformatter = DateFormatter('%H:%M', tz=tz.tzlocal())
    ax.xaxis.set_major_formatter(dateformatter)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=9, verticalalignment='top', bbox=props)

    plt.tight_layout()
    f.savefig('{}{}.png'.format(GRAPH_LOCATION, date.replace('-', '')))
    plt.close(f)
    print('Graph for {} generated at {}'.format(date, datetime.now()))

if __name__ == "__main__":
    generate_image_last24()
