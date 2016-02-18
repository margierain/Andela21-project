from flask.ext.wtf  import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Email, EqualTo

class LoginForm(Form):
    email = TextField('Email Address', [Email(),
        Required(message='Email authentication required')])
    password = PasswordField('Password',[Required(message='Input your password')])