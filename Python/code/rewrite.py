
#重写父类方法
#重写，就是子类中，有一个和父类相同名字的方法，在子类中的方法会覆盖父类中同名的方法

class Animal(object):
	"""docstring for Animal"""
	def bark(self):
		print('啊啊啊啊啊啊。。。。')

class Cat(Animal):
	#在子类中重新编写这个方法，就叫做重写
	def  bark(self):
		#调用父类的这个方法bark

		Animal.bark(self)
		
		super().bark()

		print('喵喵喵。。。')

tom = Cat()

tom.bark()
		