def isprime(num):
    for i in range(2, num):
        if (num % i) == 0:
            return False

    return True

def getPrimes(numMax):

    primes = []

    for num1 in range(2, numMax):

        if isprime(num1):
            primes.append(num1)
    return primes

maxNum = int(input("Search for primes up to: "))

listOfPrimes = getPrimes(maxNum)

for prime in listOfPrimes:
    print(prime, end=', ')