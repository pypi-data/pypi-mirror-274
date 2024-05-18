from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleRequest(_message.Message):
    __slots__ = ("request", "msg_from", "msg_to")
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    MSG_FROM_FIELD_NUMBER: _ClassVar[int]
    MSG_TO_FIELD_NUMBER: _ClassVar[int]
    request: str
    msg_from: str
    msg_to: str
    def __init__(self, request: _Optional[str] = ..., msg_from: _Optional[str] = ..., msg_to: _Optional[str] = ...) -> None: ...

class ScheduleResponse(_message.Message):
    __slots__ = ("response", "msg_from", "msg_to")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    MSG_FROM_FIELD_NUMBER: _ClassVar[int]
    MSG_TO_FIELD_NUMBER: _ClassVar[int]
    response: str
    msg_from: str
    msg_to: str
    def __init__(self, response: _Optional[str] = ..., msg_from: _Optional[str] = ..., msg_to: _Optional[str] = ...) -> None: ...

class LLMTextResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: str
    def __init__(self, response: _Optional[str] = ...) -> None: ...

class ToolCallResult(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...
