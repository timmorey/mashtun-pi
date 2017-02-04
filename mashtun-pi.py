import os
import glob
import time

import json
from firebase import firebase
from datetime import datetime

firebase = firebase.FirebaseApplication('https://barley-f8e3f.firebaseio.com/')

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
device_id = device_folder.split('/')[-1]

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def push_temp(tempC):
    record = {
        'sensorId': device_id,
        'timestamp': datetime.now().isoformat(),
        'temperature': '{0} degC'.format(tempC)
    }
    result = firebase.post('/temperatures', record)

while True:
    degc, degf = read_temp()
    print(degc, degf)
    push_temp(degc)
    time.sleep(1)
