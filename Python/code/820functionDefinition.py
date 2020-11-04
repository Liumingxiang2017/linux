# ------- FUNCTION BASICS --------

def allotEmail(firstName, surname):
    return firstName+'.'+surname+'@pythonabc.org'

name = input("Enter your name: ")
fName, sName = name.split()
compEmail = allotEmail(fName, sName)

print(compEmail)


def get_sum(*args):
    sum = 0
    for i in args:
        sum += i
    return sum
print("sum =", get_sum(3,4,5,7))