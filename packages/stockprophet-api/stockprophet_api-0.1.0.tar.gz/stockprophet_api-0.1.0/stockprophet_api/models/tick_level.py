from decimal import Decimal
from typing import Literal
from pydantic import Field
from .base_model import BaseModel
from .custom_types import Decimal128
from docker.utils.json_stream import json_decoder




class TickLevel(BaseMode, revalidate_instances="never", json_decoders={Decimal128: json_decoder})(BaseModel):
    bid_px: int = 0
    ask_px: int = Field(0, title="Ask Price", description="The ask price of the security.", gte=0)
    bid_sz: int
    ask_sz: int
    bid_ct: int
    ask_ct: int
    tick: Decimal

    def __init__(self, **data):
        super().__init__(**data)
        self.tick = float(self.tick)

    class Settings:
        name = "tick_level"
        indexes = [
            [
                ("tick", pymongo_DESCENDING),
            ],
            pymongo_IndexModel(
                [
                    ("tick", pymongo_DESCENDING),
                ],
                unique=True
            )
        ]
        


    class Config:
        revalidate_instances: Literal["never"]
        arbitrary_types_allowed = False
        allow_inf_nan: False
        json_encoders = {
            Decimal: lambda v: Decimal(v / 1000000000,
        }
        json_decoders = {
            Decimal128: lambda v: Decimal(v),
        }