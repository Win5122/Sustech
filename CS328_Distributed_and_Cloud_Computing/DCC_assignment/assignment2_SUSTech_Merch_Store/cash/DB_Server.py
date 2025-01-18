import logging
from concurrent import futures
from pprint import pprint

import grpc
import psycopg2
from psycopg2 import pool

from DB_Service_pb2 import (User, Product, Order,
                            UsersInsertRequest, UsersInsertResponse,
                            UsersDeleteRequest, UsersDeleteResponse,
                            UsersSelectRequest, UsersSelectResponse,
                            UsersUpdateRequest, UsersUpdateResponse,
                            ProductsInsertRequest, ProductsInsertResponse,
                            ProductsDeleteRequest, ProductsDeleteResponse,
                            ProductsSelectRequest, ProductsSelectResponse,
                            ProductsUpdateRequest, ProductsUpdateResponse,
                            OrdersInsertRequest, OrdersInsertResponse,
                            OrdersDeleteRequest, OrdersDeleteResponse,
                            OrdersSelectRequest, OrdersSelectResponse,
                            OrdersUpdateRequest, OrdersUpdateResponse)
from DB_Service_pb2_grpc import DBServiceServicer, add_DBServiceServicer_to_server

simple_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    user="postgres",
    # maybe password need to be read from environment variable for security issue
    password="wqy5122",
    host="localhost",
    port="5432",
    database="dcc_assignment2"
)


