import logging
from flask import json, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app import app, products, orders, client
from app.utils import helper
from datetime import datetime
from pymongo.errors import PyMongoError

PAYMENT_METHODS = ['Credit Card', 'Visa', 'Cash']
logger = logging.getLogger(__name__)

@app.post("/create-order")
@jwt_required()
def create_order():
    user_email = get_jwt_identity()
    data = request.json

    validation_error = validate_order_data(data)
    if validation_error:
        return jsonify(validation_error), 400

    try:
        with client.start_session() as session:
            with session.start_transaction():
                total_amount, order_products = process_order_products(data["products"])
                order_id = save_order(user_email, order_products, total_amount, data)
                created_order = orders.find_one({"_id": order_id})

        return jsonify({
            "message": "Order created successfully",
            "order": helper.json_converter(created_order)
        }), 201

    except ValueError as e:
        logger.error(f"ValueError occurred: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except PyMongoError as e:
        logger.error(f"Database error: {str(e)}")
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

def validate_order_data(data):
    product_list = data.get("products")
    shipping_address = data.get("shipping_address")
    payment_method = data.get("payment_method")

    if not product_list or not isinstance(product_list, list):
        return {"error": "Invalid product list"}

    if not shipping_address:
        return {"error": "Shipping address is required"}

    if payment_method not in PAYMENT_METHODS:
        return {"error": f"Only these payment methods are available {PAYMENT_METHODS}"}

    return None

def process_order_products(product_list):
    total_amount = 0
    order_products = []

    for product in product_list:
        product_id = product['product_id']
        quantity = product['quantity']

        if not ObjectId.is_valid(product_id) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Invalid product data")

        product_data = products.find_one({"_id": ObjectId(product_id)})
        if not product_data:
            raise ValueError(f"Product with ID {product_id} not found")

        if product_data["amount"] < quantity:
            raise ValueError(f"Not enough stock for product {product_data['name']}")

        products.update_one(
            {"_id": ObjectId(product_id)},
            {"$inc": {"amount": -quantity}},
        )

        order_products.append({
            "product_id": product_id,
            "product_name": product_data["name"],
            "quantity": quantity,
            "price": product_data["price"]
        })

        total_amount += (product_data["price"] * quantity)

    return total_amount, order_products

def save_order(user_email, order_products, total_amount, data):
    order = {
        "user_id": user_email,
        "products": order_products,
        "total_amount": total_amount,
        "status": "Pending",
        "order_date": datetime.now(),
        "shipping_address": data["shipping_address"],
        "payment_status": "Pending",
        "payment_method": data["payment_method"],
    }
    result = orders.insert_one(order)
    return result.inserted_id
