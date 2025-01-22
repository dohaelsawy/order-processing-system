from flask import Flask
from flask_login import LoginManager
from app.config import Config
from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object(Config)



login_manager = LoginManager(app)
mongo = PyMongo(app)
mail = Mail(app)
jwt = JWTManager(app)


client = mongo.cx
users = mongo.db.users
products = mongo.db.products
orders = mongo.db.orders


from app.routes import auth
from app.routes import product
from app.utils import helper
from app.routes import order
from app.services import email
from app.routes import payment

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)