# ------ PROBLEM : COMPOUNDING INTEREST ------

# Have the user enter their investment amout and interest rate
# Each year : investment + investment * interest rate
# Print out the earning after a 10 year period

# Ask for the money invested and the interest rate
money = input("How much to invest: ")
interest_rate = input('Interest Rate: ')

# Convert the value to a float
money = float(money)

# Convert value to a float and round the percentage rate by 2 digits
interest_rate = float(interest_rate) * 0.01

# Cycle through 10 years using a for loop and range from 0 to 9
for i in range(10):

# Add the current money in the account + interest earned that year
    money = money + money * interest_rate

# Output the results
print("Investment after 10 years: {:.2f}".format(money))