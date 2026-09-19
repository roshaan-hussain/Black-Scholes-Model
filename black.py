import math
from scipy.stats import norm


def black_scholes(S, K, T, r, vol, q=0):
    # S = Underlying price
    # K = Strike price
    # T = Time to expiration
    # r = Risk-free rate
    # vol = Volatility
    # q = dividend yield (0 = no dividends)

    d1 = (math.log(S/K) + (r - q + 0.5 * vol**2)*T) / (vol * math.sqrt(T))

    d2 = d1 - (vol * math.sqrt(T))

    # Call option price

    C = S * norm.cdf(d1) * math.exp(-q*T) - K * math.exp(-r*T) * norm.cdf(d2)

    # Put option price

    P = K * math.exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(-d1) * math.exp(-q*T)

    print(f"The value of d1 is: {round(d1, 4)}")
    print(f"The value of d2 is: {round(d2, 4)}")
    print(f"The price of the buy option is: ${round(C, 2)}")
    print(f"The price of the sell option is: ${round(P, 2)}")


black_scholes(45, 40, 1, 0.1, 0.2, 0.01)
