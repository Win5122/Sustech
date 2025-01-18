import grpc

from DB_Service_pb2 import (UsersInsertRequest, UsersDeleteRequest, UsersSelectRequest, UsersUpdateRequest,
                            ProductsInsertRequest, ProductsDeleteRequest, ProductsSelectRequest, ProductsUpdateRequest,
                            OrdersInsertRequest, OrdersDeleteRequest, OrdersSelectRequest, OrdersUpdateRequest)
from DB_Service_pb2_grpc import DBServiceStub


def run_test_user():
    with grpc.insecure_channel('localhost:8082') as channel:
        stub = DBServiceStub(channel)
        # Select
        print('> User Select')
        UsersSelectRes = stub.UsersSelect(UsersSelectRequest())
        print(f'> Client received:\n{UsersSelectRes}')
        # Insert
        print('> User Insert')
        UsersInsertRes = stub.UsersInsert(
            UsersInsertRequest(sid="121100", username="qyz3", password_hash="123456", email="121100"))
        print(f'> Client received:\n{UsersInsertRes}')
        # Select again
        print('> User Select')
        UsersSelectRes = stub.UsersSelect(UsersSelectRequest())
        print(f'> Client received:\n{UsersSelectRes}')
        # Update
        print('> User Update')
        UsersUpdateRes = stub.UsersUpdate(UsersUpdateRequest(id=UsersInsertRes.user.id, username="wqy2"))
        print(f'> Client received:\n{UsersUpdateRes}')
        # Select again
        print('> User Select')
        UsersSelectRes = stub.UsersSelect(UsersSelectRequest())
        print(f'> Client received:\n{UsersSelectRes}')
        # Delete
        print('> User Delete')
        UsersDeleteRes = stub.UsersDelete(UsersDeleteRequest(id=UsersInsertRes.user.id))
        print(f'> Client received:\n{UsersDeleteRes}')
        # Select again
        print('> User Select')
        UsersSelectRes = stub.UsersSelect(UsersSelectRequest())
        print(f'> Client received:\n{UsersSelectRes}')


def run_test_product():
    with grpc.insecure_channel('localhost:8082') as channel:
        stub = DBServiceStub(channel)
        # Select
        print('> Products Select')
        ProductsSelectRes = stub.ProductsSelect(ProductsSelectRequest())
        print(f'> Client received:\n{ProductsSelectRes}')
        # Insert
        print('> Product Insert')
        ProductsInsertRes = stub.ProductsInsert(
            ProductsInsertRequest(name="111", description="hhh", category="sb", price=12, slogan="cnm", stock=10))
        print(f'> Client received:\n{ProductsInsertRes}')
        # Select again
        print('> Product Select')
        ProductsSelectRes = stub.ProductsSelect(ProductsSelectRequest())
        print(f'> Client received:\n{ProductsSelectRes}')
        # Update
        print('> Product Update')
        ProductsUpdateRes = stub.ProductsUpdate(ProductsUpdateRequest(id=4, description="nb"))
        print(f'> Client received:\n{ProductsUpdateRes}')
        # Select again
        print('> Product Select')
        ProductsSelectRes = stub.ProductsSelect(ProductsSelectRequest())
        print(f'> Client received:\n{ProductsSelectRes}')
        # Delete
        print('> Product Delete')
        ProductsDeleteRes = stub.ProductsDelete(ProductsDeleteRequest(id=5))
        print(f'> Client received:\n{ProductsDeleteRes}')
        # Select again
        print('> Product Select')
        ProductsSelectRes = stub.ProductsSelect(ProductsSelectRequest())
        print(f'> Client received:\n{ProductsSelectRes}')


def run_test_order():
    with grpc.insecure_channel('localhost:8082') as channel:
        stub = DBServiceStub(channel)
        # Select
        print('> Order Select')
        OrdersSelectRes = stub.OrdersSelect(OrdersSelectRequest())
        print(f'> Client received:\n{OrdersSelectRes}')
        # Insert
        print('> Order Insert')
        OrdersInsertRes = stub.OrdersInsert(
            OrdersInsertRequest(user_id=8, product_id=1, quantity=2, total_price=99.9))
        print(f'> Client received:\n{OrdersInsertRes}')
        # Select again
        print('> Order Select')
        OrdersSelectRes = stub.OrdersSelect(OrdersSelectRequest())
        print(f'> Client received:\n{OrdersSelectRes}')
        # Update
        print('> Order Update')
        OrdersUpdateRes = stub.OrdersUpdate(
            OrdersUpdateRequest(id=OrdersInsertRes.order.id, user_id=8, product_id=1, quantity=1))
        print(f'> Client received:\n{OrdersUpdateRes}')
        # Select again
        print('> Order Select')
        OrdersSelectRes = stub.OrdersSelect(OrdersSelectRequest())
        print(f'> Client received:\n{OrdersSelectRes}')
        # Delete
        print('> Order Delete')
        OrdersDeleteRes = stub.OrdersDelete(OrdersDeleteRequest(id=OrdersInsertRes.order.id))
        print(f'> Client received:\n{OrdersDeleteRes}')
        # Select again
        print('> Order Select')
        OrdersSelectRes = stub.OrdersSelect(OrdersSelectRequest())
        print(f'> Client received:\n{OrdersSelectRes}')


if __name__ == '__main__':
    run_test_user()
    run_test_product()
    run_test_order()
