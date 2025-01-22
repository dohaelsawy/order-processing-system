from flask import json, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app import app, products, orders, client
from app.utils import helper
from datetime import datetime
from pymongo.errors import PyMongoError


PAYMENT_METHODS = ['Credit Card','Visa','Cash']

@app.post("/create-order")
@jwt_required()
def create_order():

    user_email = get_jwt_identity()
    
    data = request.json
    product_list = data.get("products") 
    shipping_address = data.get("shipping_address")
    payment_method = data.get("payment_method")
    
    if not product_list or not isinstance(product_list, list):
        return jsonify({"error": "Invalid product list"}), 400
    
    if not shipping_address:
        return jsonify({"error": "Shipping address is required"}), 400
    
    if payment_method not in PAYMENT_METHODS:
        return jsonify({"error": f"Only these payment methods are available {PAYMENT_METHODS}"}), 400
    
    
    total_amount = 0
    order_products = []

    try:

        with client.start_session() as session:
            with session.start_transaction():

                for product in product_list:
                    product_id = product['product_id']
                    quantity = product['quantity']
                    
                    if not ObjectId.is_valid(product_id) or not isinstance(quantity, int) or quantity <= 0:
                        return jsonify({"error": "Invalid product data"}), 400
                    
                    product = products.find_one({"_id": ObjectId(product_id)})
                    if not product:
                        return jsonify({"error": f"Product with ID {product_id} not found"}), 404
                    
                    print(product)
                    
                    if product["amount"] < quantity:
                        return jsonify({"error": f"Not enough stock for product {product['name']}"}), 400
                    
                    products.update_one(
                        {"_id": ObjectId(product_id)},
                        {"$inc": {"amount": -quantity}}
                    )
                    
                    order_products.append({
                        "product_id": product_id,
                        "product_name": product["name"],
                        "quantity": quantity,
                        "price": product["price"]
                    })
                    total_amount += (product["price"] * quantity)
                
                order = {
                    "user_id": user_email,
                    "products": order_products,
                    "total_amount": total_amount,
                    "status": "Pending",
                    "order_date": datetime.now(),
                    "shipping_address": shipping_address,
                    "payment_status": "Pending",
                    "payment_method": payment_method,
                }
                result = orders.insert_one(order)
                
                created_order = orders.find_one({"_id": result.inserted_id})
                
        return jsonify({"message": "Order created successfully",
                        "order": json.dumps(created_order, default=helper.json_converter)}), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except PyMongoError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
