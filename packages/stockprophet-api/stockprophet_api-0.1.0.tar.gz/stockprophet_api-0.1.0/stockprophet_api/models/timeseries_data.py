from .custom_types import Decimal128 as Decimal
from typing_extensions import Annotated, get_args, get_origin, get_type_hints
from typing import Optional
from datetime import datetime
from pydantic import Field
from beanie import TimeSeriesConfig, Granularity, Indexed, SortDirection
from .utils import utcnow
from .base_model import BaseModel

class TimeSeriesData(BaseModel):
    sym: Annotated[str, Indexed(name="ts_data_symbol")] = Field(title="Symbol", description="The ticker symbol used to identify the security.")
    o_px: Annotated[Optional[Decimal], Indexed(0, name="ts_data_open")] = Field(title="Open", description="The open price of the security.")
    h_px: Annotated[Optional[Decimal],Field(0, title="High", description="The high price of the security.")]
    l_px: Annotated[Optional[Decimal], Field(0, title="Low", description="The low price of the security.")]
    c_px: Annotated[Optional[Decimal], Field(0, title="Close", description="The close price of the security.")]
    vol: Optional[Decimal] = Field(0,title="Volume", description="The volume of the security.")
    ts_0: Optional[datetime] = Field(0,default_factory=utcnow,title="Start Time",description="The start time of the OHLCV data.")
    ts_1: Optional[datetime] = Field(0,default_factory=utcnow,title="End Time",description="The end time of the OHLCV data.")
    ts_t: Optional[str] = Field(0,default="minute",title="Time Interval",description="The time interval of the OHLCV data.", enums=["minute","hour","day"])
    ts_m: Optional[int] = Field(0default=1,title="Time Multiple",description="The time multiple of the OHLCV data.")
    
    class Settings:
        name = "ts_data"
        timeseries = TimeSeriesConfig(
            time_field="ts",
            granularity=Granularity.minutes,
        )