import logging
from app import app, products
from flask import request, jsonify
from app.utils import helper
from flask_jwt_extended import jwt_required

logger = logging.getLogger(__name__)

@app.post('/add-product')
@jwt_required()
def add_product():
    data = request.json

    validation_error = validate_product_data(data)
    if validation_error:
        return jsonify(validation_error), 400

    try:
        product = process_product(data)
        return jsonify({
            "message": "Success",
            "product": helper.json_converter(product)
        }), 201
    except Exception as e:
        logger.error(f"Unexpected error while adding product: {str(e)}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

def validate_product_data(data):
    name = data.get('name')
    price = data.get('price')
    amount = data.get('amount')

    if not name or price is None or amount is None:
        logger.error("Product name, price, or amount is missing in the request data")
        return {"error": "Product name, price, and amount are required"}
    
    if price < 0 or amount < 0:
        logger.error(f"Invalid product data: price or amount cannot be negative (price: {price}, amount: {amount})")
        return {"error": "The value of price and amount can't be negative"}

    return None

def process_product(data):
    name = data['name']
    price = data['price']
    amount = data['amount']

    try:
        product = products.find_one({"name": name})

        if not product:
            product = {
                "name": name,
                "price": price,
                "amount": amount
            }
            products.insert_one(product)

        else:
            updated_amount = amount + product['amount']
            product.update({
                "price": price,
                "amount": updated_amount
            })
            products.update_one(
                {"name": name},
                {"$set": product}
            )
        
        return product
    
    except Exception as e:
        logger.error(f"Error while processing product {name}: {str(e)}")
        raise
