from flask.ext.wtf  import Form
from flask import flash
from wtforms import TextField, BooleanField, PasswordField, StringField, PasswordField,SubmitField,FileField
from wtforms.validators import Required, Email, EqualTo, Length, Email, Regexp, ValidationError, regexp
from app.model import User,Post,Role 
from werkzeug import secure_filename
from flask.ext.pagedown.fields import PageDownField

class PostForm(Form):
    product = StringField('Product name:', validators=[Required()]) 
    short_description = StringField('Short description', validators=[Required(), Length(1,64)]) 
    Long_description = StringField('Long description', validators=[Required(), Length(1,225)]) 
    uploadPhotoes = FileField(u'Image File')
    price = StringField('Price', validators= [Required()])
    submit = SubmitField('Create store')

    def upload(request):
        form = PostForm(request.POST)
        if form.uploadPhotoes.data:
            uploadPhotoes_data = request.FILES[form.uploadPhotoes.name].read()
            open(os.path.join(BASE_DIR, 'app.sqlite', form.uploadPhotoes.data), 'w').write(uploadPhotoes_data)



    
class AdminProfile(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    name = StringField(
        'Username',
        validators=[Required(), Length(1, 64),
                    Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                           'Usernames should only contain letters, numbers, dots or underscores'
                           )
                    ]
    )
    name = StringField('Real Name', validators=[Length(0, 64)]) 
    is_admin = BooleanField("Is Admin")  
    submit = SubmitField('Admin profile')

    def __init__(self, user, *args, **kwargs):
        super(AdminProfile, self).__init__(*args, **kwargs)
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered.')

    def validate_name(self, field):
        if field.data != self.user.name and User.query.filter_by(name=field.data).first():
            raise ValidationError("Username is taken")



