# API Document for OPS Project 

## index
- routes 
    - auth (login, register)
    - order (create order)
    - payment (mock payment gateway)
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
- mock payment gateway 
    - Endpoint: `/mock-payment-gateway`
    - Method: POST
    - Authentication: Requires JWT token (using @jwt_required()decorator).
    - Description: mock payment process
    - Request Payload: The request body must be in JSON format and contain the following fields:
        - card_number (string): The 16-digit card number for processing the payment (required).
        - order_id (string): The ID of the order for which the payment is being processed (required).
        ```json
            {
            "card_number": "1234567812345678",
            "order_id": "64b3fcf95724dc1b6f8a4a90"
            }
        ```
    - Response: The response will be in JSON format.
        - Success (201):
        ```json
            {
            "message": "Success",
            "transaction_id": "txn_12345"
            }
        ```
        - Error (400):
        ```json
            {
            "error": "Invalid payment details"
            }
        ```
        or 
        ```json
            {
            "error": "Order does not exist"
            }
        ```
        - Error (402):
        ```json
            {
            "error": "Payment declined"
            }
        ```
        - Error (503):
        ```json
            {
            "message": "Email didn't send, please wait some time."
            }
        ```
        - Error (500):
        ```json
            {
            "error": "An unexpected error occurred",
            "details": "Error message here"
            }
        ```
