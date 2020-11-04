# ---------- IS BIRTHDAY IMPORTANT ----------
# We'll provide different output based on age
# 1 - 18 --> Important
# 50, 60, >65 --> Important
# All others --> Not important

# Receive age and store in age

# Convert a string into an integer
age = int(input("Enter age: "))

# If age is both greater than or equal to 1 and less than or equal to 18 Important
if (age >= 1) and (age <= 18):
    print("Important Birthday")

# If age is either 50 or 60 Important
elif (age == 50) or (age == 60):
    print("Import Birthday")
# We check if age is lee than 65 and then convert true to false and vice verse
# This is the same as if we put age > 65
elif not(age <= 65):
    print("Important Birthday")
# Else not important
else:
    print("Sorry Not Important")
