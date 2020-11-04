
class People(object):
	address = '山东' #类属性

	#实例方法
	def __init__(self):
		self.name = 'xiaowang' #实例属性
		self.age = 20 #实例属性

	#类方法
	@classmethod
	def setNewAddress(cls):
		cls.address = '盐城'
#可以通过类名的方法获取类属性，但是不能通过类名获取实例属性
print(People.address)

#类对象，可以直接调用类属性，也可以直接调用类方法
#但是类对象不允许调用实例属性，并且也不允许调用实例方法
#如果是一个实例对象，可以获取实例属性和类属性的值，但是只能修改实例属性，不能修改类属性
#它还可以调用实例方法和类方法
print('--$$$$----')
xiaoming = People()

xiaoming.setNewAddress()
print(People.address)
print('---$$$$--------')
#类属性不允许通过实例属性直接修改，实际是定义了一个实例属性
xiaoming.address = '河北'
print(xiaoming.address)

print(People.address)
print('------------')
#类外修改，不安全，通过类方法来修改
People.address = '阜宁'
print(People.address)

#通过类方法来修改
print('------------')
People.setNewAddress()
print(People.address)