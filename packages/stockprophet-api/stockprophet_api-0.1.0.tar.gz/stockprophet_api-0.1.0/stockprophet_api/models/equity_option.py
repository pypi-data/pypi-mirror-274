from datetime import datetime
from decimal import Decimal
from typing import Optional, Annotated
from pydantic import Field, ConfigDict, computed_field
from .utils import utcnow
from ..settings import Settings
from beanie import Document, Indexed
from math import exp, log, sqrt
from scipy.stats import norm
from .custom_types import Decimal128 as bson_Decimal128, ObjectId as bson_ObjectId
from .custom_types import datetime as bson_date
from pymongo import TEXT as pymongo_TEXT, IndexModel as pymongo_IndexModel, ASCENDING as pymongo_ASCENDING, DESCENDING as pymongo_DESCENDING
from .base_model import BaseModel


class EquityOption(BaseModel):
    symbol: str = Field(None, format="string",title="Underlying Symbol", description="The symbol of the underlying security.")
    security_id: str = Field(None, format="string", title="Security ID", description="The ID of the security.")
    expiry: bson_date = Field(None, format="datetime", title="Expiry", description="The date the option contract expires.")
    put_call: str = Field("CALL", title="Put/Call", description="The type of option (put or call).", enum=["PUT", "CALL"])
    strike: bson_Decimal128 = Field(None, format="decimal", title="Strike", description="The strike price of the option.")
    spot: bson_Decimal128 = Field(None, format="decimal", title="Spot Price", description="The current market price of the underlying asset.")
    implied_vol: bson_Decimal128 = Field(None, format="decimal", title="Implied Volatility", description="Implied volatility of the option contract.")
    delta: bson_Decimal128 = Field(None, format="decimal", title="Delta", description="Delta of the option contract.")
    gamma: bson_Decimal128 = Field(None, format="decimal", title="Gamma", description="Gamma of the option contract.")
    theta: bson_Decimal128 = Field(None, format="decimal", title="Theta", description="Theta of the option contract.")
    vega: bson_Decimal128 = Field(None, format="decimal", title="Vega", description="Vega of the option contract.")
    rho: bson_Decimal128 = Field(None, format="decimal", title="Rho", description="Rho of the option contract.")
    theo: bson_Decimal128 = Field(None, format="decimal", title="Theoretical Price", description="Theoretical price of the option contract.")
    volume: int = Field(None, format="integer", title="Volume", description="The volume of the option contract.")
    open_interest: int = Field(None, format="integer", title="Open Interest", description="Open interest of the option contract.")
    bid_00_px: bson_Decimal128 = Field(None, format="decimal", title="NBBO Bid Price", description="NBBO bid price of the option contract.")
    ask_00_px: bson_Decimal128 = Field(None, format="decimal", title="NBBO Ask Price", description="NBBO ask price of the option contract.")
    bid_00_sz: int = Field(None, format="integer", title="NBBO Bid Size", description="NBBO bid size of the option contract.")
    ask_00_sz: int = Field(None, format="integer", title="NBBO Ask Size", description="NBBO ask size of the option contract.")
    bid_99_sz: int = Field(None, format="integer", title="Book Bid Size", description="Book bid size of the option contract.")
    ask_99_sz: int = Field(None, format="integer", title="Book Ask Size", description="Book ask size of the option contract.")
    bid_01_px: bson_Decimal128 = Field(None, format="decimal", title="Book Bid Price", description="Book bid price of the option contract.")
    ask_01_px: bson_Decimal128 = Field(None, format="decimal", title="Book Ask Price", description="Book ask price of the option contract.")
    bid_01_sz: int = Field(None, format="integer", title="Book Bid Size", description="Book bid size of the option contract.")
    ask_01_sz: int = Field(None, format="integer", title="Book Ask Size", description="Book ask size of the option contract.")
    mark_px: bson_Decimal128 = Field(None, format="decimal", title="Market Price", description="The current market price for the option contract.")
    last_px: bson_Decimal128 = Field(None, format="decimal", title="Last Price", description="The last price of the option contract.")

    @computed_field(title="Theoretical Price", description="The theoretical price of the option contract.")
    def theoretical_price(self) -> bson_Decimal128:
        """
        A property method that returns the theoretical price of the option contract.
        """
        risk_free_rate = Settings.risk_free_rate
        d1 = (log(self.spot / self.strike) 
                + (risk_free_rate + 0.5 * self.implied_vol ** 2) 
                * self.time_value_years) / (self.implied_vol * sqrt(self.time_value_years))
        d2 = d1 - self.implied_vol * sqrt(self.time_value_years)
        if self.is_call:
            theo_price = self.spot * norm.cdf(d1) - self.strike * \
            exp(-risk_free_rate * self.time_value_years) * norm.cdf(d2)
        else:
            theo_price = self.strike * exp(-risk_free_rate * self.time_value_years) * norm.cdf(-d2) - self.spot * norm.cdf(-d1)
        return Decimal(theo_price)

    @computed_field(title="Days to Expire", description="The days to epiration of the option contract.")
    def days_to_expire(self) -> int:
        """
        A property method that returns the number of days until the option contract expires.
        """
        return (self.expiry - datetime.now()).days if self.expiry and self.is_expired is False else 0
    
    @computed_field(title="Expiry Date (Pretty)", description="The expiry date of the option contract printed as a formatted string.")
    def expiry_pretty(self) -> str:
        """
        A property method that returns the expiry date formatted as "%Y-%m-%d" if expiry is available, otherwise an empty string.
        """
        return self.expiry.strftime("%Y-%m-%d") if self.expiry else ""

    @computed_field(title="Strike (Pretty)", description="The strike price of the option contract printed as a formatted string.")
    def strike_pretty(self) -> str:
        """
        A property method that returns the strike value formatted to 2 decimal places, or an empty string if strike is not available.
        """
        return '${:,.2f}'.format(self.strike) if self.strike is not None else ""

    @computed_field(title="Spot (Pretty)", description="The current market price of the underlying asset printed as a formatted string.")
    def spot_pretty(self) -> str:
        """
        A property method that returns the spot value formatted to two decimal places, or an empty string if spot is not available.
        """
        return '${:,.2f}'.format(self.spot) if self.spot is not None else ""

    @computed_field(title="Days to Expiry (Pretty)", description="The days to expiration of the option contract printed as a formatted string.")
    def dte_pretty(self) -> str:
        """
        A property method that returns a formatted string representing the days to expiration (dte) in days.
        """
        return f"{self.days_to_expire} days" if self.days_to_expire else ""

    @computed_field(title="Time Value (Years)", description="The time value of the option contract in years.")
    def time_value_years(self) -> bson_Decimal128:
        """
        A property method that calculates the time value in years based on the days to expiration.
        """
        return self.dte / 365 if self.dte and self.dte > 0 else 0

    @computed_field(title="Is Call", description="True if Put/Call is equal to CALL")
    def is_call(self) -> bool:
        return self.put_call == "CALL"

    @computed_field(title="Is Put", description="True if Put/Call is equal to PUT")
    def is_put(self) -> bool:
        return self.put_call == "PUT"

    @computed_field(title="Is Expired", description="True if the option contract is expired")
    def is_expired(self) -> bool:
        return self.expiry < datetime.now()

    @computed_field(title="Is ITM", description="True if the option contract is ITM")
    def is_itm(self) -> bool:
        return self.strike < self.spot if self.is_call else self.strike > self.spot

    @computed_field(title="Is OTM", description="True if the option contract is OTM")
    def is_otm(self) -> bool:
        return self.strike > self.spot if self.is_call else self.strike < self.spot

    @computed_field(title="Is ATM", description="True if the option contract is ATM")
    def is_atm(self) -> bool:
        return self.strike == round(self.spot,2)
    
    class Settings:
        name = "equity_options"
        indexes = [
            [
                ("security_id", pymongo_TEXT), 
                ("description", pymongo_TEXT),
                ("symbol", pymongo_TEXT),
                ("expiry", pymongo_DESCENDING),
                ("put_call", pymongo_TEXT),
                ("strike", pymongo_ASCENDING),
                ("spot", pymongo_ASCENDING),
                ("implied_vol", pymongo_ASCENDING),
                ("volume", pymongo_ASCENDING),
                ("open_interest", pymongo_ASCENDING),
            ],
            pymongo_IndexModel(
                [
                    ("symbol", pymongo_TEXT), 
                    ("expiry", pymongo_DESCENDING), 
                    ("put_call", pymongo_TEXT), 
                    ("strike", pymongo_ASCENDING)], 
                unique=True
            )
        ]

    def calc_theo(self):
        @property
        def theo_price(self) -> Decimal:
            """
            Calculate the theoretical price of the option contract using the Black-Scholes formula.
            """
            risk_free_rate = 0.0442
            d1 = (log(self.spot / self.strike) + (risk_free_rate + 0.5 * self.implied_vol ** 2) * self.time_value_years) / (self.implied_vol * sqrt(self.time_value_years))
            d2 = d1 - self.implied_vol * sqrt(self.time_value_years)
            if self.is_call:
                theo_price = self.spot * norm.cdf(d1) - self.strike * exp(-risk_free_rate * self.time_value_years) * norm.cdf(d2)
            else:
                theo_price = self.strike * exp(-risk_free_rate * self.time_value_years) * norm.cdf(-d2) - self.spot * norm.cdf(-d1)
            return Decimal(theo_price)
