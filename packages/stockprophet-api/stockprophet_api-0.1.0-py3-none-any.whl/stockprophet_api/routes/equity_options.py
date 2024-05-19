from fastapi import APIRouter, HTTPException
from models import EquityOption

options_router = APIRouter()
@options_router.get("/equity-options/{option_id}", response_model=EquityOption)
async def get_equity_option(option_id: str):
    eq_opt = await EquityOption.find_one({'security_id': option_id})
    if not eq_opt:
        # If security is not found, raise an HTTPException with a 404 status code
        exception_msg = f"Equity Option not found for symbol {option_id}"
        raise HTTPException(status_code=404, detail=exception_msg)
    return eq_opt

# @options_router.get("/equity-options/{symbol}", response_model=List[EquityOption])
# async def get_option_chain(equity_symbol:str):
#     """
#     Get the option chain for a given equity found by symbool

#     Returns:
#         List[Security]: The option chain for a given equity
#     """
#     # Returns the equity options (option chain) as a list
#     return await EquityOption.find_many(
#         {
#             'symbol':equity_symbol, 
#             'is_expired': False
#         }).to_list() if equity_symbol else {}

# @options_router.get("/equity-options/call/{symbol}", response_model=List[EquityOption])
# async def get_call_options(equity_symbol:str):
#     """
#     Get the call options for a given equity found by symbol

#     Returns:
#         List[Security]: The call options for a given equity
#     """
#     # Returns the call options as a list
#     return await EquityOption.find_many(
#         {
#             'symbol':equity_symbol, 
#             'put_call': 'CALL',
#             'is_expired': False
#         }).to_list() if equity_symbol else []
    
# @options_router.get("/equity-options/put/{symbol}", response_model=List[EquityOption])
# async def get_put_options(equity_symbol:str):
#     """
#     Get the put options for a given equity found by symbol

#     Returns:
#         List[Security]: The put options for a given equity
#     """
#     # Returns the put options as a list
#     return await EquityOption.find_many(
#         {
#             'symbol':equity_symbol, 
#             'put_call': 'PUT',
#             'is_expired': False
#         }).to_list() if equity_symbol else []

# @options_router.get("/equity-options/{symbol}/calculator&calculate={function}date_to_calculate={date}&cost={cost}&size={size}", response_model=EquityOption)
# async def get_unusual_options(equity_symbol:str, function:str, date:str, cost:Decimal, size:int):
#     """
#     Get the unusual options for a given equity found by symbol

#     Returns:
#         List[Security]: The unusual options for a given equity
#     """
#     print /f"Calculating {function} for {equity_symbol} on {date} with cost {cost} and size {size}"
#     # Returns the unusual options as a list
#     return await EquityOption.find_one() if equity_symbol else {}