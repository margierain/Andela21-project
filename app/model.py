# from . import db
from datetime import datetime

from flask import current_app

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

from . import login_manager
from . import db

# base model is to be inherited
class Base(db.Model):
    __abstract__  = True

    id  = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())



class User(UserMixin, Base):
    __tablename__='user'

    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(192), nullable=False)
    password_hash =db.Column(db.String(4))
    confirm = db.Column(db.Boolean, default=False)

    last_seen = db.Column(db.DateTime(), default=datetime.now)

    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    
    

    @property
    def password(self):
        raise AttributeError('password is are hidden attributes')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)  

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def generate_confirmation_token(self, expiration=3600):
        s =Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False
        self.confirmed =True
        db.session.add(self)
        return True

    def ping(self):
        self.last_seen = datetime.utcnow()
        deb.session.add(self)

          

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:

            return False
        self.password =new_password
        db.session.add(self)
        return True      

    def generate_email_change(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return  s.dumps({'change_email': self.id, 'new_email':new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data =s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False

        new_email = data.get('new_email') 
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False

        self.email = new_email
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.name