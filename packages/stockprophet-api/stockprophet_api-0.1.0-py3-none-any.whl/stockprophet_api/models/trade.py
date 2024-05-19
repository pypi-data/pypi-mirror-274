from datetime import datetime, timezone
from typing import Annotated, Optional
from decimal import Decimal
from beanie import Document, Indexed, TimeSeriesConfig, Granularity
from pydantic import Field, ConfigDict
from .utils import utcnow

class Trade(Document):
    
    security: Annotated[str,Indexed(name="trades_symbol")] = Field(
        example="AAPL",
        primary_key=True,
        title="Instrument ID",
        description="Ticker symbol used to identify the equity or option contract associated with the trade."
    )

    ts_event: Annotated[datetime, Indexed(name="trades_executed_time")] = Field(
        default_factory=utcnow,
        example=[datetime.now(timezone.utc)],
        title="Executed Time",
        description="Trade execution time in datetime format"
    )

    price: Annotated[Decimal,Indexed(name="trades_price")] = Field(None, 
        example=Decimal(100.00),
        title="Price",
        description="The price of the trade."
    )
    

    size: Annotated[int, Indexed(name="trades_size")] = Field(
        example=100,
        title="Size",
        description="The quantity of the trade."
    )
    
    buy_sell: Optional[str] = Field(
        None, title="Buy/Sell", 
        enums=["BUY","SELL"],
        description="The market side SELL (bid) or BUY (ask) of the trade."
    )

    model_config: ConfigDict = ConfigDict(
        coerce_numbers_to_str=False,
        extra='allow',
        str_strip_whitespace=True,
        populate_by_name=True,
        use_enum_values=True,
        python_use_attribute_docstrings=True,
        str_to_upper=True
    )

    class Settings:
        name = "trades"
        timeseries = TimeSeriesConfig(
            time_field="ts",
            granularity=Granularity.minutes,
        )