# class EquityOption(Document):
#     """
#     Represents an equity option contract.

#     Attributes:
#         instrument_id (str): The id of the option contract.
#         expiry (datetime): The date the option contract expires.
#         put_call (PutCall): The type of option contract.
#         strike (Decimal): The strike price of the option contract.
#         spot (Decimal): The current market price of the underlying asset.
#         symbol (str): Ticker symbol of the underlying security.
#         impl_vol (Decimal, optional): Implied volatility of the option contract.
#         delta (Decimal, optional): Delta of the option contract.
#         gamma (Decimal, optional): Gamma of the option contract.
#         theta (Decimal, optional): Theta of the option contract.
#         vega (Decimal, optional): Vega of the option contract.
#         rho (Decimal, optional): Rho of the option contract.
#         theo (Decimal, optional): Theoretical price of the option contract.
#         volume (int, optional): Volume of the option contract.
#         open_interest (int, optional): Open interest of the option contract.
#         nbbo_bid_price (Decimal, optional): NBBO bid price of the option contract.
#         nbbo_ask_price (Decimal, optional): NBBO ask price of the option contract.
#         nbbo_bid_size (int, optional): NBBO bid size of the option contract.
#         nbbo_ask_size (int, optional): NBBO ask size of the option contract.
#         book_bid_size (int, optional): Book bid size of the option contract.
#         book_ask_size (int, optional): Book ask size of the option contract.
#         last_trade_price (Decimal, optional): Last trade price of the option contract.
#         last_trade_time (datetime, optional): Last trade time of the option contract.
#     """

