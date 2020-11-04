
# Empty sum variable
total = 0

# Use loop to accumulate 1 to 100
for num in range(101):
    total = total + num

# Print out the result
print('1 + 2 + 3 + ... + 100 =',total)

# Use for loop through the list from 1 to 21
for i in range(1, 21):

    # use modulus to check that the result is equal to 0 or not
    if (i % 2) != 0:

        # print the odds
        print('i=',i)