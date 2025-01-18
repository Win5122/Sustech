from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GreetRequest(_message.Message):
    __slots__ = ("user_name", "institution")
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTITUTION_FIELD_NUMBER: _ClassVar[int]
    user_name: str
    institution: str
    def __init__(self, user_name: _Optional[str] = ..., institution: _Optional[str] = ...) -> None: ...

class GreetResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class MultRequest(_message.Message):
    __slots__ = ("xin", "yin")
    XIN_FIELD_NUMBER: _ClassVar[int]
    YIN_FIELD_NUMBER: _ClassVar[int]
    xin: float
    yin: float
    def __init__(self, xin: _Optional[float] = ..., yin: _Optional[float] = ...) -> None: ...

class MultResponse(_message.Message):
    __slots__ = ("xin", "yin", "result")
    XIN_FIELD_NUMBER: _ClassVar[int]
    YIN_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    xin: float
    yin: float
    result: float
    def __init__(self, xin: _Optional[float] = ..., yin: _Optional[float] = ..., result: _Optional[float] = ...) -> None: ...
