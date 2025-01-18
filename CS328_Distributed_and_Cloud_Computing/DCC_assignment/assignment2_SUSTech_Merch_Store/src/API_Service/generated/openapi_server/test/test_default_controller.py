import unittest

from flask import json

from openapi_server.models.cancel_order_response import CancelOrderResponse  # noqa: E501
from openapi_server.models.deactivate_user_response import DeactivateUserResponse  # noqa: E501
from openapi_server.models.get_order_error import GetOrderError  # noqa: E501
from openapi_server.models.get_order_request import GetOrderRequest  # noqa: E501
from openapi_server.models.get_product_response import GetProductResponse  # noqa: E501
from openapi_server.models.get_user_request import GetUserRequest  # noqa: E501
from openapi_server.models.get_user_response import GetUserResponse  # noqa: E501
from openapi_server.models.greeting_data import GreetingData  # noqa: E501
from openapi_server.models.invalid_credentials import InvalidCredentials  # noqa: E501
from openapi_server.models.invalid_id import InvalidID  # noqa: E501
from openapi_server.models.login_request import LoginRequest  # noqa: E501
from openapi_server.models.login_response import LoginResponse  # noqa: E501
from openapi_server.models.place_order_error import PlaceOrderError  # noqa: E501
from openapi_server.models.place_order_request import PlaceOrderRequest  # noqa: E501
from openapi_server.models.place_order_response import PlaceOrderResponse  # noqa: E501
from openapi_server.models.protected_data import ProtectedData  # noqa: E501
from openapi_server.models.register_request import RegisterRequest  # noqa: E501
from openapi_server.models.update_error import UpdateError  # noqa: E501
from openapi_server.models.update_user_request import UpdateUserRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_cancel_order_get(self):
        """Test case for cancel_order_get

        Cancel an order
        """
        query_string = [('id', 1)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/cancelOrder',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_deactivate_user_get(self):
        """Test case for deactivate_user_get

        Deactivate a user
        """
        query_string = [('id', 1)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/deactivateUser',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_order_post(self):
        """Test case for get_order_post

        Add an order
        """
        get_order_request = {"user_id":6,"product_id":1,"id":0}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/getOrder',
            method='POST',
            headers=headers,
            data=json.dumps(get_order_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_product_get(self):
        """Test case for get_product_get

        Get a product by ID
        """
        query_string = [('id', 1)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/getProduct',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_user_post(self):
        """Test case for get_user_post

        Get a user by username and password
        """
        get_user_request = {"password":"password","username":"username"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/getUser',
            method='POST',
            headers=headers,
            data=json.dumps(get_user_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_products_get(self):
        """Test case for list_products_get

        Get a list of products
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/listProducts',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_post(self):
        """Test case for login_post

        Authenticate and get a JWT token
        """
        login_request = {"password":"password","username":"username"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/login',
            method='POST',
            headers=headers,
            data=json.dumps(login_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_place_order_post(self):
        """Test case for place_order_post

        Add an order
        """
        place_order_request = {"quantity":1,"total_price":5.962133916683182,"user_id":0,"product_id":6}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/placeOrder',
            method='POST',
            headers=headers,
            data=json.dumps(place_order_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_protected_get(self):
        """Test case for protected_get

        Access protected data
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/protected',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_register_post(self):
        """Test case for register_post

        Register a new user
        """
        register_request = {"password":"password","email":"email","sid":"sid","username":"username"}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/register',
            method='POST',
            headers=headers,
            data=json.dumps(register_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_root_get(self):
        """Test case for root_get

        Get a greeting
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_user_post(self):
        """Test case for update_user_post

        Update a user
        """
        update_user_request = {"password":"password","created_at":"created_at","id":0,"email":"email","sid":"sid","username":"username"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/updateUser',
            method='POST',
            headers=headers,
            data=json.dumps(update_user_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
