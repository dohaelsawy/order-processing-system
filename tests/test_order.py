import unittest
from unittest.mock import MagicMock, patch, Mock
from flask import Flask, json
from flask_jwt_extended import JWTManager
from bson import ObjectId
from app.routes.order import create_order_func
from app import app

class CreateOrderTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["JWT_SECRET_KEY"] = app.config['JWT_SECRET_KEY']
        self.jwt = JWTManager(self.app)
        self.client = self.app.test_client()

        self.mock_orders = MagicMock()
        self.mock_products = MagicMock()


    @patch("app.routes.order.get_jwt_identity")
    @patch("app.routes.order.products", new_callable=MagicMock)
    @patch("app.routes.order.orders", new_callable=MagicMock)
    @patch("app.routes.order.client", new_callable=MagicMock)
    def test_create_order_success(self, mock_client, mock_orders, mock_products, mock_get_jwt_identity):
        mock_get_jwt_identity.return_value = "test@example.com"
        def mock_find_one(query):
            if query["_id"] == ObjectId("6791df42f3e5dae0f0f4e7f1"):
                return {
                    "_id": ObjectId("6791df42f3e5dae0f0f4e7f1"),
                    "name": "Test Product",
                    "price": 10,
                    "amount": 100,
                }
            return None

        mock_products.find_one.side_effect = mock_find_one

        session_mock = MagicMock()
        mock_client.start_session.return_value.__enter__.return_value = session_mock

        mock_orders.insert_one.return_value.inserted_id = ObjectId("679162e639e87678196c8fac")
        mock_orders.find_one.return_value = {
            "_id": ObjectId("679162e639e87678196c8fac"),
            "status": "Pending"
        }

        order_data = {
            "products": [{"product_id": "6791df42f3e5dae0f0f4e7f1", "quantity": 2}],
            "shipping_address": "123 Test Street",
            "payment_method": "Cash"
        }

        with self.app.test_request_context(json=order_data):
            response = create_order_func(mock_orders)

        response_body, status_code = response
        response_data = json.loads(response_body.get_data(as_text=True))

        self.assertEqual(status_code, 201)
        self.assertEqual(response_data["message"], "Order created successfully")
        self.assertIn("order", response_data)



    @patch("app.routes.order.get_jwt_identity")
    def test_create_order_invalid_data(self, mock_get_jwt_identity):
        mock_get_jwt_identity.return_value = "test@example.com"

        invalid_order_data = {
            "products": "invalid_product_list",
            "shipping_address": "",
            "payment_method": "Bitcoin"
        }

        with self.app.test_request_context(json=invalid_order_data):
            response = create_order_func(self.mock_orders)

        response_body, status_code = response
        response_data = json.loads(response_body.get_data(as_text=True))

        self.assertEqual(status_code, 400)
        self.assertIn("error", response_data)



    @patch("app.routes.order.get_jwt_identity")
    @patch("app.routes.order.products", new_callable=MagicMock)
    def test_create_order_product_not_found(self, mock_products, mock_get_jwt_identity):
        mock_get_jwt_identity.return_value = "test@example.com"
        mock_products.find_one.return_value = None

        order_data = {
            "products": [{"product_id": "invalid_product_id", "quantity": 2}],
            "shipping_address": "123 Test Street",
            "payment_method": "Cash"
        }

        with self.app.test_request_context(json=order_data):
            response = create_order_func(self.mock_orders)

        response_body, status_code = response
        response_data = json.loads(response_body.get_data(as_text=True))
        
        self.assertEqual(status_code, 400)
        self.assertIn("error", response_data)


if __name__ == "__main__":
    unittest.main()
