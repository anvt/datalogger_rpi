
import time
import requests
import json
if __name__ == '__main__':

    while True:
        payload = {"value": 5, 'token': 'test', "user_id": 1, "name": "Fridge", 'datetime': 'test',
                   'sensor_name': 'sensor_name', 'sensor_code': 'sensor_code'}

        headers = {'content-type': 'application/json'}
        try:
            print('Server Send')
            url = 'http://192.168.1.2:5000/temperature'
            print(payload)
            response = requests.post(url, data=json.dumps(payload), headers=headers)

        except Exception as e:
            print(e)

        try:
            print('Loacal Send')
            response = requests.post('http://localhost:5000/temperature', data=json.dumps(payload), headers=headers)
        except Exception as e:
            print(e)
            # todo: send request to server that an error has occured else send an sms from the shield.
    time.sleep(30)
