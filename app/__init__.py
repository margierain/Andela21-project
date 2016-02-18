from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap

from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
bootstrap = Bootstrap(app)
# config
app.config.from_object('config')

db = SQLAlchemy(app)
#register a blueprint

from app.mod_auth.view import mod_auth as auth_mod
app.register_blueprint(auth_mod)
db.create_all()