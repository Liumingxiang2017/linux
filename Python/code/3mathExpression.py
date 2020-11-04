# -------------MATH ON 2 VALUES-------------
# input: 5 4
# output: 
# 5 + 4 = 9
# 5 - 4 = 9
# 5 * 4 = 20
# 5 / 4 = 1.25
# 5 % 4 = 1

# Ask the user to input 2 values and store them in variables num1 num2
# split() splits input using whitespace
num1, num2 = input('Enter 2 numbers').split()

# Convert the string into regular numbers Integer
num1 = int(num1)
num2 = int(num2)

# Add the values enterd and store in sum
sum = num1 + num2

# Subtract the values entered and store in difference
difference = num1 - num2

# Multiply the values entered and store in product
product = num1 * num2

# Divide the values entered and store in quotient
quotient = num1 / num2

# Use modulus on the values to find the remainder
remainder = num1 % num2

# Print the results
# format() loads the variable values in order into the {} placeholders
print("{} + {} = {}".format(num1, num2, sum))
print("{} - {} = {}".format(num1, num2, difference))
print("{} * {} = {}".format(num1, num2, product))
print("{} / {} = {}".format(num1, num2, quotient))
print("{} % {} = {}".format(num1, num2, remainder))
