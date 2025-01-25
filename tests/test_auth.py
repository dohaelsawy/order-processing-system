import unittest
from unittest.mock import MagicMock
import bcrypt
from flask import Flask, json
from flask_jwt_extended import JWTManager
from app.routes.auth import register_user, login_user
from app import app

class RegisterUserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        self.mock_users = MagicMock()


    def test_register_user_success(self):
        self.mock_users.find_one.return_value = None
        self.mock_users.insert_one.return_value = None
        
        with self.app.test_request_context(json={"email": "test@example.com", "password": "password123"}):
            response = register_user(self.mock_users)

            response_body, status_code = response
            expected_response = {"message": "User registered successfully"}
            
            self.assertEqual(status_code, 201)
            self.assertEqual(json.loads(response_body.get_data(as_text=True)), expected_response)


    def test_register_user_already_exists(self):
        self.mock_users.find_one.return_value = {"email": "test@example.com"}
        
        with self.app.test_request_context(json={"email": "test@example.com", "password": "password123"}):
            response = register_user(self.mock_users)

            response_body, status_code = response
            expected_response =  {"error": "User already exists"}

            self.assertEqual(status_code, 409)
            self.assertEqual(json.loads(response_body.get_data(as_text=True)), expected_response)


    def test_register_email_missing(self):        
        with self.app.test_request_context(json={"password": "password123"}):
            response = register_user(self.mock_users)

            response_body, status_code = response
            expected_response =  {"error": "Email and password are required"}

            self.assertEqual(status_code, 400)
            self.assertEqual(json.loads(response_body.get_data(as_text=True)), expected_response)

    
    def test_register_password_missing(self):        
        with self.app.test_request_context(json={"email": "test@example.com"}):
            response = register_user(self.mock_users)

            response_body, status_code = response
            expected_response =  {"error": "Email and password are required"}

            self.assertEqual(status_code, 400)
            self.assertEqual(json.loads(response_body.get_data(as_text=True)), expected_response)




class LoginUserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["JWT_SECRET_KEY"] = app.config['JWT_SECRET_KEY']
        self.jwt = JWTManager(self.app)
        self.client = self.app.test_client()
        self.mock_users = MagicMock()


    def test_login_user_success(self):
        hashed_password = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())
        self.mock_users.find_one.return_value = {
            "email": "test@example.com",
            "password": hashed_password
        }

        with self.app.test_request_context(json={"email": "test@example.com", "password": "password123"}):
            response = login_user(self.mock_users)

            response_body, status_code = response
            response_data = json.loads(response_body.get_data(as_text=True))

            self.assertEqual(status_code, 200)
            self.assertIn("message", response_data)
            self.assertIn("token", response_data)
            self.assertEqual(response_data["message"], "Login successful")


    def test_login_user_invalid_credentials(self):
        self.mock_users.find_one.return_value = None

        with self.app.test_request_context(json={"email": "test@example.com", "password": "wrongpassword"}):
            response = login_user(self.mock_users)

            response_body, status_code = response            
            response_data = json.loads(response_body.get_data(as_text=True))

            self.assertEqual(status_code, 401)            
            self.assertEqual(response_data, {"error": "Invalid credentials"})


    def test_login_user_missing_fields(self):
        with self.app.test_request_context(json={"email": ""}):
            response = login_user(self.mock_users)
            
            response_body, status_code = response
            response_data = json.loads(response_body.get_data(as_text=True))
            
            self.assertEqual(status_code, 400)            
            self.assertEqual(response_data, {"error": "Email and password are required"})


    def test_login_user_internal_server_error(self):
        self.mock_users.find_one.side_effect = Exception("Database error")

        with self.app.test_request_context(json={"email": "test@example.com", "password": "password123"}):
            response = login_user(self.mock_users)
            
            response_body, status_code = response            
            response_data = json.loads(response_body.get_data(as_text=True))

            self.assertEqual(response_data, {"error": "Internal server error"})
            self.assertEqual(status_code, 500)
