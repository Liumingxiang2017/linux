
class Animal(object):
	"""docstring for Animal"""
	def bark(self):
		print('啊啊啊啊啊')

class Cat(object):
	"""docstring for Cat"""
	def bark(self):
		print('喵喵喵')

class Dog(object):
	"""docstring for Dog"""
	def bark(self):
		print('汪汪汪。。。')

#所谓的多态是指，调用的方法是同一个，但是执行的代码或者说现象不一样

class Robot(object):
	"""docstring for Robot"""
	def bark(self):
		print('嗡嗡嗡')

def animalBark(temp):
	temp.bark()

maomi = Cat()
wangcai = Dog()

animalBark(maomi)
animalBark(wangcai)

dingdang = Robot()
animalBark(dingdang)