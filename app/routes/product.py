from app import app, products
from flask import request, jsonify
from app.utils import helper
from flask_jwt_extended import jwt_required


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
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500



def validate_product_data(data):
    name = data.get('name')
    price = data.get('price')
    amount = data.get('amount')

    if not name or price is None or amount is None:
        return {"error": "Product name, price, and amount are required"}
    
    if price < 0 or amount < 0:
        return {"error": "The value of price and amount can't be negative"}

    return None


def process_product(data):
    name = data['name']
    price = data['price']
    amount = data['amount']

    product = products.find_one({"name":name})

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
            "amount":  updated_amount
        })
        products.update_one(
            {"name":name},
            {"$set":product}
        )

    return product
