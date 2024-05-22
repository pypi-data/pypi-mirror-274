from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TokenUsage(_message.Message):
    __slots__ = ("token_input", "token_output")
    TOKEN_INPUT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    token_input: float
    token_output: float
    def __init__(self, token_input: _Optional[float] = ..., token_output: _Optional[float] = ...) -> None: ...

class QueryRequest(_message.Message):
    __slots__ = ("query",)
    QUERY_FIELD_NUMBER: _ClassVar[int]
    query: str
    def __init__(self, query: _Optional[str] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ("token_usage", "response", "sources")
    TOKEN_USAGE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    token_usage: TokenUsage
    response: str
    sources: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, token_usage: _Optional[_Union[TokenUsage, _Mapping]] = ..., response: _Optional[str] = ..., sources: _Optional[_Iterable[str]] = ...) -> None: ...
