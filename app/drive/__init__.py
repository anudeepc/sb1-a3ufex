from flask import Blueprint

drive = Blueprint('drive', __name__)

from . import routes