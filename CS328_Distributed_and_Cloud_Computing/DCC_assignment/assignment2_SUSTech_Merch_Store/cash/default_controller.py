import os.path
import sys
import time

import connexion
from openapi_server.controllers.security_controller import generate_token
from openapi_server.models.cancel_order_response import CancelOrderResponse  # noqa: E501
from openapi_server.models.deactivate_user_response import DeactivateUserResponse  # noqa: E501
from openapi_server.models.get_order_error import GetOrderError  # noqa: E501
from openapi_server.models.get_order_request import GetOrderRequest  # noqa: E501
from openapi_server.models.get_product_response import GetProductResponse  # noqa: E501
from openapi_server.models.get_user_request import GetUserRequest  # noqa: E501
from openapi_server.models.get_user_response import GetUserResponse  # noqa: E501
from openapi_server.models.invalid_credentials import InvalidCredentials  # noqa: E501
from openapi_server.models.invalid_id import InvalidID  # noqa: E501
from openapi_server.models.login_request import LoginRequest  # noqa: E501
from openapi_server.models.place_order_error import PlaceOrderError  # noqa: E501
from openapi_server.models.place_order_request import PlaceOrderRequest  # noqa: E501
from openapi_server.models.place_order_response import PlaceOrderResponse  # noqa: E501
from openapi_server.models.update_error import UpdateError  # noqa: E501
from openapi_server.models.update_user_request import UpdateUserRequest  # noqa: E501
from werkzeug.security import generate_password_hash, check_password_hash

DB_Service_path = os.path.abspath("../../DB_Service")
Logging_Service_path = os.path.abspath("../../Logging_Service")
sys.path.append(DB_Service_path)
sys.path.append(Logging_Service_path)

import grpc
from DB_Service_pb2 import (UsersInsertRequest, UsersSelectRequest, UsersUpdateRequest,
                            ProductsSelectRequest, OrdersInsertRequest, OrdersDeleteRequest, OrdersSelectRequest)
from DB_Service_pb2_grpc import DBServiceStub
from Logging_Service_pb2 import (LoggingRequest)
from Logging_Service_pb2_grpc import LoggingServiceStub

deactivated_userID = []


def send_log_message(string):
    with grpc.insecure_channel('localhost:50051') as channel:
        service = LoggingServiceStub(channel)
        message = LoggingRequest(message=string, timestamp=str(time.time()))
        print(message)

        def generate_logs():
            yield message

        try:
            print("start send log message")
            response = service.LoggingService(generate_logs())
            print(response)
        except Exception as e:
            print(e)


def root_get():  # noqa: E501
    """Get a greeting

     # noqa: E501


    :rtype: Union[GreetingData, Tuple[GreetingData, int], Tuple[GreetingData, int, Dict[str, str]]
    """
    send_log_message('root greeting with GET method')
    return 'Hello, welcome to the goods store!'


def list_products_get():  # noqa: E501
    """Get a list of products

     # noqa: E501


    :rtype: Union[List[GetProductResponse], Tuple[List[GetProductResponse], int], Tuple[List[GetProductResponse], int, Dict[str, str]]
    """
    send_log_message('list products with GET method')
    with grpc.insecure_channel('localhost:8082') as channel:
        service = DBServiceStub(channel)
        productsList = service.ProductsSelect(ProductsSelectRequest()).matched_products
        return [GetProductResponse(id=product.id,
                                   name=product.name,
                                   description=product.description,
                                   category=product.category,
                                   price=product.price,
                                   slogan=product.slogan,
                                   stock=product.stock,
                                   created_at=product.created_at,
                                   ) for product in productsList]


def get_product_get():  # noqa: E501
    """Get a product by ID

     # noqa: E501

    :param id: The ID of the product
    :type id: int

    :rtype: Union[GetProductResponse, Tuple[GetProductResponse, int], Tuple[GetProductResponse, int, Dict[str, str]]
    """
    send_log_message('get product with GET method')
    productID = connexion.request.args.get('id')
    with grpc.insecure_channel('localhost:8082') as channel:
        service = DBServiceStub(channel)
        productsList = service.ProductsSelect(ProductsSelectRequest()).matched_products
        products = [GetProductResponse(id=product.id,
                                       name=product.name,
                                       description=product.description,
                                       category=product.category,
                                       price=product.price,
                                       slogan=product.slogan,
                                       stock=product.stock,
                                       created_at=product.created_at,
                                       ) for product in productsList if str(product.id) == str(productID)]
        if len(products) > 0:
            return products[0]
        else:
            return InvalidID(message="Invalid ID"), 400


