
randList = ["string", 1.234, 28]
print(randList)

# list[start:end:step]

oneToTen = list(range(11))
print(oneToTen)

randList = randList + oneToTen
print(randList)

print(randList[0])

print("List Length :", len(randList))

first3 = randList[0:3]

print("string" in first3)

print("Index of string: ", first3.index("string"))

for i in first3:
    print("{} : {}".format(first3.index(i), i))

print("How many string :", first3.count("string"))

first3[0] = "New String"
for i in first3:
    print("{} : {}".format(first3.index(i), i))
print(first3)

first3.append("Another")
for i in first3:
    print("{} : {}".format(first3.index(i), i))