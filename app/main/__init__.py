from flask import Blueprint
from ..model import Permission
main = Blueprint('main', __name__)

from . import view, errors

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)