class DBService(DBServiceServicer):
    def UsersInsert(self, request: UsersInsertRequest, context):
        pprint('> UsersInsert')
        try:
            conn = simple_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (sid, username, password_hash, email) VALUES (%s, %s, %s, %s) RETURNING id, sid, username, password_hash, email, created_at",
                (request.sid, request.username, request.password_hash, request.email))
            results = cursor.fetchall()
            conn.commit()
            pprint(results)
            return UsersInsertResponse(message='UsersInsert OK', user=User(
                id=results[0][0],
                sid=results[0][1],
                username=results[0][2],
                password_hash=results[0][3],
                email=results[0][4],
                created_at=results[0][5].isoformat()
            ))
        except Exception as e:
            pprint(e)
            logging.error(e)
            return UsersInsertResponse(message=f"Error during UsersInsert.\n {e}", user=None)
        finally:
            simple_pool.putconn(conn)

    def UsersDelete(self, request: UsersDeleteRequest, context):
        pprint('> UsersDelete')
        try:
            conn = simple_pool.getconn()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = %s", (request.id,))
            conn.commit()
            return UsersDeleteResponse(message='UsersDelete OK')
        except Exception as e:
            pprint(e)
            logging.error(e)
            return UsersDeleteResponse(message=f"Error during UsersDelete.\n {e}")
        finally:
            simple_pool.putconn(conn)

    def UsersSelect(self, request: UsersSelectRequest, context):
        pprint('> UsersSelect')
        try:
            conn = simple_pool.getconn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, sid, username, password_hash, email, created_at FROM users")
            results = cursor.fetchall()
            pprint(results)
            return UsersSelectResponse(message='UsersSelect OK',
                                       matched_users=[
                                           User(
                                               id=row[0],
                                               sid=row[1],
                                               username=row[2],
                                               password_hash=row[3],
                                               email=row[4],
                                               created_at=row[5].isoformat()  # Convert datetime to string if needed
                                           )
                                           for row in results
                                       ])
        except Exception as e:
            pprint(e)
            logging.error(e)
            return UsersSelectResponse(message=f"Error during UsersSelect.\n {e}")
        finally:
            simple_pool.putconn(conn)

    def UsersUpdate(self, request: UsersUpdateRequest, context):
        pprint('> UsersUpdate')
        try:
            conn = simple_pool.getconn()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET sid = %s, username = %s, password_hash = %s, email = %s WHERE id = %s",
                           (request.sid, request.username, request.password_hash, request.email, request.id))
            conn.commit()
            return UsersUpdateResponse(message='User updated')
        except Exception as e:
            pprint(e)
            logging.error(e)
            return UsersUpdateResponse(message=f"Error during UsersUpdate.\n {e}")
        finally:
            simple_pool.putconn(conn)

    def ProductsInsert(self, request: ProductsInsertRequest, context):
        pprint('> ProductsInsert')
        try:
            conn = simple_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (name, description, category, price, slogan, stock) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id, name, description, category, price, slogan, stock, created_at",
                (request.name, request.description, request.category, request.price, request.slogan, request.stock))
            results = cursor.fetchall()
            conn.commit()
            pprint(results)
            return ProductsInsertResponse(message='ProductsInsert OK', product=Product(
                id=results[0][0],
                name=results[0][1],
                description=results[0][2],
                category=results[0][3],
                price=results[0][4],
                slogan=results[0][5],
                stock=results[0][6],
                created_at=results[0][7].isoformat()
            ))
        except Exception as e:
            pprint(e)
            logging.error(e)
            return ProductsInsertResponse(message=f"Error during ProductsInsert.\n {e}")
        finally:
            simple_pool.putconn(conn)

    def ProductsDelete(self, request: ProductsDeleteRequest, context):
        pprint('> ProductsDelete')
        try:
            conn = simple_pool.getconn()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = %s", (request.id,))
            conn.commit()
            return ProductsDeleteResponse(message='ProductsDelete OK')
        except Exception as e:
            pprint(e)
            logging.error(e)
            return ProductsDeleteResponse(message=f"Error during ProductsDelete.\n {e}")
        finally:
            simple_pool.putconn(conn)

    def ProductsSelect(self, request: ProductsSelectRequest, context):
        pprint('> ProductsSelect')
        try:
            conn = simple_pool.getconn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, description, category, price, slogan, stock, created_at FROM products")
            results = cursor.fetchall()
            pprint(results)
            return ProductsSelectResponse(message='ProductsSelect OK',
                                          matched_products=[
                                              Product(
                                                  id=row[0],
                                                  name=row[1],
                                                  description=row[2],
                                                  category=row[3],
                                                  price=row[4],
                                                  slogan=row[5],
                                                  stock=row[6],
                                                  created_at=row[7].isoformat()  # Convert datetime to string if needed
                                              )
                                              for row in results
                                          ])
        except Exception as e:
            pprint(e)
            logging.error(e)
            return ProductsSelectResponse(message=f"Error during ProductsSelect.\n {e}")
        finally:
            simple_pool.putconn(conn)

    def ProductsUpdate(self, request: ProductsUpdateRequest, context):
        pprint('> ProductsUpdate')
        try:
            conn = simple_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE products SET name = %s, description = %s, category = %s, price = %s, slogan = %s, stock = %s WHERE id = %s",
                (request.name, request.description, request.category, request.price, request.slogan, request.stock,
                 request.id))
            conn.commit()
            return ProductsUpdateResponse(message='Product updated')
        except Exception as e:
            pprint(e)
            logging.error(e)
            return ProductsUpdateResponse(message=f"Error during ProductsUpdate.\n {e}")
        finally:
            simple_pool.putconn(conn)

    def OrdersInsert(self, request: OrdersInsertRequest, context):
        pprint('> OrdersInsert')
        try:
            conn = simple_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO orders (user_id, product_id, quantity, total_price) VALUES (%s, %s, %s, %s) RETURNING id, user_id, product_id, quantity, total_price, created_at",
                (request.user_id, request.product_id, request.quantity, request.total_price))
            results = cursor.fetchall()
            conn.commit()
            pprint(results)
            return OrdersInsertResponse(message='OrdersInsert OK', order=Order(
                id=results[0][0],
                user_id=results[0][1],
                product_id=results[0][2],
                quantity=results[0][3],
                total_price=results[0][4],
                created_at=results[0][5].isoformat()
            ))
        except Exception as e:
            pprint(e)
            logging.error(e)
            return OrdersInsertResponse(message=f"Error during OrdersInsert.\n {e}")
        finally:
            simple_pool.putconn(conn)

    def OrdersDelete(self, request: OrdersDeleteRequest, context):
        pprint('> OrdersDelete')
        try:
            conn = simple_pool.getconn()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM orders WHERE id = %s", (request.id,))
            conn.commit()
            return OrdersDeleteResponse(message='OrdersDelete OK')
        except Exception as e:
            pprint(e)
            logging.error(e)
            return OrdersDeleteResponse(message=f"Error during OrdersDelete.\n {e}")
        finally:
            simple_pool.putconn(conn)

    def OrdersSelect(self, request: OrdersSelectRequest, context):
        pprint('> OrdersSelect')
        try:
            conn = simple_pool.getconn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_id, product_id, quantity, total_price, created_at FROM orders")
            results = cursor.fetchall()
            pprint(results)
            return OrdersSelectResponse(message='OrdersSelect OK',
                                        matched_orders=[
                                            Order(
                                                id=row[0],
                                                user_id=row[1],
                                                product_id=row[2],
                                                quantity=row[3],
                                                total_price=row[4],
                                                created_at=row[5].isoformat()  # Convert datetime to string if needed
                                            )
                                            for row in results
                                        ])
        except Exception as e:
            pprint(e)
            logging.error(e)
            return OrdersSelectResponse(message=f"Error during OrdersSelect.\n {e}")
        finally:
            simple_pool.putconn(conn)

    def OrdersUpdate(self, request: OrdersUpdateRequest, context):
        pprint('> OrdersUpdate')
        try:
            conn = simple_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE orders SET user_id = %s, product_id = %s, quantity = %s, total_price = %s WHERE id = %s",
                (request.user_id, request.product_id, request.quantity, request.total_price, request.id))
            conn.commit()
            return OrdersUpdateResponse(message='Order updated')
        except Exception as e:
            pprint(e)
            logging.error(e)
            return OrdersUpdateResponse(message=f"Error during OrdersUpdate.\n {e}")
        finally:
            simple_pool.putconn(conn)


def serve():
    port = '8082'
    # the server can handle 10 client requests concurrently
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_DBServiceServicer_to_server(DBService(), server)
    # [::] specifies the listen on all ipv4/ipv6 addresses
    server.add_insecure_port('[::]:' + port)
    server.start()
    logging.info(f'Server started, listening on {port}')
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
    simple_pool.closeall()
