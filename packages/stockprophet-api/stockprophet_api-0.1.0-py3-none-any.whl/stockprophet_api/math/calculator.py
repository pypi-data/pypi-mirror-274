import math
# RISK FREE INTEREST RATE = 0.0442
# FOR WHATEVER REASON 0.2 is COMMONLY USED

# T = The Days to Expire / 365 (1 YEAR = 365 DAYS)
# S0 = The Spot Price
# K = The Strike Price
# r = The Risk Free Interest Rate
# u = The Up Factor
# d = The Down Factor

T = 10 # Number of periods
S0 = 8 # Starting price of stock
K = 9 # Strike price of option
r = 0.2 # Risk free interest rate


u = 1.5 # Up factor
d = 0.5 # Down factor

C = 0

q = ((1+r) - d) / (u - d)
risk_free = 1 / ((1 + r)**T)

for i in range(0, T+1):
    prob = math.comb(T, i) * (q**i) * (1-q)**(T-i)
    ST = (u**i) * (d**(T-i)) * S0
    max_value = max(ST - K, 0)
    C += max_value * prob

print(C * risk_free)




# Binomial Tree
tree = [[S0]]
for i in range(1, T+1):
    level = []
    for j in range(i+1):
        price = S0 * (u**(i-j)) * (d**j)
        level.append(price)
    tree.append(level)

# Binomial Option Pricing Method
option_price = 0
for i in range(T, -1, -1):
    for j in range(i+1):
        if i == T:
            option_price = max(tree[i][j] - K, 0)
        else:
            option_price = (q * option_price + (1 - q) * option_price) / (1 + r)
print(option_price)