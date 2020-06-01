# Calculate pi to 100+ decimal places

from bs4 import BeautifulSoup
from decimal import Decimal, getcontext
import requests
import time

getcontext().prec = 100

# Get pi from the internet
url = "https://www.piday.org/million/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
full_pi = str(soup.findAll("div")[7])
full_pi = full_pi.split('id="million_pi">')[-1].split("</div>")[0]

start = time.time()

# Calculate pi
taylor_terms = 10000000
print("Calculating pi using a series approximation with {} terms".format(taylor_terms))

## utilize arctan(1) = pi / 4, so get series approximation of arctan(1)
## -  arctan(x) = x - x^3/3 + x^5/5 - ...
arctan_1 = Decimal(0)
denom_int = 1
for term_index in range(taylor_terms):
    if term_index % 2 == 0:
        arctan_1 += Decimal(1) / Decimal(denom_int)
    else:
        arctan_1 -= Decimal(1) / Decimal(denom_int)
    denom_int += 2

#Sadly, this method is slower and less accurate
"""
even_terms = [Decimal(1) / Decimal(x) for x in range(1, taylor_terms * 4, 4)]
odd_terms = [Decimal(-1) / Decimal(x) for x in range(3, taylor_terms * 4, 4)]
arctan_1 = sum(even_terms) + sum(odd_terms)
"""

pi = Decimal(4) * arctan_1
result = str(pi)

end = time.time()
print("Runtime: {:.2f} seconds".format(end - start))

# Determine the decimal place where we become inaccurate
found_inaccuracy = False
for place, (full_pi_digit, result_digit) in enumerate(zip(full_pi, result)):
    if full_pi_digit != result_digit:
        print("Accurate to {} decimal places.".format(place))
        found_inaccuracy = True
        break


if not found_inaccuracy:
    print("Accurate to more than {} decimal places.".format(place))

