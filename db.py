#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy import Column, DateTime, Integer, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dateutil import tz

engine = create_engine('sqlite:///temp.sqlite', echo=True)
Base = declarative_base()

class Temperature(Base):
    __tablename__ = 'temperatures'

    time = Column(DateTime, primary_key=True, default=datetime.utcnow)
    sensor = Column(Integer, primary_key=True)
    temperature = Column(Float)
    
    def __init__(self, sensor, temperature):
        self.sensor = sensor
        self.temperature = temperature

def create_db():
    Base.metadata.create_all(engine)

def insert_temperature(sensor=0, temperature=0.0):
    session = sessionmaker(bind=engine)()
    temp = Temperature(sensor, temperature)
    session.add(temp)
    session.commit()
    session.close()

def get_latest_temperature():
    session = sessionmaker(bind=engine)()
    q = session.query(Temperature).order_by(Temperature.time.desc()).first()
    session.close()
    return(q.time.replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal()), q.temperature)

def get_latest_temperatures():
    session = sessionmaker(bind=engine)()
    q = session.query(Temperature).filter(Temperature.sensor == 0).order_by(Temperature.time.desc()).first()
    temp0 = q.temperature
    q = session.query(Temperature).filter(Temperature.sensor == 1).order_by(Temperature.time.desc()).first()
    temp1 = q.temperature
    session.close()
    return(q.time.replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal()), temp0, temp1)

def get_last_24hours_data():
    data = [['time', 'sensor', 'temperature']]
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