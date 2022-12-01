from sqlmodel import Session

from models import Device, Sensor

from handler import engine

import serial

arduino = serial.Serial(port='/dev/cu.usbserial-2110', baudrate=115200, timeout=.1)


with Session(engine) as session:
    sensor_id = "ESP8266"
    sensor = session.query(Sensor).filter(Sensor.id == sensor_id).first()
    if not sensor:
        sensor = Sensor(id=sensor_id)
        session.add(sensor)
        session.commit()
        session.refresh(sensor)
    while True:

        data = arduino.readline()
        data = data.decode("utf-8")
        if len(data) == 0:
            continue
        data = data.split("\n")

        data = [val.split() for val in data]
        data = [val for sublist in data for val in sublist if val != 'ff:ff:ff:ff:ff:ff']

        if len(data) == 0:
            continue

        for mac_address in data:
            objects = [Device(sensor_id=sensor.id, mac_address=mac_address)]
            session.bulk_save_objects(objects)
            session.commit()

        print(data)
