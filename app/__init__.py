from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from elasticsearch import Elasticsearch
from config import Config

app = Flask(__name__, static_folder='', static_url_path='')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'
app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
  if app.config['ELASTICSEARCH_URL'] else None


from app import routes, models, errors