import json
import requests
import sensor
import time
from firebase import firebase
from datetime import datetime

def init_sensor_record(sensorid):
    candidate_sensors = firebase.get('/sensors', None, params={
        'orderBy': '"deviceId"',
        'equalTo': '"' + sensorid + '"'
    })
    if len(candidate_sensors) > 0:
        recordid = list(candidate_sensors.keys())[0]
        return recordid
    else:
        print('creating new record for sensor ' + sensorid)
        record = {
            'deviceId': sensorid,
            'deviceModel': 'DS18B20',
            'type': 'temperature',
            'temperatures': {}
        }
        response = firebase.post('/sensors', record)
        recordid = response['name']
        return recordid

def push_temp(recordid, tempc):
    patch = {
        datetime.now().isoformat().split('.')[0]: '{0} degC'.format(tempc)
    }
    requests.patch('https://barley-f8e3f.firebaseio.com/sensors/' + recordid + '/temperatures.json', json=patch)

firebase = firebase.FirebaseApplication('https://barley-f8e3f.firebaseio.com/')
tempsensor = sensor.Sensor()
recordid = init_sensor_record(tempsensor.device_id)
print('found sensor record id: ' + recordid)

while True:
    tempc = tempsensor.tempc()
    print(tempc)
    push_temp(recordid, tempc)
    time.sleep(1)
