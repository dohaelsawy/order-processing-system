# API Document for OPS Project 

## index
- routes 
    - auth (login, register)
    - order (create order)
    - payment (create payment intent, confirm-payment)
    - product (create product)

## General Info
- Base URL: `http://0.0.0.0:5000`

## Routes - Auth
- login API 
    - Endpoint: `/login`
    - Description: login user to generate access token 
    - Request Payload: The request body must be in JSON format and contain the following fields:
        - email (string): The email address of the user (required).
        - password (string): The password of the user (required).
        ```json
            {
            "email": "user@example.com",
            "password": "securepassword123"
            }
        ```
    - Response: The response will be in JSON format.
        - Success (200):
        ```json
            {
            "message": "Login successful",
            "token": "<JWT_TOKEN>"
            }
        ```
        - Error (400):
        ```json
            {
            "error": "Email and password are required"
            }
        ```
        - Error (401):
        ```json
            {
            "error": "Invalid credentials"
            }
        ```
        - Error (500):
        ```json
            {
            "error": "Internal server error"
            }
        ```

- register API 
    - Endpoint: `/register`
    - Description: register user to system 
    - Request Payload: The request body must be in JSON format and contain the following fields:
        - email (string): The email address of the user (required).
        - password (string): The password of the user (required).
        ```json
            {
            "email": "user@example.com",
            "password": "securepassword123"
            }
        ```
    - Response: The response will be in JSON format.
        - Success (200):
        ```json
            {
            "message": "User registered successfully"
            }
        ```
        - Error (400):
        ```json
            {
            "error": "Email and password are required"
            }
        ```
        - Error (409):
        ```json
            {
            "error": "User already exists"
            }
        ```
        - Error (500):
        ```json
            {
            "error": "Internal server error"
            }
        ```

## Routes - Product
- add product 
    - Endpoint: `/add-product`
    - Method: POST
    - Authentication: Requires JWT token (using @jwt_required()decorator).
    - Description: add product 
    - Request Payload: The request body must be in JSON format and contain the following fields:
        - name (string): The name of the product (required).
        - price (number): The price of the product (required, must be a non-negative value).
        - amount (integer): The amount of the product in stock (required, must be a non-negative value).
        ```json
            {
            "name": "Product A",
            "price": 25.00,
            "amount": 100
            }
        ```
    - Response: The response will be in JSON format.
        - Success (201):
        ```json
            {
            "message": "Success",
            "product": {
                "_id": "67915053538af665f2e3ddbc",
                "amount": 76,
                "name": "hody",
                "price": 300
            }
            }
        ```
        - Error (400):
        ```json
            {
            "error": "Product name, price, and amount are required"
            }
        ```
        - Error (500):
        ```json
            {
            "error": "An unexpected error occurred",
            "details": "Error message here"
            }
        ```


## Routes - Order
- add product 
    - Endpoint: `/create-order`
    - Method: POST
    - Authentication: Requires JWT token (using @jwt_required()decorator).
    - Description: create order
    - Request Payload: The request body must be in JSON format and contain the following fields:
        - products (array): A list of products to be ordered. Each product object must include:
            - product_id (string): The unique ID of the product (required).
            - quantity (integer): The quantity of the product to be ordered (required, must be greater than 0).

        - shipping_address (string): The shipping address for the order (required).
        - payment_method (string): The method of payment. Must be one of the following:
                "Credit Card"
                "Visa"
                "Cash" (required).
        ```json
            "products": [
                {
                "product_id": "<product_id>",
                "quantity": 2
                },
                {
                "product_id": "<product_id>",
                "quantity": 1
                }
            ],
            "shipping_address": "1234 Elm Street, Springfield, IL",
            "payment_method": "Credit Card"
        ```
    - Response: The response will be in JSON format.
        - Success (201):
        ```json
            {
            "message": "Order created successfully",
                "order": {
                    "_id": "<order_id>",
                    "user_id": "user@example.com",
                    "products": [
                    {
                        "product_id": "<product_id>",
                        "product_name": "Product A",
                        "quantity": 2,
                        "price": 25.00
                    },
                    {
                        "product_id": "<product_id>",
                        "product_name": "Product B",
                        "quantity": 1,
                        "price": 15.00
                    }
                    ],
                    "total_amount": 65.00,
                    "status": "Pending",
                    "order_date": "2025-01-23T15:30:00",
                    "shipping_address": "1234 Elm Street, Springfield, IL",
                    "payment_status": "Pending",
                    "payment_method": "Credit Card"
                }
            }
        ```
        - Error (400):
        ```json
            {
            "error": "Invalid product list"
            }
        ```
        - Error (500):
        ```json
            {
            "error": "An unexpected error occurred",
            "details": "Error message here"
            }
        ```

## Routes - Payment
- create payment intent 
    - Endpoint: `/create-payment-intent`
    - Method: POST
    - Authentication: Requires JWT token (using @jwt_required()decorator).
    - Description: create payment intent at stripe
    - Request Payload: The request body must be in JSON format and contain the following fields:
        - order_id (string, required): The ID of the order for which the payment is being initiated.
        ```json
            {"order_id": "<order_id>"}
        ```
    - Response: The response will be in JSON format.
        - Success (200):
        ```json
            {
            "client_secret": "<client_secret>",
            "payment_intent_id": "<payment_intent_id>"
            }
        ```
        - Error (404):
        ```json
            {
            "error": "Order not found"
            }
        ```
        - Error (500):
        ```json
            {
            "error": "<error_message>"
            }
        ```

- confirm payment 
    - Endpoint: `/confirm-payment`
    - Method: POST
    - Authentication: Requires JWT token (using @jwt_required()decorator).
    - Description: confirm a stripe payment intent
    - Request Payload: The request body must be in JSON format and contain the following fields:
        - payment_intent_id (string, required): The ID of the PaymentIntent to be confirmed.
        - payment_method_id (string, required): The ID of the payment method to use for confirmation.
        ```json
            {
            "payment_intent_id": "<payment_intent_id>",
            "payment_method_id": "<payment_method_id>"
            }
        ```
    - Response: The response will be in JSON format.
        - Success (200):
        ```json
            {
            "message": "Payment succeeded"
            }
        ```
        - Error (404):
        ```json
            {
            "error": "Payment failed"
            }
        ```
        - Error (500):
        ```json
            {
            "error": "<error_message>"
            }
        ``` 