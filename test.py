import os
import glob
import time
import json
import requests
import json

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
    device_folders_slave = [p + '/w1_slave' for p in device_folders]

    for path in device_folders_slave:
        ds.append(path)
        sensor_id.append(path.split('/')[-2])
    return list(zip(sensor_id, ds))


def read_temp_raw(path):
    try:
        f = open(path, 'r')
        lines = f.readlines()
        f.close()
        return lines
    except Exception as e:
        print(e)
        return None


def read_temp(path):
    currentDT = datetime.datetime.now()
    lines = read_temp_raw(path)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(path)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f, str(currentDT)


if __name__ == '__main__':

    with open('parameters.json') as parameters:
        data = json.load(parameters)

    while True:

        user_id = data['user_id']

        ds18b20s = get_ds18b20_paths()
        print(ds18b20s)
        sensors = data['ds18b20']
        for sensor in ds18b20s:
            sensor_id = sensor[0]
            path = sensor[1]
            for se in sensors:
                if se['sensor_code'] == sensor_id:
                    payload = se
                    break
                else:
                    print('Default')
                    payload = {
                        "name": "Fridge",
                        "id": "28-031897790020",
                        "token": "bigpennis"
                    }
                # todo: what to do when not in it?
            c, f, dt = read_temp(path)
            print(c, f)
            payload['user_id'] = user_id
            payload['value'] = c
            payload['datetime'] = dt

            # payload = {"value": c, 'token': 'test', "user_id": 1, "name": "Fridge",
            headers = {'content-type': 'application/json'}
            try:

                url = 'http://thethalos.com/epoptis/temperature'
                print(payload)
                response = requests.post(url, data=json.dumps(payload), headers=headers)

            except Exception as e:
                print(e)

            try:
                response = requests.post('http://localhost:5000/temperature', data=json.dumps(payload), headers=headers)
            except Exception as e:
                print(e)
                # todo: send request to server that an error has occured else send an sms from the shield.
        time.sleep(30)

