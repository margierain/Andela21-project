from flask import Blueprint


# Define a blueprint

auth = Blueprint('auth',__name__, url_prefix='/auth')



from . import view