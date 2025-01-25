import unittest
from unittest.mock import MagicMock, patch
from flask import Flask, json
from bson import ObjectId
from app.routes.payment import confirm_payment_func

class ConfirmPaymentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()

        self.mock_orders = MagicMock()

    @patch("app.routes.payment.stripe.PaymentIntent.confirm")
    @patch("app.routes.payment.send_confirmation_email")
    def test_confirm_payment_success(self, mock_send_email, mock_stripe_confirm):
        mock_stripe_confirm.return_value = MagicMock(
            status='succeeded',
            metadata={'order_id': '507f1f77bcf86cd799439014'}
        )

        mock_order = {
            '_id': ObjectId('507f1f77bcf86cd799439014'),
            'payment_status': 'successful'
        }
        self.mock_orders.find_one_and_update.return_value = mock_order

        mock_send_email.return_value = {"message": "Email sent successfully"}

        with self.app.test_request_context(
            json={
                'payment_intent_id': 'pi_12345',
                'payment_method_id': 'pm_12345'
            }
        ):
            response = confirm_payment_func(self.mock_orders)

        response_body, status_code = response
        response_data = json.loads(response_body.get_data(as_text=True))

        self.assertEqual(status_code, 200)
        self.assertEqual(response_data['message'], 'Payment succeeded')
        mock_stripe_confirm.assert_called_once_with(
            'pi_12345', payment_method='pm_12345'
        )
        self.mock_orders.find_one_and_update.assert_called_once()
        mock_send_email.assert_called_once_with(mock_order)



    @patch("app.routes.payment.stripe.PaymentIntent.confirm")
    @patch("app.routes.payment.send_confirmation_email")
    def test_confirm_payment_email_failure(self, mock_send_email, mock_stripe_confirm):
        mock_stripe_confirm.return_value = MagicMock(
            status='succeeded',
            metadata={'order_id': '507f1f77bcf86cd799439014'}
        )

        mock_order = {
            '_id': ObjectId('507f1f77bcf86cd799439014'),
            'payment_status': 'successful'
        }
        self.mock_orders.find_one_and_update.return_value = mock_order

        mock_send_email.return_value = {"error": "Failed to send email"}

        with self.app.test_request_context(
            json={
                'payment_intent_id': 'pi_12345',
                'payment_method_id': 'pm_12345'
            }
        ):
            response = confirm_payment_func(self.mock_orders)

        response_body, status_code = response
        response_data = json.loads(response_body.get_data(as_text=True))

        self.assertEqual(status_code, 500)
        self.assertEqual(response_data['error'], 'Failed to send email')



    @patch("app.routes.payment.stripe.PaymentIntent.confirm")
    def test_confirm_payment_failed_status(self, mock_stripe_confirm):
        mock_stripe_confirm.return_value = MagicMock(status='failed')

        with self.app.test_request_context(
            json={
                'payment_intent_id': 'pi_12345',
                'payment_method_id': 'pm_12345'
            }
        ):
            response = confirm_payment_func(self.mock_orders)

        response_body, status_code = response
        response_data = json.loads(response_body.get_data(as_text=True))

        self.assertEqual(status_code, 400)
        self.assertEqual(response_data['error'], 'Payment failed')



    @patch("app.routes.payment.stripe.PaymentIntent.confirm")
    def test_confirm_payment_exception(self, mock_stripe_confirm):
        mock_stripe_confirm.side_effect = Exception("Unexpected error")

        with self.app.test_request_context(
            json={
                'payment_intent_id': 'pi_12345',
                'payment_method_id': 'pm_12345'
            }
        ):
            response = confirm_payment_func(self.mock_orders)

        response_body, status_code = response
        response_data = json.loads(response_body.get_data(as_text=True))

        self.assertEqual(status_code, 500)
        self.assertEqual(response_data['error'], 'Unexpected error')

