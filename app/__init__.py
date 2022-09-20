from flask import Flask

app = Flask(__name__)

app.secret_key = "qwerty"

from app import views
from app import helpers
