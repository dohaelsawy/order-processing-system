from app import app, orders
from flask import request, jsonify
from app.services.email import send_order_confirmation_email
from bson import ObjectId
from flask_jwt_extended import get_jwt_identity, jwt_required

@app.post('/payment')
@jwt_required()
def payment():
    data = request.json
    order_id = data.get('order_id')
    to_email = get_jwt_identity()

    if not order_id:
        return jsonify({"message":"order is required"})

    if not check_payment_status() :
        return jsonify({"message":"payment didn't complete correctly"})
    
    orders.update_one({'_id':ObjectId(order_id)},{"$set":{'payment_status':'successful'}})
    
    order = orders.find_one({"_id":ObjectId(order_id)})
    
    if not order :
        return jsonify({"message":"no such order exist"})
    
    is_send = send_order_confirmation_email(app.config['MAIL_USERNAME'],to_email, order_id, order['products'],order['total_amount']
                                            ,order['order_date'],order['status'], order['shipping_address'],order['payment_status'],
                                            order['payment_method'])
    
    if not is_send:
        return jsonify({"message":"email doesn't send, please wait some time."})
    
    return jsonify({"message":"email sent"})






def check_payment_status():
    return True