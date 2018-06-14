from flask import Blueprint

book = Blueprint('books', __name__)

from . import views

