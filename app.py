# todo: This will create a mini webpage for setting the tokens etc for the server.

# Testing Crontab


import json
import glob
import os

from flask import Flask, redirect, flash
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterSensor, DeleteSensorForm

from bokeh.plotting import figure

from flask import render_template, request
import pandas as pd
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter
from math import pi

template_dir = os.path.abspath('./')
static_dir = os.path.abspath('./')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

app.secret_key = 'lkdja;ldksjas;lkfblamn'

app.config['UPLOAD_FOLDER'] = os.path.abspath('./')
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sensor_data.db')

csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

try:
    db.create_all()
except Exception as e:
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


def get_ds18b20_paths():
    """
    This method returns the path to the ds18b20 sensors in the raspberry 1-wire protocol implementation.
    :return:
    """
    base_dir = '/sys/bus/w1/devices/'
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
    form = RegisterSensor(prefix='form')

    with open('parameters.json') as parameters:
        data = json.load(parameters)

    ds18b20s = data['ds18b20']
    find_ds18b20_paths = get_ds18b20_paths()
    # find_ds18b20_paths = [('28-00000b246922', 'path')]
    try:
        detected_ds18b20s = [d[0] for d in find_ds18b20_paths]
    except:
        detected_ds18b20s = []

    output = []
    for dd in ds18b20s:
        output.append(str([dd['sensor_name'], dd['sensor_code'], dd['token'], dd['user_id']]))

    form1 = DeleteSensorForm(prefix='form1')
    codes = []
    for d, dd in enumerate(ds18b20s):
        code = dd['sensor_code']
        name = dd['sensor_name']
        codes.append((d, name + ' ' + code))

    form1.sensor_name.choices = codes

    if form.validate_on_submit() and form.submit1.data:
        flag = False
        print(request.form)
        if request.form['form-sensor_code'] in detected_ds18b20s:
            for d, ds in enumerate(ds18b20s):
                if ds['sensor_code'] == request.form['form-sensor_code']:
                    ds = request.form
                    flag = True
                    print(flag)
                    data['ds18b20'][d] = ds
                    break
            if not flag:
                ds = request.form
                temp = {}
                for k in ds.keys():
                    print(k)
                    new_key = k[5:]
                    temp[new_key] = ds[k]
                data['ds18b20'].append(temp)
                #     data['ds18b20'].append(ds)
            with open('parameters.json', 'w') as f:
                json.dump(data, f)
            flash('Please Reboot the system (if you are done)')
            # os.system('/etc/init.d/cron reload')
            # flash('Reloaded Cron.')
        else:
            flash('Sensor is not connected please check if the sensor code exists on the right.')
        return redirect('/')
    elif form1.validate_on_submit() and form1.submit2.data:
        ds18b20s.pop(form1.sensor_name.data)
        data['ds18b20'] = ds18b20s
        flash('Erased Sensor Info Succesfully')
        with open('parameters.json', 'w') as data_file:
            json.dump(data, data_file)
        return redirect('/')

    return render_template('./index.html', form=form, form1=form1, datasources=output,
                           detected_ds18b20s=detected_ds18b20s)


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

    try:
        values = [d.value for d in data]
        datetimes = [d.datetime for d in data]
        dts = pd.to_datetime(datetimes)
        df = pd.DataFrame(list(zip(dts, values)), columns=['x', 'y'])
        # todo: add parameter in form to show last n results.
        df2 = df.dropna().iloc[-20:]

        x = df2['x']
        y = df2['y']
    except Exception as e:
        print(e)
        x = []
        y = []
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


def reboot():
    # time.sleep(5)
    os.popen('sudo reboot now')


def shutdown():
    # time.sleep(5)
    os.popen('sudo shutdown now')


def update_and_reboot():
    # time.sleep(5)
    os.popen('git pull')
    # time.sleep(5)
    os.popen('sudo reboot')


@app.route('/shutdown', methods=['GET'])
@csrf.exempt
def shutdown():
    print('Shutting Down')
    # todo: add a thread?
    # threading.Thread(target=shutdown).start()
    # shutdown()
    os.popen('sudo shutdown now')

    # ipv4 = os.popen('sudo shutdown now')
    # flash('Shutting Down DataLogger. To turn back on please remove the power source and reconnect it')
    # return redirect('/')
    return 'Shutting Down DataLogger. To turn back on please remove the power source and reconnect it'


@app.route('/reboot', methods=['GET'])
@csrf.exempt
def reboot():
    print('Rebooting')
    # reboot()
    os.popen('sudo reboot now')

    # threading.Thread(target=reboot).start()
    # flash('Rebooting DataLogger. Visit this site in a few minutes.')

    # todo: add a thread?
    # return redirect('/')
    return 'Rebooting DataLogger. Visit this site in a few minutes.'


@app.route('/reboot', methods=['GET'])
@csrf.exempt
def update_and_reboot_system():
    return 'Updating and Rebooting you system'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
