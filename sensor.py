# Based on https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing

import os
import glob
import time

class Sensor:

    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = device_folder + '/w1_slave'
        self.device_id = device_folder.split('/')[-1]

    def tempc(self):
        lines = self.raw_input()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.1)
            lines = self.raw_input()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

    def raw_input(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
