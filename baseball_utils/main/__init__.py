from flask import Blueprint

bp = Blueprint('main', __name__)

from baseball_utils.main import routes
