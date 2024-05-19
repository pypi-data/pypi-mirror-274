from typing import List
from fastapi import APIRouter, HTTPException
from models import Security

securities_router = APIRouter()
@securities_router.get("/securities/{symbol}", response_model=Security)
async def get_security(symbol: str):
    """
    Get equity information for a specific ticker symbol.

    Parameters:
        symbol (str): The primary security identifier for the security requested.

    Returns:
        Security: The metadata for the security corresponding to the symbol provided.
    """
    # Find the security with the given symbol
    security = await Security.find_one({'symbol': symbol})
    if not security:
        # If security is not found, raise an HTTPException with a 404 status code
        exception_msg = f"Security not found for ticker {symbol}"
        raise HTTPException(status_code=404, detail=exception_msg)
    return security

@securities_router.get("/securities/", response_model=List[Security])
async def get_securities():
    """
    Get all securities.

    Returns:
        List[Security]: A list of all securities.
    """
    # Find all securities and return them as a list
    return await Security.find_all().to_list()

@securities_router.get("/securities/exchange/{exchange_name}", response_model=List[Security])
async def get_securities_by_exchange(exchange_name: str):
    """
    Get securities by exchange name.

    Parameters:
        exchange_name (str): The name of the exchange to retrieve securities from.

    Returns:
        List[Security]: A list of Security objects from the specified exchange.
    """
    # Find securities with the specified exchange name and return them as a list
    return await Security.find_many({"exchange": exchange_name}).to_list()

@securities_router.get("/securities/sector/{sector}", response_model=List[Security])
async def get_securities_by_sector(sector: str):
    """
    Get securities by sector.

    Parameters:
        sector (str): The sector to filter securities by.

    Returns:
        List[Security]: A list of securities belonging to the specified sector.
    """
    # Find securities with the specified sector and return them as a list
    return await Security.find_many({"sector": sector}).to_list()

@securities_router.get("/securities/industry/{industry}", response_model=List[Security])
async def get_securities_by_industry(industry: str):
    """
    Get securities by industry.

    Parameters:
        industry (str): The industry to filter securities by.

    Returns:
        List[Security]: A list of securities belonging to the specified industry.
    """
    # Find securities with the specified industry and return them as a list
    return await Security.find_many({"industry": industry}).to_list()