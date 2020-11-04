# ----------- STRING METHODS ---------

# Strings have many methods we can use beyond what I covered last time
rand_string = '   life is a beautiful struggle   '

# Delete whitespace on left
rand_string = rand_string.lstrip()

# Delete whitespace on right
rand_string = rand_string.rstrip()

# Delete whitespace on right and left
rand_string = rand_string.strip()

# Capitalize the 1st letter
print(rand_string.capitalize())

# Capitalize the every letter
print(rand_string.upper())

# lowercase all letters
print(rand_string.lower())

# Turn a list into a string and separate items with the defined
# separator
a_list = ["Bunch", "of", "random", "words"]
print(" ".join(a_list))

# Convert a string into a list
a_list_2 = rand_string.split()

print(a_list_2)

for i in a_list_2:
    print(i)

# Count how many times a string occurs in a string
print("How many is :", rand_string.count("if"))

# Get index of matching string
print("Where is 'is' :", rand_string.find("is"))

# Replace a substring
print(rand_string.replace("struggle", "journey"))

# For our next problem some additional string methods
# very useful

letter_z = "z"
num_3 = "3"
a_space = " "

# Returns True if characters are letters or numbers
# Whitespace is false
print("Is z a letter or number :", letter_z.isalnum())

# Returns True if characters are letters
print("Is z a letter :", letter_z.isalpha())

# Returns True if characters are numbers(Floats are false)
print("Is 3 a number :", num_3.isdigit())

# Returns True if all are lowercase
print("Is z a lowercase :", letter_z.islower())

# Returns True if all are uppercase
print("Is z a uppercase :", letter_z.isupper())

# Returns True if all are spaces
print("Is space a space :", a_space.isspace())
