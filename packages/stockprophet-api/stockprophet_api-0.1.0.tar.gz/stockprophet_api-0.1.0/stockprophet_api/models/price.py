from __future__ import annotations
import decimal
from decimal import Decimal
from typing import Any, Dict, Type, Union
from typing_extensions import TypeVar
from bson import Decimal128
from pydantic import BaseModel


T: Type = TypeVar('T', int, float, Decimal, Decimal128)

class Price(T):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update({"type": "number"})

    @classmethod
    def validate(cls, v: Union[str, int, float, Decimal, Decimal128]) -> Decimal:
        if isinstance(v, str):
            v = decimal.Decimal(v)
        elif isinstance(v, (int, float)):
            v = decimal.Decimal(v) / 1000000000
        elif isinstance(v, Decimal128):
            v = v.to_decimal()
        return v
