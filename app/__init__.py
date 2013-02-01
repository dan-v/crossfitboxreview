from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.social import Social
from flask.ext.social.datastore import SQLAlchemyConnectionDatastore

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models, hooks
