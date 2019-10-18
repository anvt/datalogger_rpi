import os
import glob
import time
import json
import requests

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

import datetime

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

import os
import requests


# os.environ['NO_PROXY'] = '127.0.0.1'

def get_ds18b20_paths():
    ds = []
    sensor_id = []
    device_folders = glob.glob(base_dir + '28*')
    for path in device_folders:
        ds.append(path)
        sensor_id.append(path.split('/')[-1])
    return list(zip(sensor_id, ds))


def read_temp_raw(path):
    f = open(path, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp(path):
    currentDT = datetime.datetime.now()
    lines = read_temp_raw(path)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f, str(currentDT)


while True:
    ds18b20s = get_ds18b20_paths()
    for sensor in ds18b20s:
        path = sensor[1]
        try:
            c, f, dt = read_temp(path)
            print(c, f)
            payload = {"value": c, 'token': 'test', "user_id": 1, "name": "Fridge", "datetime": dt}
            headers = {'content-type': 'application/json'}
            url = 'http://192.168.1.2:5000/test2'
            response = requests.post(url, data=json.dumps(payload), headers=headers)
        except Exception as e:
            print(e)
            # todo: send request to server that an error has occured else send an sms from the shield.
        time.sleep(30)
