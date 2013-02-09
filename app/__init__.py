from flask import Flask, redirect, url_for, session, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask_oauth import OAuth

app = Flask(__name__)
app.config.from_object('config')
app.debug = True
db = SQLAlchemy(app)

from app import views, models, hooks
