# --------------PROBLEM : Dollar To RMB--------------
# Dollar currency rate is 6.74, ￥ = $ * 6.74
# Enter $5, $5 equals ￥33.7

# Ask the user to input $ and assign it to the $ variable
dollar = input("Enter dollars: ")
 
# Convert from string to integer
dollar = int(dollar)

# Perform calculation by multiplying 6.74 times $
CNY = dollar * 6.74

# Print results using format()
print("{} dollars equals {} Yuan".format(dollar, CNY))
