#break/continue must be used in loop
#break/continue only work in the nearest loop

name = "python"

for temp in name:
	if temp=="h":
		break
	print(temp)
print("it is a break demo")
for temp in name:
	if temp=="h":
		continue
	print(temp)
print("it is a continue demo")
