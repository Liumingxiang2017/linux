# A prime can only be divided by 1 and itself
# 5 is prime because 1 and 5 are its only positive factors
# 6 is a composite because it is divisible by 1 2 3 and 6

def isprime(num):

    for i in range(2, num):
        if (num%i) == 0:
            return False

    return True