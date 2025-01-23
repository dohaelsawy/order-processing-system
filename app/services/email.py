import logging
from flask_mail import Message
from app import mail
from flask import jsonify

logger = logging.getLogger(__name__)

def send_order_confirmation_email(from_email, to_email, order):
    try:
        subject = f"Order Confirmation - Order #{str(order['_id'])}"
        body = f"""
        Hello,

        Thank you for your order! Here are the details:

        Order ID: {str(order['_id'])}
        In {order['order_date']}
        Which has state {order['status']}
        Deliver at {order['shipping_address']}
        has payment status {order['payment_status']}
        payment method is {order['payment_method']}
        Purchased Items:
        """
        
        for item in order['products']:
            body += f"\n- {item['product_name']} (x{item['quantity']}) - ${item['price'] * item['quantity']:.2f}"

        body += f"""
        
        Total Amount: ${order['total_amount']:.2f}

        We hope you enjoy your purchase!

        Best regards,
        Your Store Team
        """

        msg = Message(subject=subject, sender=from_email, recipients=[to_email])
        msg.body = body
        mail.send(msg)
        return jsonify({"message": "Email sent successfully"})
    
    except Exception as e:
        logger.error(f"Failed to send order confirmation email for order {order['_id']} to {to_email}: {str(e)}")
        return jsonify({"message": f"There is something wrong, error: {e}"}), 500
