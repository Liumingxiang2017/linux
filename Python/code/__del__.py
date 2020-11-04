

class Animal(object):

	#初始化的事情
	def __init__(self,name):
		self.__name = name

	#临死之前要做的事情
	def __del__(self):
		print('-----啊。。。。-----')

dog = Animal('旺财')

print('-----1-----')

dog1 = dog
dog2 = dog

print(id(dog))
print(id(dog1))
print(id(dog2))



print('-----2-----')

del dog
del dog1
del dog2

print('-----3-----')

#虽然没有调用__del__方法，那是谁调用的呢？
#python解释器，如果检测到一个对象没有任何用处，那么就把这个对象kill掉