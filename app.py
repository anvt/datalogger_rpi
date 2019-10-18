# todo: This will create a mini webpage for setting the tokens etc for the server.


from flask import Flask, render_template, request, redirect
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


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegisterSensor()
    with open('parameters.json') as parameters:
        data = json.load(parameters)

    ds18b20s = data['ds18b20']

    output = []
    for dd in ds18b20s:
        output.append(str([dd['sensor_name'],dd['sensor_code'],dd['token'],dd['user_id']]))

    if form.validate_on_submit():
        flag=False
        print(request.form)
        for d, ds in enumerate(ds18b20s):

            if ds['sensor_code'] == request.form['sensor_code']:
                ds = request.form
                flag=True
                print(flag)
                data['ds18b20'][d] = ds
                break
        if not flag:
            data['ds18b20'].append(request.form)
            #     data['ds18b20'].append(ds)
        with open('parameters.json', 'w') as f:
            json.dump(data, f)
        # return redirect('/')
    return render_template('./index.html', form=form, datasources=output)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
