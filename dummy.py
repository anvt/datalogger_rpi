import os
import glob
import time
import json
import random

import datetime

import requests


def read_temp_ds18b20():
    currentDT = datetime.datetime.now()
    return random.random(), random.random(), str(currentDT)


while True:
    try:
        print('Reading Temperature')

        c, f, dt = read_temp_ds18b20()
        payload = {"value": c, "user_id": 1, "name": "Fridge", "datetime": dt}
        print(payload)
        headers = {'content-type': 'application/json'}
        url = 'http://192.168.1.2:5000/test2'
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        time.sleep(5)
    except Exception as e:
        print(e)
        # todo: send request to server that an error has occured else send an sms from the shield.

    try:
        print('Reading Analog')
        c, f, dt = read_temp_ds18b20()
        payload = {"value": c, "user_id": 1, "name": "Fridge", "datetime": dt}
        print(payload)
        headers = {'content-type': 'application/json'}
        url = 'http://192.168.1.2:5000/test2'
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        time.sleep(5)
    except Exception as e:
        print(e)
        # todo: send request to server that an error has occured else send an sms from the shield.
