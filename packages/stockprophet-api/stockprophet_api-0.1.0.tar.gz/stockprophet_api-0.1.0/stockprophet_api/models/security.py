from decimal import Decimal
from typing import Optional, List, Annotated
from datetime import datetime
from pydantic import ConfigDict, Field
from pymongo import ASCENDING as pymongo_ASCENDING
from beanie import Document, BeanieObjectId, Indexed

from .utils import utcnow

class Security(Document):
    """

    Metadata about any tradeable financial instrument.

    ### Attributes:
    - _id (BeanieObjectId): The unique identifier of the security metadata.
    - symbol (str): The ticker symbol of the security.
    - name (str, optional): The name of the security.
    - industry (str, optional): The industry of the security.
    - sector (str, optional): The sector of the security.
    - exchange (str): The exchange where the security is listed.
    - currency (str, optional): The currency of the security. Defaults to "USD".
    - country (str, optional): The country where the security is listed. Defaults to "US".
    - issued_shares (int, optional): The number of issued shares of the security.
    - outstanding_shares (int, optional): The number of outstanding shares of the security.
    - market_cap (int, optional): The market capitalization of the security.
    - eps (Decimal, optional): The earnings per share of the security.
    - description (str, optional): The description of the security.
    - website (str, optional): The website of the security.
    - tags (List[str], optional): The tags associated with the security. Defaults to an empty list.
    - listed_date (datetime, optional): The date when the security was listed. Defaults to the current date and time.
    - last_updated (datetime, optional): The date and time when the security metadata was last updated. Defaults to the current date and time.
    """
    _id: BeanieObjectId = None
    symbol: Annotated[str, Indexed(unique=True, name="securities_metadata_ticker_symbol", index_type=pymongo_ASCENDING)]
    name: Optional[str] = Field(None, example="Apple Inc.", title="Security Name", description="The name of the security.")
    industry: Optional[str] = Field(None, example="Technology", title="Industry", description="The industry of the security.")
    sector: Annotated[Optional[str], Indexed(name="securities_metadata_sector", index_type=pymongo_ASCENDING)]
    exchange: Annotated[str, Indexed(name="securities_metadata_exchange", index_type=pymongo_ASCENDING)]
    currency: Optional[str] = "USD"
    country:Optional[str] = "US"
    issued_shares: Optional[int] = None
    outstanding_shares: Optional[int] = None
    market_cap: Optional[int] = None
    description: Optional[str] = None
    website: Optional[str] = None
    listed_date: Optional[datetime] = None
    last_updated: datetime = utcnow()
    tags: Optional[List[str]] = []
    
    model_config: ConfigDict = ConfigDict(
        extra="allow",
        str_strip_whitespace=True,
        python_use_attribute_docstrings=True,
        str_to_upper=True,
        populate_by_name=True
    )
    """
    Pydantic model class configurations for the SecurityMetadata model.
    """
    
    class Settings:
        """
        Beanie model settings for the SecurityMetadata model.
        """
        name ="securities"
