# ------- SORT A LIST : BUBBLE SORT ---------
import random

# create a list by random generate
numList = []
M = 10
for i in range(M):
    numList.append(random.randrange(1,10))

print(numList)

# define a variable to identify the last index and decrement for the outer loop
i = len(numList) - 1

while i > 0:

    # define a variable to identify the inner loop and compare adjacent elements
    j = 0

    # inner loop to compare and switch adjacent elements
    while j < i:

        # if the value on the left is bigger, then switch
        if numList[j] > numList[j+1]:
            numList[j], numList[j+1] = numList[j+1], numList[j]

        # increment the inner loop control variable
        j += 1

    # Identify the end of one round
    for k in numList:
        print(k, end=", ")
    print()

    # decrement the outer loop control variable
    i -= 1
