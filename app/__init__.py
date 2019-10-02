import sentry_sdk

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from config import Config
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://a2e152adf1ae4896b10ae1558dc58d25@sentry.io/1767305",
    integrations=[FlaskIntegration()]
)

app = Flask(__name__, static_folder='', static_url_path='')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'
login.init_app(app)

from app import routes, models, errors