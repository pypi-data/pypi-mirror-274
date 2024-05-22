"""Common machineray for wrapping proto messages."""

from __future__ import annotations

import abc
import copy
from typing import Generic, TypeGuard, TypeVar

import google.protobuf.message

from corvic.op_graph.errors import OpParseError
from corvic_generated.orm.v1 import table_pb2

SomeMessage = TypeVar("SomeMessage", bound=google.protobuf.message.Message)


class ProtoWrapper(Generic[SomeMessage]):
    """Provides common operations for classes that wrap a proto message."""

    _proto: SomeMessage

    def __init__(self, proto: SomeMessage):
        self._proto = proto

    @staticmethod
    def _is_self_type(
        val: object,
    ) -> TypeGuard[ProtoWrapper[google.protobuf.message.Message]]:
        if isinstance(val, ProtoWrapper):
            return True
        return False

    def __eq__(self, other: object) -> bool:
        """Instances are equal if their underlying messages are equal.

        As a convenience, equality also applies if the target of comparison is a raw
        message.
        """
        if self._is_self_type(other):
            other = other._proto
        return self._proto == other  # pyright: ignore[reportUnknownVariableType]

    def to_proto(self) -> SomeMessage:
        # copy since a caller could modify this and wrappers are immutable
        return copy.copy(self._proto)

    def to_bytes(self):
        return self._proto.SerializeToString()


class ProtoOneofWrapper(ProtoWrapper[SomeMessage], abc.ABC):
    """ProtoWrapper around a specific "oneof" field in SomeMessage."""

    def __init__(self, proto: SomeMessage):
        super().__init__(proto)
        if self.expected_oneof_field() != self._proto.WhichOneof(self.oneof_name()):
            raise OpParseError(
                "expected oneof field not populated",
                expected=self.expected_oneof_field(),
            )

    def __hash__(self) -> int:
        return self._proto.SerializeToString(deterministic=True).__hash__()

    @classmethod
    @abc.abstractmethod
    def oneof_name(cls) -> str:
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def expected_oneof_field(cls) -> str:
        raise NotImplementedError()


ProtoOp = (
    table_pb2.TableComputeOp
    | table_pb2.SelectFromStagingOp
    | table_pb2.RenameColumnsOp
    | table_pb2.JoinOp
    | table_pb2.SelectColumnsOp
    | table_pb2.LimitRowsOp
    | table_pb2.OrderByOp
    | table_pb2.FilterRowsOp
    | table_pb2.DistinctRowsOp
    | table_pb2.UpdateMetadataOp
    | table_pb2.SetMetadataOp
    | table_pb2.RemoveFromMetadataOp
    | table_pb2.UpdateFeatureTypesOp
    | table_pb2.RollupByAggregationOp
    | table_pb2.EmptyOp
    | table_pb2.EmbedNode2vecFromEdgeListsOp
    | table_pb2.EmbeddingMetricsOp
    | table_pb2.EmbeddingCoordinatesOp
    | table_pb2.ReadFromParquetOp
)


def proto_op_hash(self: ProtoOp) -> int:
    return self.SerializeToString(deterministic=True).__hash__()


table_pb2.TableComputeOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.SelectFromStagingOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.RenameColumnsOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.JoinOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.SelectColumnsOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.LimitRowsOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.OrderByOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.FilterRowsOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.DistinctRowsOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.UpdateMetadataOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.SetMetadataOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.RemoveFromMetadataOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.UpdateFeatureTypesOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.RollupByAggregationOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.EmptyOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.EmbedNode2vecFromEdgeListsOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.EmbeddingMetricsOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.EmbeddingCoordinatesOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
table_pb2.ReadFromParquetOp.__hash__ = proto_op_hash  #  pyright: ignore[reportAttributeAccessIssue]
