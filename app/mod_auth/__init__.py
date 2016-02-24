from flask import Blueprint
# Define a blueprint
mod_auth = Blueprint('mod_auth',__name__, url_prefix='/auth')
from . import view