def register_post(body):  # noqa: E501
    """Register a new user

     # noqa: E501

    :param register_request:
    :type register_request: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    send_log_message('register with POST method')
    register_request = body
    if connexion.request.is_json:
        register_request = UpdateUserRequest.from_dict(connexion.request.get_json())  # noqa: E501
    with grpc.insecure_channel('localhost:8082') as channel:
        service = DBServiceStub(channel)
        if register_request.email is not None:
            email = register_request.email
        else:
            email = register_request.sid + "@mail.sustech.edu.cn"
        result = service.UsersInsert(UsersInsertRequest(
            sid=register_request.sid,
            username=register_request.username,
            password_hash=generate_password_hash(register_request.password),
            email=email,
        ))
        if result.message != 'UsersInsert OK':
            return result.message, 400
        else:
            user = result.user
            return GetUserResponse(
                id=user.id,
                sid=user.sid,
                username=user.username,
                password=user.password_hash,
                email=user.email,
                created_at=user.created_at,
            ), 201


def deactivate_user_get():  # noqa: E501
    """Deactivate a user

     # noqa: E501

    :param id: The ID of the user
    :type id: int

    :rtype: Union[DeactivateUserResponse, Tuple[DeactivateUserResponse, int], Tuple[DeactivateUserResponse, int, Dict[str, str]]
    """
    send_log_message('deactivate user with GET method')
    userID = int(connexion.request.args.get('id'))
    with grpc.insecure_channel('localhost:8082') as channel:
        service = DBServiceStub(channel)
        userList = service.UsersSelect(UsersSelectRequest()).matched_users
        user = [user for user in userList if user.id == userID]
        if len(user) <= 0:
            return InvalidID(message='User not found'), 400
        user = user[0]
        user_name = connexion.context['token_info']['user_name']
        if user_name != user.username or user.id in deactivated_userID:
            return UpdateError("Error: You are not this user"), 401
        deactivated_userID.append(user.id)
        return DeactivateUserResponse("log out successful")


def get_user_post(body):  # noqa: E501
    """Get a user by username and password

     # noqa: E501

    :param get_user_request:
    :type get_user_request: dict | bytes

    :rtype: Union[GetUserResponse, Tuple[GetUserResponse, int], Tuple[GetUserResponse, int, Dict[str, str]]
    """
    send_log_message('get user with POST method')
    get_user_request = body
    if connexion.request.is_json:
        get_user_request = GetUserRequest.from_dict(connexion.request.get_json())  # noqa: E501
    with grpc.insecure_channel('localhost:8082') as channel:
        service = DBServiceStub(channel)
        usersList = service.UsersSelect(UsersSelectRequest()).matched_users
        users = [user for user in usersList if user.username == get_user_request.username]
        if len(users) <= 0:
            return InvalidCredentials(message='User not found'), 400
        for user in users:
            if check_password_hash(user.password_hash, get_user_request.password):
                return GetUserResponse(
                    id=user.id,
                    sid=user.sid,
                    username=user.username,
                    password=user.password_hash,
                    email=user.email,
                    created_at=user.created_at,
                )
            else:
                return InvalidCredentials(message='Invalid password'), 400


def update_user_post(body):  # noqa: E501
    """Update a user

     # noqa: E501

    :param update_user_request:
    :type update_user_request: dict | bytes

    :rtype: Union[GetUserResponse, Tuple[GetUserResponse, int], Tuple[GetUserResponse, int, Dict[str, str]]
    """
    send_log_message('update user with POST method')
    update_user_request = body
    if connexion.request.is_json:
        update_user_request = UpdateUserRequest.from_dict(connexion.request.get_json())  # noqa: E501
    with grpc.insecure_channel('localhost:8082') as channel:
        service = DBServiceStub(channel)
        usersList = service.UsersSelect(UsersSelectRequest()).matched_users
        user = [user for user in usersList if user.id == update_user_request.id]
        if len(user) <= 0:
            return UpdateError("Error: User not found"), 400
        else:
            user = user[0]
            user_name = connexion.context['token_info']['user_name']
            if user_name != user.username or user.id in deactivated_userID:
                return UpdateError("Error: You are not this user"), 401
            message = service.UsersUpdate(UsersUpdateRequest(
                id=user.id,
                sid=user.sid if update_user_request.sid is None else update_user_request.sid,
                username=user.username if update_user_request.username is None else update_user_request.username,
                password_hash=user.password_hash if update_user_request.password is None else generate_password_hash(
                    update_user_request.password),
                email=user.email if update_user_request.email is None else update_user_request.email,
                created_at=user.created_at,
            )).message
            if message == 'User updated':
                return UpdateUserRequest(message)
            else:
                return UpdateError(message), 400


def login_post(body):  # noqa: E501
    """Authenticate and get a JWT token

     # noqa: E501

    :param login_request:
    :type login_request: dict | bytes

    :rtype: Union[LoginResponse, Tuple[LoginResponse, int], Tuple[LoginResponse, int, Dict[str, str]]
    """
    send_log_message('login with POST method')
    login_request = body
    if connexion.request.is_json:
        login_request = LoginRequest.from_dict(connexion.request.get_json())  # noqa: E501
    with grpc.insecure_channel('localhost:8082') as channel:
        service = DBServiceStub(channel)
        userList = service.UsersSelect(UsersSelectRequest()).matched_users
        user = [user for user in userList if user.username == login_request.username]
        if len(user) <= 0:
            return {'message': f'User {login_request.username} does not exist.'}, 404
        user = user[0]
        if check_password_hash(user.password_hash, login_request.password):
            if user.id in deactivated_userID:
                deactivated_userID.remove(user.id)
            token = generate_token(user_name=login_request.username)
            return {'token': token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401


def place_order_post(body):  # noqa: E501
    """Add an order

     # noqa: E501

    :param place_order_request:
    :type place_order_request: dict | bytes

    :rtype: Union[PlaceOrderResponse, Tuple[PlaceOrderResponse, int], Tuple[PlaceOrderResponse, int, Dict[str, str]]
    """
    send_log_message('place order with POST method')
    place_order_request = body
    if connexion.request.is_json:
        place_order_request = PlaceOrderRequest.from_dict(connexion.request.get_json())  # noqa: E501
    with grpc.insecure_channel('localhost:8082') as channel:
        service = DBServiceStub(channel)
        usersList = service.UsersSelect(UsersSelectRequest()).matched_users
        user = [user for user in usersList if user.id == place_order_request.user_id]
        if len(user) <= 0:
            return PlaceOrderError("Error: User not found"), 400
        user = user[0]
        user_name = connexion.context['token_info']['user_name']
        if user_name != user.username or user.id in deactivated_userID:
            return PlaceOrderError("Error: You are not this user"), 401
        productsList = service.ProductsSelect(ProductsSelectRequest()).matched_products
        product = [product for product in productsList if product.id == place_order_request.product_id]
        if len(product) <= 0:
            return PlaceOrderError("Error: Product not found"), 400
        product = product[0]
        result = service.OrdersInsert(OrdersInsertRequest(
            user_id=place_order_request.user_id,
            product_id=place_order_request.product_id,
            quantity=place_order_request.quantity,
            total_price=place_order_request.quantity * product.price,
        ))
        if result.message == "OrdersInsert OK":
            order = result.order
            return PlaceOrderResponse(
                id=order.id,
                user_id=order.user_id,
                product_id=order.product_id,
                quantity=order.quantity,
                total_price=order.total_price,
                created_at=order.created_at,
            )
        else:
            return PlaceOrderError(result.message)


def cancel_order_get():  # noqa: E501
    """Cancel an order

     # noqa: E501

    :param id: The ID of the order
    :type id: int

    :rtype: Union[CancelOrderResponse, Tuple[CancelOrderResponse, int], Tuple[CancelOrderResponse, int, Dict[str, str]]
    """
    send_log_message('cancel order with GET method')
    orderID = int(connexion.request.args.get('id'))
    with grpc.insecure_channel('localhost:8082') as channel:
        service = DBServiceStub(channel)
        ordersList = service.OrdersSelect(OrdersSelectRequest()).matched_orders
        order = [order for order in ordersList if order.id == orderID]
        if len(order) <= 0:
            return InvalidID("Error: Order not found"), 400
        userList = service.UsersSelect(UsersSelectRequest()).matched_users
        user = [user for user in userList if user.id == order[0].user_id][0]
        user_name = connexion.context['token_info']['user_name']
        if user_name != user.username or user.id in deactivated_userID:
            return InvalidID("Error: You are not this user"), 401
        result = service.OrdersDelete(OrdersDeleteRequest(id=orderID))
        return CancelOrderResponse(message=result.message)


def get_order_post(body):  # noqa: E501
    """Add an order

     # noqa: E501

    :param get_order_request:
    :type get_order_request: dict | bytes

    :rtype: Union[List[PlaceOrderResponse], Tuple[List[PlaceOrderResponse], int], Tuple[List[PlaceOrderResponse], int, Dict[str, str]]
    """
    send_log_message('get order with POST method')
    get_order_request = body
    if connexion.request.is_json:
        get_order_request = GetOrderRequest.from_dict(connexion.request.get_json())  # noqa: E501
    with grpc.insecure_channel('localhost:8082') as channel:
        service = DBServiceStub(channel)
        userList = service.UsersSelect(UsersSelectRequest()).matched_users
        user = [user for user in userList if user.id == get_order_request.user_id]
        if len(user) <= 0:
            return InvalidID("Error: User not found"), 400
        user = user[0]
        user_name = connexion.context['token_info']['user_name']
        if user_name != user.username or user.id in deactivated_userID:
            return InvalidID("Error: You are not this user"), 401
        ordersList = service.OrdersSelect(OrdersSelectRequest()).matched_orders
        orders = [order for order in ordersList if order.user_id == get_order_request.user_id]
        if get_order_request.product_id is not None:
            orders = [order for order in orders if order.product_id == get_order_request.product_id]
        if len(orders) <= 0:
            return GetOrderError("Error: Orders not found"), 400
        else:
            return [PlaceOrderResponse(id=order.id,
                                       user_id=order.user_id,
                                       product_id=order.product_id,
                                       quantity=order.quantity,
                                       total_price=order.total_price,
                                       created_at=order.created_at,
                                       ) for order in orders]


def protected_get():  # noqa: E501
    """Access protected data

     # noqa: E501


    :rtype: Union[ProtectedData, Tuple[ProtectedData, int], Tuple[ProtectedData, int, Dict[str, str]]
    """
    send_log_message('protected with GET method')
    user_name = connexion.context['token_info']['user_name']
    return {'message': f'Congratulations! Authentication passed! You are {user_name}.'}, 200
