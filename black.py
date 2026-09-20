import math
from scipy.stats import norm
import qfin as qf
import matplotlib.pyplot as plt


def black_scholes(S, K, T, r, vol, q=0):
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

    return round(call, 2)


def black_scholes_plot(S, K, T, r, vol, option_type="call"):

    premium = black_scholes(45, 40, 1, 0.1, 0.2, 0.01)

    path = qf.simulations.GeometricBrownianMotion(S, r, vol, 1/252, T)

    plt.style.use('dark_background')

    plt.hlines(K, 0, T * 252, label="Strike", color="Blue")

    plt.plot(path.simulated_path, label="Price Path", color="White")

    if path.simulated_path[-1] <= K:
        plt.vlines(252, path.simulated_path[-1], K, color='red', label="P/L")
        print(f"Loss of {premium}")
    else:
        plt.vlines(
            252, K, path.simulated_path[-1], color='green', label="P/L")
        print(f"Win of {path.simulated_path[-1] - K - premium}")

    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()


black_scholes_plot(45, 40, 1, 0.1, 0.2)
