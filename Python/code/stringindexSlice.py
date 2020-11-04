samp_string = 'Whatever you are, be a good one.'

# You can get a character by referencing an index
print(samp_string[0])

# get the last character
print(samp_string[-1])

# get the string length
print('Length : ', len(samp_string))

# Get a slice by saying where to start and end
# The 4th index isn't returned
print(samp_string[0:4])

# Get everything starting at an index
print(samp_string[8:])
print()

print(samp_string)
print(samp_string[::])
print(samp_string[::2])

# Reverse the string
print(samp_string[::-1])
# Palindrome
print('I did, did I?'[::-1])
print('No lenmon, no melon'[::-1])

# Practical use
url = "http://pythonabc.org"
# Get the top level domain
print(url[-4:])
# Print the url without the http://
print(url[7:])
# Print the url without the http:// or the top level domain
print(url[7:-4])

# Cycle through each character with for
for char in samp_string:
    print(char)

# Cycle through charcters in pairs
# 这一段程序只对长度为偶数的有效，要程序更有包容性，可用的方法之一是分类讨论。
for i in range(0, len(samp_string)-1, 2):
    print(samp_string[i] + samp_string[i+1])

# Join or concatenate strings with +
print('Green' + 'egg')

# Repeat string with *
print("Hello" * 5)

# Convert an int into a string
num_string = str(4)

# Computers assign characters with a number known as a Unicode
# A - Z 65 - 90
# a - z 97 - 122

# You can get the Unicode with ord()
print("A =", ord("A"))

# You can convert from Unicode with chr()
print("65 = ", chr(65))

print("桃 = ", ord("桃"))
print("26691 = ", chr(26691))