#     model_config: ConfigDict = ConfigDict(
#         str_strip_whitespace=True,
#         populate_by_name=True,
#         str_to_upper=True,
#     )
#     """Pydantic Model Config"""
#     class Settings:
#         name = "equity_options"

#     security_id: str = Field(None, unique=True, required=True, title="Security ID", description="The id of the option contract.")

#     expiry: Annotated[datetime, Indexed()] = Field(
#         default_factory=utcnow, 
#         title="Expiry",
#         description="The date the option contract expires",
#         example="2024-12-31",
#         format="%Y-%m-%d",
#     )

#     put_call: Annotated[str, Indexed(name="equity_option_putcall")] = Field(
#         required=True,
#         enums=["CALL", "PUT"],
#         example="PUT",
#         title="Option Type", 
#         description="The type of option contract",
#     )

#     strike: Annotated[Decimal, Indexed(name="equity_option_strike")] = Field(
#         required=True, 
#         example=100.0,
#         default_factory=None,
#         title="Strike", 
#         description="The strike price of the option contract", 
#         decimal_places=2,
#     )

#     spot: Annotated[Decimal,Indexed()] = Field(
#         required=True,
#         default_factory=None,
#         example=100.0, 
#         title="Spot Price",
#         decimal_places=2,
#         description="The current market price of the underlying asset", 
#     )

#     symbol: Annotated[str, Indexed()] = Field(
#         None,
#         required=True,
#         example="AAPL",
#         title="Underlying Symbol", 
#         description="The symbol of the underlying security",
#     )
    
#     implied_vol: Annotated[Decimal, Field(
#         None,
#         title="Implied Volatility", 
#         description="Implied volatility of the option contract", 
#         decimal_places=8,
#         gt=0
#         )] | None = None
    
#     delta: Optional[Decimal] = None
#     gamma: Optional[Decimal] = None
#     theta: Optional[Decimal] = None
#     vega: Optional[Decimal] = None
#     rho: Optional[Decimal] = None
#     theo: Optional[Decimal] = None
#     volume: Optional[int] = None
#     open_interest: Optional[int] = None
#     nbbo_bid: Optional[Decimal] = None
#     nbbo_ask: Optional[Decimal] = None
#     nbbo_bid_size: Optional[int] = None
#     nbbo_ask_size: Optional[int] = None
#     book_bid_size: Optional[int] = None
#     book_ask_size: Optional[int] = None
#     last_trade_price: Optional[datetime] = None
#     last_trade_size: Optional[int] = None
#     last_trade_time: Optional[datetime] = None

