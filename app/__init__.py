from flask import Flask, jsonify
from flask_login import LoginManager
from app.config import Config
from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_jwt_extended import JWTManager
import stripe

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)


login_manager = LoginManager(app)
mongo = PyMongo(app)
mail = Mail(app)
jwt = JWTManager(app)

stripe.api_key = app.config['STRIPE_SECRET_KEY']


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


@app.errorhandler(500)
def err500(e):
    return jsonify({"error":f"something went wrong, {e}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)