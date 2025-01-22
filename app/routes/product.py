from app import app, products
from flask import json, request, jsonify
from app.utils import helper
from flask_jwt_extended import jwt_required



@app.post('/add-product')
@jwt_required() 
def add_product():
    data = request.json

    name = data.get('name')
    price = data.get('price')
    amount = data.get('amount')

    if not name or not price or not amount:
        return jsonify({"error": "Product name, price and mount are required"}), 400


    if price < 0 or amount < 0 :
        return jsonify({"message":"the value of price and amount can't be negative"}), 400
    
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

    return jsonify({"message":"success",
                    "product":json.dumps(product, default=helper.json_converter)}), 201


