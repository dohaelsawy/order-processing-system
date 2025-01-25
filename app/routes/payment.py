import logging

from pymongo import ReturnDocument
import stripe
from app import app, orders
from flask import request, jsonify
from app.services.email import send_order_confirmation_email
from bson import ObjectId
from flask_jwt_extended import get_jwt_identity, jwt_required
from bson import ObjectId

logger = logging.getLogger(__name__)


@app.post('/create-payment-intent')
@jwt_required()
def create_payment_intent():
    data = request.json
    order_id = data['order_id']

    order = orders.find_one({'_id': ObjectId(order_id)})

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    try:
        intent = stripe.PaymentIntent.create(
            amount=order['total_amount'], 
            currency='usd',
            payment_method_types=['card'],
            metadata={'order_id': str(order_id)},
        )
        return jsonify({'client_secret': intent.client_secret,
                        "payment_intent_id":intent.id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@app.post('/confirm-payment')
@jwt_required()
def confirm_payment():
    return confirm_payment_func(orders)

def confirm_payment_func(orders):
    data = request.json
    payment_intent_id = data['payment_intent_id']
    payment_method_id = data['payment_method_id']

    try:
        intent = stripe.PaymentIntent.confirm(
            payment_intent_id,
            payment_method=payment_method_id,
        )
        if intent.status == 'succeeded':
            order = orders.find_one_and_update(
                {'_id': ObjectId(intent.metadata['order_id'])},
                {'$set': {'payment_status': 'successful'}},
                return_document=ReturnDocument.AFTER
            )
            response = send_confirmation_email(order)
            
            if 'error' in response:
                return jsonify(response), 500
            
            return jsonify({'message': 'Payment succeeded'}), 200
        else:
            return jsonify({'error': 'Payment failed'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

def send_confirmation_email(order):
    to_email = get_jwt_identity()
    from_email = app.config.get('MAIL_USERNAME')

    if not from_email:
        logger.error('Mail configuration missing')
        return {'error': 'Mail configuration missing'}
    

    is_send = send_order_confirmation_email(from_email, to_email, order)
    if not is_send:
        logger.error('Failed to send confirmation email')
        return {"error": "Email didn't send, please wait some time."}
    
    return {'message': 'Payment succeeded'}
    
