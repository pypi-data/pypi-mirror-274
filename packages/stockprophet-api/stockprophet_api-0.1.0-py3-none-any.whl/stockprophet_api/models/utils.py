from typing_extensions import Annotated
from typing import Any
from datetime import datetime, timezone
from pydantic import SerializerFunctionWrapHandler
from pydantic.functional_serializers import WrapSerializer



def utcnow() -> datetime:
    """
    Get the current datetime in UTC timezone.

    Returns:
        datetime: The current datetime in UTC timezone.
                    Currently mongo does not support 
                    datetime in UTC timezone.
    """
    # Convert the current datetime to UTC timezone
    return datetime.utcnow()
