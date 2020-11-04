#a=4为函数默认值
def test1(a=4):
	return a

print test1()


#**猩猩是字典, *是元祖

def test(**kr):
	return kr

print test(a=1,b=2)


def test2(*z):
	return z

print test2(11,22,[1,2,3])


def test(*z,**kr):
	return z,kr

print test(11,22,[1,2,3],a=1,b=2)