import math
from scipy.stats import norm
import qfin as qf
import matplotlib.pyplot as plt


def black_scholes(S, K, T, r, vol, q=0, option_type="call"):
    # S - current price
    # K - strike price
    # T - Time to expiry (years)
    # r - risk-free rate
    # vol - volatility
    # q - dividend yield (0 = no dividends)

    d1 = (math.log(S/K) + (r - q + 0.5 * vol**2)*T) / (vol * math.sqrt(T))

    d2 = d1 - (vol * math.sqrt(T))

    # Call option price

    call = S * norm.cdf(d1) * math.exp(-q*T) - K * \
        math.exp(-r*T) * norm.cdf(d2)

    # Put option price

    put = K * math.exp(-r*T) * norm.cdf(-d2) - S * \
        norm.cdf(-d1) * math.exp(-q*T)

    if option_type == "call":
        return round(call, 2)
    else:
        return round(put, 2)


def black_scholes_plot(S, K, T, r, vol, q, option_type):

    premium = black_scholes(S, K, T, r, vol, q, option_type)

    path = qf.simulations.GeometricBrownianMotion(S, r, vol, 1/252, T)

    if option_type == "call":
        pay = max(path.simulated_path[-1] - K, 0)
    else:
        pay = max(K - path.simulated_path[-1], 0)

    plt.style.use('dark_background')

    plt.hlines(K, 0, T * 252, label="Strike", color="Blue")

    plt.plot(path.simulated_path, label="Price Path", color="White")

    if pay - premium < 0:
        plt.vlines(252, path.simulated_path[-1], K, color='red', label="P/L")
        print(f"Loss of {round(premium - pay, 2)}")
    elif pay - premium == 0:
        print(f"Breakeven")
    else:
        plt.vlines(
            252, K, path.simulated_path[-1], color='green', label="P/L")
        print(f"Win of {round(pay - premium, 2)}")

    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()


black_scholes_plot(35, 40, 1, 0.1, 0.2, 0.01, "call")
