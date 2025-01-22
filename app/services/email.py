from flask_mail import Message
from app import mail


def send_order_confirmation_email(from_email,to_email, order_id, purchased_items, total_amount, order_date,status,shipping_address,payment_status,payment_method):
    subject = f"Order Confirmation - Order #{order_id}"
    body = f"""
    Hello,

    Thank you for your order! Here are the details:

    Order ID: {order_id}
    In {order_date}
    Which has state {status}
    Deliver at {shipping_address}
    has payment status {payment_status}
    payment method is {payment_method}
    Purchased Items:
    """
    
    for item in purchased_items:
        body += f"\n- {item['product_name']} (x{item['quantity']}) - ${item['price'] * item['quantity']:.2f}"

    body += f"""
    
    Total Amount: ${total_amount:.2f}

    We hope you enjoy your purchase!

    Best regards,
    Your Store Team
    """

    msg = Message(subject=subject, sender=from_email, recipients=[to_email])
    msg.body = body
    mail.send(msg)
    return True
    
