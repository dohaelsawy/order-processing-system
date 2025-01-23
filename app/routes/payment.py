import logging
from app import app, orders
from flask import request, jsonify
from app.services.email import send_order_confirmation_email
from bson import ObjectId
from flask_jwt_extended import get_jwt_identity, jwt_required

logger = logging.getLogger(__name__)

@app.post('/mock_payment_gateway')
@jwt_required()
def mock_payment_gateway():
    try:
        data = request.json
        card_num = data.get('card_number')
        order_id = data.get('order_id')

        if not card_num or not order_id:
            return jsonify({'error': 'Invalid payment details'}), 400
        
        to_email = get_jwt_identity()
        from_email = app.config.get('MAIL_USERNAME')

        if not from_email:
            logger.error('Mail configuration missing')
            return jsonify({'error': 'Mail configuration missing'}), 500

        order = orders.find_one({"_id": ObjectId(order_id)})
        if not order:
            logger.error(f'Order with ID {order_id} not found')
            return jsonify({'error': 'Order does not exist'}), 400

        if card_num and len(card_num) == 16:
            orders.update_one({'_id': ObjectId(order_id)}, {"$set": {'payment_status': 'success'}})

            is_send = send_order_confirmation_email(from_email, to_email, order)
            if not is_send:
                logger.error('Failed to send confirmation email')
                return jsonify({"message": "Email didn't send, please wait some time."}), 503

            return jsonify({'message': 'Success', 'transaction_id': 'txn_12345'}), 200
        else:
            logger.error(f'Payment declined for order {order_id}')
            return jsonify({'error': 'Payment declined'}), 402
    
    except Exception as e:
        logger.error(f"Unexpected error in mock_payment_gateway: {str(e)}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
