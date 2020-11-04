# ---------- MORE LIST FUNCTION ----------
import random
numList = []
for i in range(5):
    numList.append(random.randrange(1,9))

print(numList)

numList.sort()
print(numList)

l = numList.sort()
print(l)

numList.sort(reverse = True)
print(numList)

numList.reverse()
print(numList)

numList.insert(4, 10)
print(numList)

numList.remove(10)
print(numList)

numList.pop(2)
print(numList)

print("*"*20)
numList2 = []
for i in range(5):
    numList2.append(random.randrange(1,9))
print(sorted(numList2))
print(numList2)

print(sorted(numList2, reverse = True))

PI = 3.14

tup = (9,2,1,3,4,7,3)

print(tup)
print(max(tup))
s_tup = sorted(tup)
print(s_tup)

student = ["Tom", "Jerry", "guojing"]
print(random.choice(student))

nList = [i*2 for i in range(10)]
print(nList)

numList3 = [1,2,3,4,5]
pList = [pow(i, 2) for i in numList3]
print(pList)

listOfValue = [[pow(i, 2), pow(i, 3), pow(i, 4)] for i in numList3]

for k in listOfValue:
    print(k)

print("hope" * 3)
print([0] * 10)
multiDlist = [[i]*10 for i in range(10)]
for k in multiDlist:
    print(k)

# ------ MULTIDEMENSIONAL LIST ------
listTable = [[0]*10 for i in range(10)]
for i in range(1,10):
    for j in range(1,10):
        listTable[i][j] = "{} : {}".format(i,j)
        print(listTable[i][j], end="   ")
    print()
