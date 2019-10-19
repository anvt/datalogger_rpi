# todo: This will create a mini webpage for setting the tokens etc for the server.

# Testing Crontab

from flask import Flask, render_template, request, redirect, flash
import json
import os
from flask_wtf.csrf import CSRFProtect

from forms import RegisterSensor

# template_dir = os.path.abspath('../../frontend/src')
template_dir = os.path.abspath('./')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'lkdja;ldksjas;lkfblamn'
from flask_bootstrap import Bootstrap

csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)

import datetime
import glob

import os
import requests


def get_ds18b20_paths():
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

    ds = []
    sensor_id = []
    device_folders = glob.glob(base_dir + '28*')
    device_folders_slave = [p + '/w1_slave' for p in device_folders]

    for path in device_folders_slave:
        ds.append(path)
        sensor_id.append(path.split('/')[-2])
    return list(zip(sensor_id, ds))


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegisterSensor()
    with open('parameters.json') as parameters:
        data = json.load(parameters)

    ds18b20s = data['ds18b20']
    try:
        detected_ds18b20s = [d[0] for d in get_ds18b20_paths()]
    except:
        detected_ds18b20s = []

    output = []
    for dd in ds18b20s:
        output.append(str([dd['sensor_name'], dd['sensor_code'], dd['token'], dd['user_id']]))

    if form.validate_on_submit():
        flag = False
        print(request.form)
        if request.form['sensor_code'] in detected_ds18b20s:
            for d, ds in enumerate(ds18b20s):
                if ds['sensor_code'] == request.form['sensor_code']:
                    ds = request.form
                    flag = True
                    print(flag)
                    data['ds18b20'][d] = ds
                    break
            if not flag:
                data['ds18b20'].append(request.form)
                #     data['ds18b20'].append(ds)
            with open('parameters.json', 'w') as f:
                json.dump(data, f)
            flash('Please Reboot the system (if you are done)')


            # os.system('/etc/init.d/cron reload')
            # flash('Reloaded Cron.')
        else:
            flash('Sensor is not connected please check if the sensor code exists on the right.')
        return redirect('/')
    return render_template('./index.html', form=form, datasources=output, detected_ds18b20s=detected_ds18b20s)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
