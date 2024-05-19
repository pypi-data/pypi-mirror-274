from enum import Enum
from decimal import Decimal
from typing import Optional, Annotated
from pydantic import Field, ConfigDict
from beanie import Document, Indexed, Link
from datetime import datetime
from .utils import utcnow

class OHLCVData(Document):
    """
    Represents Open, High, Low, Close, and Volume data for a security over a specific time interval.

    Attributes:
        symbol (str): The ticker symbol used to identify the security.
        open (Decimal): The open price of the security.
        high (Decimal): The high price of the security.
        low (Decimal): The low price of the security.
        close (Decimal): The close price of the security.
        volume (Decimal): The volume of the security.
        ts_start (datetime): The start time of the OHLCV data.
        ts_end (datetime): The end time of the OHLCV data.
        time_int (str): The time interval of the OHLCV data.
        time_multiple (int): The time multiple of the OHLCV data.
    """
    symbol: Annotated[Link["Security"], Indexed(name="ohlcv_symbol")] = Field(title="Symbol", description="The ticker symbol used to identify the security.", required=True, unique_with=["ts_end","time_int","time_multiple"])
    open: Annotated[Decimal, Indexed(name="ohlcv_open")] = Field(default=0, title="Open", description="The open price of the security.")
    high: Optional[Decimal] = Field(default=0, title="High", description="The high price of the security.")
    low: Optional[Decimal] = Field(default=0, title="Low", description="The low price of the security.")
    close: Annotated[Decimal, Indexed(name="ohlcv_close")] = Field(default=0, title="Close", description="The close price of the security.")
    volume: Annotated[Decimal, Indexed(name="ohlcv_volume")] = Field(default=0, title="Volume", description="The volume of the security.")
    ts_start: Optional[datetime] = Field(default_factory=utcnow,title="Start Time",description="The start time of the OHLCV data.")
    ts_end: Optional[datetime] = Field(default_factory=utcnow,title="End Time",description="The end time of the OHLCV data.")
    time_int: Optional[str] = Field(default="min",title="Time Interval",description="The time interval of the OHLCV data.")
    time_multiple: Optional[int] = Field(default=1,title="Time Multiple",description="The time multiple of the OHLCV data.")

    model_config: ConfigDict = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,
        extra="forbid",
        str_to_upper=True,
        coerce_enum_to_str=True
    )
    
    class Settings:
        name = "ohlcv_data"
