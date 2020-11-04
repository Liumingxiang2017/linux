

class Animal(object):

	def test1(self):
		self.a = 10
		self.__b = 11
		print(self.a)
		print(self.__b)

	def __test3(self):
		self.a = 100
		self.__b = 110
		print(self.a)
		print(self.__b)

	def test4(self):
		#判断用户的密码
		#判断用户的权限
		self.__test3()



class Dog(Animal):
	def test2(self):
		print(self.__b)

	def test5()
		self.__test3()

aa = Animal()
aa.test1()

#aa.__test3()
aa.test4()

print('-------分隔线--------')


dd = Dog()
dd.test1() #如果是通过继承的方法访问父类的私有属性是可以的

#dd.test2() #如果是在子类中，自定义一个方法，此方法不能访问父类

#dd.test5()
