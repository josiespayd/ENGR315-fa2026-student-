"""
This problem requires you to calculate compounding interest and final value of a  US treasury deposit based upon
current interest rates (that will be provided). Your analysis should return the final value of the investment
after a 10-year and 20-year period. The final values should be stored in the variables "ten_year_final"
and "twenty_year_final", respectively. Perform all your calculations in this file. Do not perform the calculations by hand
and simply write in the final result.

Prompt: On October 27th, 2022, Elon Musk purchased Twitter for $44B in total, with reportedly $33B of his own money. Since
that time, it appears this investment has not worked out. If Elon has instead bought $33B of US Treasury Bonds, how much
would his investment be worth in 10-year and 20-year bonds? Assume the 10-year bonds pay 3.96%,
the 20-year bonds pay 4.32%, with each compounding annually.
Note that Elon's capital will be $33B.
"""

### all your code below ###

## Given values
capital = 33000000000 

## 10-year investment claculation
rate_10 = 3.96/100
years_10 = 10
ten_year_final = capital*((1 + rate_10)**years_10)

## 20-year investment calculation
rate_20 = 4.32/100
years_20 = 20
twenty_year_final = capital*((1 + rate_20)**years_20)

## Check values
print(ten_year_final)
print(twenty_year_final)
