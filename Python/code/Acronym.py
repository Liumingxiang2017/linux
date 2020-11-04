# ---------- PROBLEM : ACRONYM GENERATOR ----------
# You will enter a string and then convert it to an acronym
# with upper letters like this
'''
Convert to Acronym : Random Access Memory
'''

# Ask for a string
str = input("Convert to Acronym : ")

# Convert the string to all uppercase
str = str.upper()

# Convert the string into a list
listOfWords = str.split()

# Cycle through the list
for word in listOfWords:


# Print the 1st letter of the word
    print(word[0], end='')