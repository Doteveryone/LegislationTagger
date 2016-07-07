import json
import os
from flask import Flask
from mongoengine import *
from flask_mongoengine import MongoEngine
from flask.ext.security import Security, MongoEngineUserDatastore
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(os.environ.get('SETTINGS', 'config.DevelopmentConfig'))
db = MongoEngine(app)
mail = Mail(app)

import views
import models
import forms

users = MongoEngineUserDatastore(db, models.User, models.Role)
security = Security(app, users, register_form=forms.RegisterUserForm)