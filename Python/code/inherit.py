

class Animal(object):

	#初始化的事情
	def __init__(self, name = '动物', color = 'white'):
		#self.__name = name 私有属性不会被继承，所有要用公有属性
		#self.__color = color 
		self.name = name
		self.color = color

	#临死之前要做的事情
	def __del__(self):
		print('-----啊。。。。-----')

class Dog(Animal):

	#初始化的事情
	#def __init__(self, name = '狗', color = 'white'):
	#	self.__name = name
	#	self.__color = color

	#临死之前要做的事情
	#def __del__(self):
	#	print('-----啊。。。。-----')

	def  printInfo(self):
		#print('颜色是： %s'%self.__color) 私有属性不能被继承，所以不能直接使用
		#print('名字是： %s'%self.__name)
		print('颜色是： %s'%self.color)
		print('名字是： %s'%self.name)

wangcai = Dog(name = 'wangcai')
wangcai.printInfo()
