from flask.ext.wtf  import Form
from wtforms import TextField, PasswordField, StringField, PasswordField,SubmitField
from wtforms.validators import Required, Email, EqualTo

class LoginForm(Form):
    email = TextField('Email Address', [Email(),
        Required(message='Email authentication required')])
    password = PasswordField('Password',[Required(message='Input your password')])
    submit = SubmitField('submit')

class signup(Form):
    name = StringField('Enter your name', validators=[Required()]) 
    email = StringField('Enter email',validators=[Required()])
    password = PasswordField(' password', validators= [Required()])
    submit = SubmitField('submit')


    