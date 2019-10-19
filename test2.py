


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
            try:
                c, f, dt = read_temp(path)
                print(c, f)
                payload['user_id'] = user_id
                payload['value'] = c
                payload['datetime'] = dt

                # payload = {"value": c, 'token': 'test', "user_id": 1, "name": "Fridge",
                headers = {'content-type': 'application/json'}
                url = 'http://192.168.1.2:5000/temperature'
                print(payload)
                response = requests.post(url, data=json.dumps(payload), headers=headers)
            except Exception as e:
                print(e)
                # todo: send request to server that an error has occured else send an sms from the shield.
        time.sleep(30)
