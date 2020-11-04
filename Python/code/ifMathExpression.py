# ------------ CALCULATOR ----------
# Receive 2 numbers separated by an operator and show a result
# Sample
# Enter Calculation: 5 * 6
# 5 * 6 = 30

# Store the user input of 2 numbers and the operator
num1, operator, num2 = input('Enter calculation: ').split()

# Convert the strings into integers
num1 = int(num1)
num2 = int(num2)

# if + then we need to provide output based on addition
# Print the result
# If, else if (elif) and else execute different code 
# depending on a condition
if operator == '+':
    print('{} + {} = {}'.format(num1, num2, num1+num2))

# If the 1st condition wasn't true check if this one is 
elif operator == '-':
    print('{} - {} = {}'.format(num1, num2, num1-num2))
elif operator == '*':
    print('{} * {} = {}'.format(num1, num2, num1*num2))
elif operator == '/':
    print('{} / {} = {}'.format(num1, num2, num1/num2))

# If none of the above condition were true then execute this by default

else:
    print("Use either + - * or / next time")
