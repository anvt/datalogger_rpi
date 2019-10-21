# todo: This will create a mini webpage for setting the tokens etc for the server.

# Testing Crontab

from flask import Flask, render_template, request, redirect, flash
import json
import os
from flask_wtf.csrf import CSRFProtect

from forms import RegisterSensor

# template_dir = os.path.abspath('../../frontend/src')
template_dir = os.path.abspath('./')
static_dir = os.path.abspath('./')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = 'lkdja;ldksjas;lkfblamn'

app.config['UPLOAD_FOLDER'] = os.path.abspath('./')
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sensor_data.db')

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

csrf = CSRFProtect(app)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

try:
    db.create_all()
except:
    os.remove(os.path.join(basedir, 'sensor_data.db'))
    db.create_all()


class TemperatureData(db.Model):
    """
    This model has a one to one relationship with the user model. This might be the most important table in the whole
    application because almost every other model has a foreign key referring back to it.
    """
    __tablename__ = "temperature_data"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), nullable=True)

    value = db.Column(db.Float)

    datetime = db.Column(db.String(64))

    sensor_type = db.Column(db.String(64))

    sensor_code = db.Column(db.String(64))

    @staticmethod
    def insert_data(data):
        new = TemperatureData(**data)
        db.session.add(new)
        db.session.commit()


db.create_all()
db.session.commit()

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


# https://stackoverflow.com/questions/9198334/how-to-build-up-a-html-table-with-a-simple-for-loop-in-jinja2
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


import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

# @app.route('/plot.png')
# def plot_png():
#     fig = create_figure()
#
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')
#     # full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'new_plot.png')
#     #
#     # return render_template('graphs.html', name='new_plot', url=full_filename)


import pandas as pd
import numpy as np

# import matplotlib.pyplot as plt
#
#
# def create_figure():
#     start = pd.to_datetime('2015-02-24')
#     rng = pd.date_range(start, periods=15, freq='20H')
#     df = pd.DataFrame({'datetime': rng, 'data': np.random.random(15)})
#     days = 2
#     cutoff_date = df["datetime"].iloc[-1] - pd.Timedelta(days=days)
#     df1 = df[df['datetime'] > cutoff_date]
#
#     print(df1)
#
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     # xs = range(100)
#     # ys = [random.randint(1, 50) for x in xs]
#     xs = df1['datetime']
#     ys = df1['data']
#     plt.setp(axis.xaxis.get_majorticklabels(), rotation=45)
#
#     axis.plot(xs, ys)
#     axis.set_title('Temperature Graphs')
#     axis.set_ylabel('Temperature [C]')
#     axis.set_xlabel('Time')
#     # plt.savefig('new_plot.png')
#     # plt.rcParams["figure.figsize"] = [50, 30]
#     fig.savefig('new_plot.png')
#     return fig


from bokeh.plotting import figure, show, output_file

from flask import Flask, render_template, request
import pandas as pd
from bokeh.charts import Histogram, Line
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter
from math import pi


@app.route('/sensors')
def index3():
    p = figure(title='Plots', sizing_mode='scale_width', height=200)

    p.xaxis.formatter = DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )

    p.xaxis.major_label_orientation = pi / 4

    # sensors = Sensor.query.filter_by(user_id=current_user.id).all()

    colors = ['tomato', 'limegreen', 'mediumorchid']
    data = TemperatureData.query.all()

    values = [d.value for d in data]
    datetimes = [d.datetime for d in data]
    dts = pd.to_datetime(datetimes)
    df = pd.DataFrame(list(zip(dts, values)), columns=['x', 'y'])
    df2 = df.dropna()
    print(df2)

    x = df2['x']
    y = df2['y']
    p.line(x, y, legend='Sensor 1',
           line_color=colors[0], line_dash="dotdash")
    # p.sizing_mode = 'scale_width'
    p.legend.location = "bottom_left"
    script, div = components(p)

    return render_template("bekeh_tes2t.html", script=script, div=div,
                           feature_names=['d', 'a', 'd'])


@app.route('/temperature', methods=['POST'])
@csrf.exempt
def local_data():
    print('test')
    data = request.get_json()
    print(data)
    value = data['value']
    datetime = data['datetime']
    sensor_name = data['sensor_name']
    sensor_code = data['sensor_code']
    TemperatureData.insert_data(
        {'value': value, 'datetime': datetime, 'name': sensor_name, 'sensor_code': sensor_code})
    return 'Hello'


@app.route('/shutdown', methods=['GET'])
@csrf.exempt
def shutdown():
    print('Shutting Down')
    # todo: add a thread?
    ipv4 = os.popen('sudo shutdown now').read().split("inet ")[1].split("/")[0]

    return 'Shutting Down DataLogger'


@app.route('/reboot', methods=['GET'])
@csrf.exempt
def reboot():
    print('Rebooting')
    # todo: add a thread?
    ipv4 = os.popen('sudo reboot now').read().split("inet ")[1].split("/")[0]
    return 'Rebooting DataLogger Please visit the page in a few minutes.'


@app.route('/reboot', methods=['GET'])
@csrf.exempt
def update_and_reboot_system():
    return 'Updating and Rebooting you system'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
