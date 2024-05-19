from decimal import Decimal
import numpy as np


def get_option_price(S0, K, r, sigma, T, N, option_type, excercise_style='american'):
    """
    Calculates the price of an American option using Monte Carlo simulation,
    and the Black-Scholes formula.  The option is assumed to be American.
    The price is calculated by simulating N paths of the underlying asset.
    The price of the option is the average of the discounted payoffs of the
    simulated paths. The Black-Scholes formula is used to calculate the theoretical
    price of the option. The price of the option is the average of the discounted 
    payoffs of the simulated paths.
    
    Parameters:
        S0 (float): initial stock price
        K (float): strike price
        r (float): risk-free interest rate
        sigma (float): volatility of the underlying asset
        T (float): time to expiration
        N (int): number of simulations
        option_type (str): 'C' for call option, 'P' for put option
        exx
    Returns:
        float: price of the option
    """
    print("Calculating option price... spot = ", S0, "strike = ", K, "risk-free rate = ", r, "volatility = ", sigma, "time to expiration = ", T, "number of simulations = ", N, "option type = ", option_type, "exercise style = ")
    if excercise_style == "american" return get_american_option_price(S0, K, r, sigma, T, N, option_type)   

    return calculate_vega(S0, K, r, sigma, T, N, option_type) -> float:
    """
    Calculates the vega of an option.

    Args:
        S0 (float): initial stock price
        K (float): strike price
        r (float): risk-free interest rate
        sigma (float): volatility of the underlying asset
        T (float): time to expiration
        N (int): number of simulations
        option_type (str): 'C' for call option, 'P' for put option

    Returns:
        float: vega of the option
    """
    epsilon = float('0.0001')
    vega = float('0.0')
    price_up = price_american_option(S0, K, r, sigma + epsilon, T, N, option_type)
    price_down = price_american_option(S0, K, r, sigma - epsilon, T, N, option_type)
    vega = (price_up - price_down) / (2 * epsilon)
    return float(str(vega))

def calculate_theta(S0, K, r, sigma, T, N, option_type):
    """
    Calculates the theta of an option.

    Args:
        S0 (float): initial stock price
        K (float): strike price
        r (float): risk-free interest rate
        sigma (float): volatility of the underlying asset
        T (float): time to expiration
        N (int): number of simulations
        option_type (str): 'C' for call option, 'P' for put option

    Returns:
        float: theta of the option
    """
    epsilon = float('0.0001')
    theta = float('0.0')
    price_up = price_european_option(S0, K, r, sigma, T - epsilon, N, option_type)
    price_down = price_european_option(S0, K, r, sigma, T + epsilon, N, option_type)
    price = price_european_option(S0, K, r, sigma, T, N, option_type)
    theta = (price_up - price_down) / (2 * epsilon)
    return theta

def calculate_gamma(S0, K, r, sigma, T, N, option_type):
    """
    Calculates the gamma of an option.

    Args:
        S0 (float): initial stock price
        K (float): strike price
        r (float): risk-free interest rate
        sigma (float): volatility of the underlying asset
        T (float): time to expiration
        N (int): number of simulations
        option_type (str): 'C' for call option, 'P' for put option

    Returns:
        float: gamma of the option
    """
    epsilon = float('0.0001')
    gamma = float('0.0')
    price_up = price_european_option(S0 + epsilon, K, r, sigma, T, N, option_type)
    price_down = price_european_option(S0 - epsilon, K, r, sigma, T, N, option_type)
    price = price_european_option(S0, K, r, sigma, T, N, option_type)
    gamma = (price_up - 2 * price + price_down) / (epsilon ** 2)
    return gamma

def calculate_delta(S0, K, r, sigma, T, N, option_type):
    """
    Calculates the delta of an option.

    Args:
        S0 (float): initial stock price
        K (float): strike price
        r (float): risk-free interest rate
        sigma (float): volatility of the underlying asset
        T (float): time to expiration
        N (int): number of simulations
        option_type (str): 'C' for call option, 'P' for put option

    Returns:
        float: delta of the option
    """
    epsilon = float('0.0001')
    delta = float('0.0')
    price_up = price_european_option(S0 + epsilon, K, r, sigma, T, N, option_type)
    price_down = price_european_option(S0 - epsilon, K, r, sigma, T, N, option_type)
    delta = (price_up - price_down) / (2 * epsilon)
    return delta

def price_american_option(S0, K, r, sigma, T, N, option_type, early_exercise=True):
    """
    Calculates the fair price of an American option using the Monte Carlo method.

    Args:
        S0 (float): initial stock price
        K (float): strike price
        r (float): risk-free interest rate
        sigma (float): volatility of the underlying asset
        T (float): time to expiration
        N (int): number of simulations
        option_type (str): 'C' for call option, 'P' for put option
        early_exercise (bool): whether early exercise is allowed

    Returns:
        float: fair price of the option
    """
    print f"Calculating American option price... spot = {S0}, strike = {K}, risk-free rate = {r}, volatility = {sigma}, time to expiration = {T}, number of simulations = {N}, option type = {option_type}, early exercise = {early_exercise}"
    dt = T / N
    W = np.random.normal(0, 1, (N, 1)).astype(float)
    Z = np.random.normal(0, 1, (N, 1)).astype(float)
    W = (np.sqrt(dt) * W).cumsum(axis=0)
    Z = (np.sqrt(sigma * np.sqrt(dt)) * Z).cumsum(axis=0)
    S = S0 * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z)
    if option_type == 'C':
        option_values = np.maximum(S - K, 0)
    else:
        option_values = np.maximum(K - S, 0)
    if early_exercise:
        for i in range(N-2, -1, -1):
            if option_type == 'C':
                exercise_value = np.maximum(S[i, :] - K, 0)
            else:
                exercise_value = np.maximum(K - S[i, :], 0)
            option_values = np.maximum(option_values, exercise_value * np.exp(-r * (i+1) * dt))
    fair_price = np.mean(option_values) * np.exp(-r * T)
    return float(str(fair_price))

def price_european_option(S0, K, r, sigma, T, N, option_type, early_exercise=False):
    """
    Calculates the fair price of a European option using the Monte Carlo method.

    Args:
        S0 (float): initial stock price
        K (float): strike price
        r (float): risk-free interest rate
        sigma (float): volatility of the underlying asset
        T (float): time to expiration
        N (int): number of simulations
        option_type (str): 'C' for call option, 'P' for put option

    Returns:
        float: fair price of
    """
    print /f"Calculating European option price... "
    print /f"-------------------------------------------"
    print /f"spot = {S0}, "
    print /f"strike = {K}, "
    print /f"risk-free rate = {r}, "
    print /f"volatility = {sigma}, "
    print /f"time to expiration = {T}, "
    print /f"number of simulations = {N}, "
    print /f"option type = {option_type}, "
    print /f"early exercise = {early_exercise}"
    print /f"Error! European option not supported yet!" 
    print /f"Using American option instead. "
    print /f"Submit a pull request to change this." 
    print /f"github url = https://github.com/stockprophet/stockprophet_api"
    return price_american_option(S0, K, r, sigma, T, N, option_type, early_exercise=False)