#     def __str__(self):
#         return f"{self.symbol} {self.spot_pretty} {self.expiry_pretty} {self.put_call} {self.strike_pretty}"

#     def __repr__(self):
#         return f"{self.symbol} {self.spot_pretty} {self.expiry_pretty} {self.put_call} {self.strike_pretty}"

#     def __eq__(self, other):
#         return (
#             self.symbol == other.symbol
#             and self.expiry == other.expiry
#             and self.put_call == other.put_call
#             and self.strike == other.strike
#             and self.security_id == other.security_id
#             and self.symbol == other.symbol
#         )

#     def __hash__(self):
#         return hash(
#             (
#                 self.symbol,
#                 self.expiry,
#                 self.put_call,
#                 self.strike,
#             )
#         )

#     @property
#     def expiry_pretty(self) -> str:
#         """
#         A property method that returns the expiry date formatted as "%Y-%m-%d" if expiry is available, otherwise an empty string.
#         """
#         return self.expiry.strftime("%Y-%m-%d") if self.expiry else ""

#     @property
#     def strike_pretty(self) -> str:
#         """
#         A property method that returns the strike value formatted to 2 decimal places, or an empty string if strike is not available.
#         """
#         return '${:,.2f}'.format(self.strike) if self.strike is not None else ""

#     @property
#     def spot_pretty(self) -> str:
#         """
#         A property method that returns the spot value formatted to two decimal places, or an empty string if spot is not available.
#         """
#         return '${:,.2f}'.format(self.spot) if self.spot is not None else ""

#     @property
#     def dte_pretty(self) -> str:
#         """
#         A property method that returns a formatted string representing the days to expiration (dte) in days.
#         """
#         return f"{self.days_to_expire} days" if self.days_to_expire else ""

#     @property
#     def time_value_years(self) -> Decimal:
#         """
#         A property method that calculates the time value in years based on the days to expiration.
#         """
#         return self.dte / 365 if self.dte and self.dte > 0 else 0


#     @property
#     def is_call(self) -> bool:
#         return self.put_call == "CALL"

#     @property
#     def is_put(self) -> bool:
#         return self.put_call == "PUT"

#     @property
#     def is_expired(self) -> bool:
#         return self.expiry < datetime.now()

#     @property
#     def days_to_expire(self) -> Optional[int]:
#         if self.expiry:
#             return (self.expiry - datetime.now()).days
#         else:
#             return None

#     @property
#     def calculate_impl_vol(self) -> Decimal:
#         """
#         Calculate the implied volatility of the option contract.
#         """
#         # Define the target function
#         def target_function(impl_vol):
#             self.implied_vol = impl_vol
#             return self.black_scholes_price - self.theo

#         # Define the derivative of the target function
#         def target_function_derivative(impl_vol):
#             self.implied_vol = impl_vol
#             d1 = (log(self.spot / self.strike) + (risk_free_rate + 0.5 * self.implied_vol ** 2) * self.time_value_years) / (self.implied_vol * sqrt(self.time_value_years))
#             if self.is_call:
#                 return self.spot * norm.pdf(d1) * sqrt(self.time_value_years)
#             else:
#                 return -self.spot * norm.pdf(d1) * sqrt(self.time_value_years)

#         # Use the Newton-Raphson method to find the implied volatility
#         initial_guess = 0.5  # Initial guess for the implied volatility
#         max_iterations = 100  # Maximum number of iterations
#         tolerance = 1e-6  # Tolerance for convergence

#         # Perform the Newton-Raphson iteration
#         for _ in range(max_iterations):
#             f = target_function(initial_guess)
#             f_prime = target_function_derivative(initial_guess)
#             new_guess = initial_guess - f / f_prime
#             if abs(new_guess - initial_guess) < tolerance:
#                 break
#             initial_guess = new_guess

#         return Decimal(new_guess)
#     @property
#     def black_scholes_price(self) -> Decimal:
#         risk_free_rate = 0.04

#         d1 = (log(self.spot / self.strike) + (risk_free_rate + 0.5 * self.implied_vol ** 2) * self.time_value_years) / (self.implied_vol * sqrt(self.time_value_years))
#         d2 = d1 - self.implied_vol * sqrt(self.time_value_years)

#         if self.is_call:
#             price = self.spot * norm.cdf(d1) - self.strike * exp(-risk_free_rate * self.time_value_years) * norm.cdf(d2)
#         else:
#             price = self.strike * exp(-risk_free_rate * self.time_value_years) * norm.cdf(-d2) - self.spot * norm.cdf(-d1)

#         return price