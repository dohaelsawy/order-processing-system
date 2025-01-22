from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_pymongo import PyMongo
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object(Config)



login_manager = LoginManager(app)
mongo = PyMongo(app)
mail = Mail(app)



users = mongo.db.users
inventory = mongo.db.products
orders = mongo.db.orders