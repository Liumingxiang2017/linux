
#如果有(object)叫做 新式类
#原来的那种没有的叫做 经典类
class Person(object):
	"""docstring for Person"""
	def __init__(self, name, age):
		#self.name = name
		self.__name = name #私有属性
		#self.age = age
		self.__age = age
		self.high = 180 #公有属性
	def __str__(self):
		return '年龄为: ' + str(self.__age)

	def setNewAge(self, newAge):
		if newAge>0 and newAge<80:
			self.__age = newAge

	def getAge(self):

		return self.__age

xiaoming = Person('xiaoming', 18)

#print(xiaoming.age)

#print(xiaoming.age)
print(xiaoming)
xiaoming.setNewAge(119)
print(xiaoming)
ageTemp = xiaoming.getAge()
print(ageTemp)