import datetime
import glob
import time
import os
import requests
import json

from config import base_dir


def get_local_ip_address():
    """
    This function runs a terminal command and retrieves the ip address of the host.
    :return:
    """
    # todo: Check operating system and run a different command.
    try:
        ipv4 = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]
    except Exception as e:
        ipv4 = None
        print(e)
    return ipv4


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
    current_datetime = datetime.datetime.now()
    lines = read_temp_raw(path)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(path)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temperature_celsius = float(temp_string) / 1000.0
        temperature_fahrenheit = temperature_celsius * 9.0 / 5.0 + 32.0
        return temperature_celsius, temperature_fahrenheit, str(current_datetime)


def send_data(payload):
    headers = {'content-type': 'application/json'}
    try:
        url = 'http://thethalos.com/temperature'
        response_epoptis = requests.post(url, data=json.dumps(payload), headers=headers)
    except Exception as e:
        print(e)
    try:
        response_local = requests.post('http://localhost:5000/temperature', data=json.dumps(payload), headers=headers)
    except Exception as e:
        print(e)
    return response_epoptis, response_local
