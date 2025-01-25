import unittest
from unittest.mock import MagicMock, patch
from flask import Flask, json
from flask_jwt_extended import JWTManager
from app import app
from app.routes.product import add_product_func
from bson import ObjectId

class AddProductTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["JWT_SECRET_KEY"] = app.config['JWT_SECRET_KEY']
        self.jwt = JWTManager(self.app)
        self.client = self.app.test_client()

        self.mock_products = MagicMock()

    @patch("app.routes.product.products", new_callable=MagicMock)
    def test_add_product_success_new_product(self, mock_products):

        mock_products.insert_one.return_value.inserted_id = ObjectId("507f1f77bcf86cd799439014")
        mock_products.find_one.side_effect = [None]

        with self.app.test_request_context(json={"name": "Test Product", "price": 10, "amount": 100}):
            response = add_product_func(mock_products)

        response_body, status_code = response
        response_data = json.loads(response_body.get_data(as_text=True))

        self.assertEqual(status_code, 201)
        self.assertEqual(response_data["message"], "Success")
        self.assertIn("product", response_data)
        self.assertEqual(response_data["product"]["name"], "Test Product")
        self.assertEqual(response_data["product"]["price"], 10)
        self.assertEqual(response_data["product"]["amount"], 100)




    @patch("app.routes.product.products", new_callable=MagicMock)
    def test_add_product_success_existing_product(self, mock_products):
        self.mock_products.reset_mock()

        product_data = {
            "name": "Existing Product",
            "price": 10,
            "amount": 100
        }

        existing_product = {
            "_id": ObjectId("507f1f77bcf86cd799439011"),
            "name": "Existing Product",
            "price": 15,
            "amount": 50
        }
        mock_products.find_one.return_value = existing_product

        def update_side_effect(filter, update):
            existing_product.update(update["$set"])
            return MagicMock(matched_count=1)

        mock_products.update_one.side_effect = update_side_effect

        with self.app.test_request_context(json=product_data):
            response = add_product_func(mock_products)

        response_body, status_code = response
        response_data = json.loads(response_body.get_data(as_text=True))

        self.assertEqual(status_code, 201)
        self.assertEqual(response_data["message"], "Success")
        self.assertIn("product", response_data)
        self.assertEqual(response_data["product"]["name"], "Existing Product")
        self.assertEqual(response_data["product"]["price"], 10)
        self.assertEqual(response_data["product"]["amount"], 150)
        self.assertEqual(str(response_data["product"]["_id"]), "507f1f77bcf86cd799439011")




    @patch("app.routes.product.products", new_callable=MagicMock)
    def test_add_product_missing_fields(self, mock_products):
        product_data = {
            "name": "Test Product",
            "price": 10
        }

        with self.app.test_request_context(json=product_data):
            response = add_product_func(mock_products)

        response_body, status_code = response
        response_data = json.loads(response_body.get_data(as_text=True))

        self.assertEqual(status_code, 400)
        self.assertEqual(response_data["error"], "Product name, price, and amount are required")




    @patch("app.routes.product.products", new_callable=MagicMock)
    def test_add_product_negative_values(self, mock_products):
        product_data = {
            "name": "Test Product",
            "price": -10,
            "amount": -100
        }

        with self.app.test_request_context(json=product_data):
            response = add_product_func(mock_products)

        response_body, status_code = response
        response_data = json.loads(response_body.get_data(as_text=True))

        self.assertEqual(status_code, 400)
        self.assertEqual(response_data["error"], "The value of price and amount can't be negative")
