from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

from app import routes, models