#!/usr/bin/env python3

import time

from sqlalchemy import create_engine
from sqlalchemy import Column, DateTime, Integer, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dateutil import tz

engine = create_engine('sqlite:///temps_v2.sqlite', echo=False)
Base = declarative_base()

class Temperatures(Base):
    __tablename__ = 'temperatures'

    time = Column(DateTime, primary_key=True, default=datetime.utcnow)
    temp_internal = Column(Float)
    temp_external = Column(Float)
    
    def __init__(self, temp_internal, temp_external):
        self.temp_internal = temp_internal
        self.temp_external = temp_external

def create_db():
    Base.metadata.create_all(engine)

def insert_temperatures(temp_internal=None, temp_external=None):
    session = sessionmaker(bind=engine)()
    temps = Temperatures(temp_internal, temp_external)
    measurement_time = datetime.now()
    session.add(temps)
    print('Inserting data: {}/{}°C at {}'.format(temp_internal, temp_external, measurement_time))
    session.commit()
    session.close()

def get_latest_temperatures():
    session = sessionmaker(bind=engine)()
    q = session.query(Temperatures).order_by(Temperatures.time.desc()).first()
    session.close()
    return(q.time.replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal()), q.temp_internal, q.temp_external)

def get_last_24hours_data():
    data = [['time', 'temp_internal', 'temp_external']]
    query = "select * from temperatures where time >= datetime('now', '-1 day')"
    with engine.connect() as conn:
        rs = conn.execute(query)
        for row in rs:
            data.append([row[0], row[1], row[2]])
    return data

def get_last_24hours_csv():
    data = get_last_24hours_data()
    csv_string = ''
    for row in data:
        csv_string += '"{}",{},{}\n'.format(row[0], row[1], row[2])
    return csv_string

if __name__ == "__main__":
    create_db()