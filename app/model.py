# from . import db
from datetime import datetime

from flask import current_app, request

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from sqlalchemy_imageattach.entity import Image, image_attachment
from . import login_manager
from . import db
import hashlib
from markdown import markdown
import bleach
from flask.ext.social import Social
from flask.ext.social.datastore import SQLAlchemyConnectionDatastore


class Role(db.Model):
    __tablename__='roles'
    
    id  = db.Column(db.Integer, primary_key=True)
    
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users=db.relationship('User',backref='role',lazy='dynamic')
    
class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x80 #0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80    



    @staticmethod
    def insert_roles():
        roles = {
                'User':(Permission.FOLLOW |
                        Permission.COMMENT |
                        Permission.WRITE_ARTICLES, True),
                'Moderator':(Permission.FOLLOW |
                        Permission.COMMENT |
                        Permission.WRITE_ARTICLES |
                        Permission.MODERATE_COMMENTS, False),
                'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(192), nullable=False)
    password_hash =db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    avatar_hash = db.Column(db.String(32))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.now)

    role_id =db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
   
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['JOKENIA_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
            if self.email is not None and self.avatar_hash is None:
                self.avatar_hash = hashlib.md5(
                    self.email.encode('utf-8')).hexdigest()            

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
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):    
        s =Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False
        print("Getting into confirmations...")
        self.confirmed =True
        db.session.add(self)
        db.session.commit()
        return True

    
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

          

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
        # change profile pic
        self.email = new_email
        self.avatar_hash = hashlib.md5(
        self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
                                                                    url=url, hash=hash, size=size, 
                                                                    default=default, rating=rating)    


    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions    

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)



def __repr__(self):
    return '<User %r>' % self.name



    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                    name=forgery_py.internet.user_name(True),
                    password=forgery_py.lorem_ipsum.word(),
                    confirmed=True,
                    location=forgery_py.address.city(),
                    member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()        

# model db for main 

class Post(db.Model):
    __tablename__ = 'posts'# this is the product section    

    id = db.Column(db.Integer, primary_key=True)
    product= db.Column(db.String, nullable=False)
    short_description = db.Column(db.String(64))
    Long_description = db.Column(db.String(225))
    uploadPhotoes = db.Column(db.String(255))
    price = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        
        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Post(product=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                    short_description=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                    Long_description=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                    uploadPhotoes=forgery_py.lorem_ipsum.images(randint(1, 3)),
                    price=forgery_py.lorem_ipsum.numbers(randint(1, 3)),
                    timestamp=forgery_py.date.date(True),
                                    author=u)
            db.session.add(p)
            db.session.commit()
