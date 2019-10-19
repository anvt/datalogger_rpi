from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required, Length, DataRequired


class RegisterSensor(Form):
    """
    This is the Login Form class. It has the Form as a parent. When used in templating the wtf automatically
    generates a Form just as seen when we navigate towards /login page.
    """
    sensor_name = StringField('Name')#,validators=[DataRequired()])

    sensor_code = StringField('Sensor Code')#, validators=[DataRequired()])

    user_id = StringField('User ID')#, validators=[DataRequired()])

    token = StringField('Token')#, validators=[DataRequired()])

    submit1 = SubmitField('Save')