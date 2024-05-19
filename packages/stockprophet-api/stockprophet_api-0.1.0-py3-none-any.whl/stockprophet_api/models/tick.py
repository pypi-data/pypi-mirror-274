from typing import TYPE_CHECKING, Any, Literal

from decimal import Decimal

from pydantic import Field

from .base_model import BaseModel
from .price import Price

class TickLevel(BaseModel):
    
    bid_px: Price = Field(0, title="Bid Price", description="The bid price of the security.", gte=0)
    ask_px: Price = Field(0, title="Ask Price", description="The ask price of the security.", gte=0)
    bid_sz: int = Field(0, title="Bid Size", description="The bid size of the security.", gte=0)
    ask_sz: int = Field(0, title="Ask Size", description="The ask size of the security.", gte=0)
    bid_ct: int = Field(0, title="Bid Count", description="The bid count of the security.", gte=0)
    ask_ct: int = Field(0, title="Ask Count", description="The ask count of the security.", gte=0)
    level: int = Field(0, title="Level", description="The order book level associated with this data.", gte=0)

    def __init__(self, **data):
        super().__init__(**data)
        self.model_config.update(anystr_strip_whitespace = True)
    if TYPE_CHECKING:
        def model_dump(
            self,
            *,
            mode: Literal['json', 'python'] | str = 'python',
            include: Any = None,
            exclude: Any = None,
            by_alias: bool = False,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
            round_trip: bool = False,
            warnings: bool = True,
        ) -> str:
        
    class Config():
        title = "Tick Level"
        anystr_strip_whitespace = True
        validate_assignment = False
        validate_all = False
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        extra = "forbid"
        str_to_upper = True
        json_schema_serialization_defaults_required: False