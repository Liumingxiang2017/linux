# ---------- PROBLEM : SECRET STRING ----------
# Receive a uppercase string and then hide its meaning by turning it into a string of unicode
# Then translate it from unicode back into its original meaning

# Enter a string to hide in uppercase
# Secret Message : 34567890
# Original Message : HIDE

# Input string to be encrypted
orig_message = input("Enter a string in uppercase :")

secret_message = ''

# cycle through each character in the string
for char in orig_message:

# store each character code in secret message
    if char.isalpha():
        secret_message += str(ord(char)-23)
    elif char.isspace():
        secret_message += str(ord(char))

# Print "Secret message: 98989099"
print("Secret message: ", secret_message)

# Cycle through each character code 2 at a time
norm_string = ''

for i in range(0, len(secret_message)-1, 2):

# Convert the code into characters and add them to the string
    char_code = secret_message[i] + secret_message[i+1]
    if char_code != '32':
        norm_string += chr(int(char_code) + 23)
    else:
        norm_string += chr(int(char_code))

# Print the string
print("Original message : ", norm_string)