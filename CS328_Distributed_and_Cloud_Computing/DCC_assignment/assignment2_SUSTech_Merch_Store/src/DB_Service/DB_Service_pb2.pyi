from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("id", "sid", "username", "password_hash", "email", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    SID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_HASH_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    sid: str
    username: str
    password_hash: str
    email: str
    created_at: str
    def __init__(self, id: _Optional[int] = ..., sid: _Optional[str] = ..., username: _Optional[str] = ..., password_hash: _Optional[str] = ..., email: _Optional[str] = ..., created_at: _Optional[str] = ...) -> None: ...

class UsersInsertRequest(_message.Message):
    __slots__ = ("sid", "username", "email", "password_hash")
    SID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_HASH_FIELD_NUMBER: _ClassVar[int]
    sid: str
    username: str
    email: str
    password_hash: str
    def __init__(self, sid: _Optional[str] = ..., username: _Optional[str] = ..., email: _Optional[str] = ..., password_hash: _Optional[str] = ...) -> None: ...

class UsersInsertResponse(_message.Message):
    __slots__ = ("message", "user")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    message: str
    user: User
    def __init__(self, message: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class UsersDeleteRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class UsersDeleteResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class UsersSelectRequest(_message.Message):
    __slots__ = ("id", "sid", "username", "email", "password_hash", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    SID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_HASH_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    sid: str
    username: str
    email: str
    password_hash: str
    created_at: str
    def __init__(self, id: _Optional[int] = ..., sid: _Optional[str] = ..., username: _Optional[str] = ..., email: _Optional[str] = ..., password_hash: _Optional[str] = ..., created_at: _Optional[str] = ...) -> None: ...

class UsersSelectResponse(_message.Message):
    __slots__ = ("message", "matched_users")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    MATCHED_USERS_FIELD_NUMBER: _ClassVar[int]
    message: str
    matched_users: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(self, message: _Optional[str] = ..., matched_users: _Optional[_Iterable[_Union[User, _Mapping]]] = ...) -> None: ...

class UsersUpdateRequest(_message.Message):
    __slots__ = ("id", "sid", "username", "password_hash", "email", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    SID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_HASH_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    sid: str
    username: str
    password_hash: str
    email: str
    created_at: str
    def __init__(self, id: _Optional[int] = ..., sid: _Optional[str] = ..., username: _Optional[str] = ..., password_hash: _Optional[str] = ..., email: _Optional[str] = ..., created_at: _Optional[str] = ...) -> None: ...

class UsersUpdateResponse(_message.Message):
    __slots__ = ("message", "user")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    message: str
    user: User
    def __init__(self, message: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class Product(_message.Message):
    __slots__ = ("id", "name", "description", "category", "price", "slogan", "stock", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    SLOGAN_FIELD_NUMBER: _ClassVar[int]
    STOCK_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    description: str
    category: str
    price: float
    slogan: str
    stock: int
    created_at: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., category: _Optional[str] = ..., price: _Optional[float] = ..., slogan: _Optional[str] = ..., stock: _Optional[int] = ..., created_at: _Optional[str] = ...) -> None: ...

class ProductsInsertRequest(_message.Message):
    __slots__ = ("name", "description", "category", "price", "slogan", "stock")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    SLOGAN_FIELD_NUMBER: _ClassVar[int]
    STOCK_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    category: str
    price: float
    slogan: str
    stock: int
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., category: _Optional[str] = ..., price: _Optional[float] = ..., slogan: _Optional[str] = ..., stock: _Optional[int] = ...) -> None: ...

class ProductsInsertResponse(_message.Message):
    __slots__ = ("message", "product")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_FIELD_NUMBER: _ClassVar[int]
    message: str
    product: Product
    def __init__(self, message: _Optional[str] = ..., product: _Optional[_Union[Product, _Mapping]] = ...) -> None: ...

class ProductsDeleteRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class ProductsDeleteResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class ProductsSelectRequest(_message.Message):
    __slots__ = ("id", "name", "description", "category", "price", "slogan", "stock", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    SLOGAN_FIELD_NUMBER: _ClassVar[int]
    STOCK_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    description: str
    category: str
    price: float
    slogan: str
    stock: int
    created_at: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., category: _Optional[str] = ..., price: _Optional[float] = ..., slogan: _Optional[str] = ..., stock: _Optional[int] = ..., created_at: _Optional[str] = ...) -> None: ...

class ProductsSelectResponse(_message.Message):
    __slots__ = ("message", "matched_products")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    MATCHED_PRODUCTS_FIELD_NUMBER: _ClassVar[int]
    message: str
    matched_products: _containers.RepeatedCompositeFieldContainer[Product]
    def __init__(self, message: _Optional[str] = ..., matched_products: _Optional[_Iterable[_Union[Product, _Mapping]]] = ...) -> None: ...

class ProductsUpdateRequest(_message.Message):
    __slots__ = ("id", "name", "description", "category", "price", "slogan", "stock", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    SLOGAN_FIELD_NUMBER: _ClassVar[int]
    STOCK_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    description: str
    category: str
    price: float
    slogan: str
    stock: int
    created_at: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., category: _Optional[str] = ..., price: _Optional[float] = ..., slogan: _Optional[str] = ..., stock: _Optional[int] = ..., created_at: _Optional[str] = ...) -> None: ...

class ProductsUpdateResponse(_message.Message):
    __slots__ = ("message", "id")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    message: str
    id: int
    def __init__(self, message: _Optional[str] = ..., id: _Optional[int] = ...) -> None: ...

class Order(_message.Message):
    __slots__ = ("id", "user_id", "product_id", "quantity", "total_price", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PRICE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    created_at: str
    def __init__(self, id: _Optional[int] = ..., user_id: _Optional[int] = ..., product_id: _Optional[int] = ..., quantity: _Optional[int] = ..., total_price: _Optional[float] = ..., created_at: _Optional[str] = ...) -> None: ...

class OrdersInsertRequest(_message.Message):
    __slots__ = ("user_id", "product_id", "quantity", "total_price")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PRICE_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    def __init__(self, user_id: _Optional[int] = ..., product_id: _Optional[int] = ..., quantity: _Optional[int] = ..., total_price: _Optional[float] = ...) -> None: ...

class OrdersInsertResponse(_message.Message):
    __slots__ = ("message", "order")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    message: str
    order: Order
    def __init__(self, message: _Optional[str] = ..., order: _Optional[_Union[Order, _Mapping]] = ...) -> None: ...

class OrdersDeleteRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class OrdersDeleteResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class OrdersSelectRequest(_message.Message):
    __slots__ = ("id", "user_id", "product_id", "quantity", "total_price", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PRICE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    created_at: str
    def __init__(self, id: _Optional[int] = ..., user_id: _Optional[int] = ..., product_id: _Optional[int] = ..., quantity: _Optional[int] = ..., total_price: _Optional[float] = ..., created_at: _Optional[str] = ...) -> None: ...

class OrdersSelectResponse(_message.Message):
    __slots__ = ("message", "matched_orders")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    MATCHED_ORDERS_FIELD_NUMBER: _ClassVar[int]
    message: str
    matched_orders: _containers.RepeatedCompositeFieldContainer[Order]
    def __init__(self, message: _Optional[str] = ..., matched_orders: _Optional[_Iterable[_Union[Order, _Mapping]]] = ...) -> None: ...

class OrdersUpdateRequest(_message.Message):
    __slots__ = ("id", "user_id", "product_id", "quantity", "total_price", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PRICE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    created_at: str
    def __init__(self, id: _Optional[int] = ..., user_id: _Optional[int] = ..., product_id: _Optional[int] = ..., quantity: _Optional[int] = ..., total_price: _Optional[float] = ..., created_at: _Optional[str] = ...) -> None: ...

class OrdersUpdateResponse(_message.Message):
    __slots__ = ("message", "order")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    message: str
    order: Order
    def __init__(self, message: _Optional[str] = ..., order: _Optional[_Union[Order, _Mapping]] = ...) -> None: ...
