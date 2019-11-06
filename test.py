import time
import json
from utilities import get_ds18b20_paths, read_temp, get_local_ip_address, send_data
import os
import requests
from config import w1_sensor_directory

# device_folder = glob.glob(w1_sensor_directory + '28*')[0]
# device_file = device_folder + '/w1_slave'
# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')


# os.environ['NO_PROXY'] = '127.0.0.1'


if __name__ == '__main__':

    with open('../parameters.json') as parameters:
        data = json.load(parameters)

    while True:

        ipv4 = get_local_ip_address()
        user_id = data['user_id']

        ds18b20s_sensors = get_ds18b20_paths()
        print('Connected Sensors: ', ds18b20s_sensors)
        registered_sensors = data['ds18b20']

        for ds18b20_sensor in ds18b20s_sensors:
            sensor_id = ds18b20_sensor[0]
            sensor_path = ds18b20_sensor[1]

            for sensor in registered_sensors:
                if sensor['sensor_code'] == sensor_id:
                    payload = sensor
                    break
                else:
                    print('Sensor Code: Not found.')
                    continue
                    print('Default')
                    payload = {
                        "name": "Fridge",
                        "id": "28-031897790020",
                        "token": "bigpennis"
                    }
                # todo: what to do when not in it?
            temperature_celsius, temperature_fahrenheit, current_datetime = read_temp(sensor_path)
            print(temperature_celsius, temperature_fahrenheit)
            payload['user_id'] = user_id
            payload['value'] = temperature_celsius
            payload['datetime'] = current_datetime
            payload['ipv4'] = ipv4

            send_data(payload)
                # todo: send request to server that an error has occured else send an sms from the shield.
        time.sleep(30)

