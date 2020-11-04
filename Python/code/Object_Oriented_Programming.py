

class ClassName(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg


#类名使用大驼峰，创建一个类
class Dog:

	#定义一个init方法,自动调用

	def __init__(self,newName,newWeight,newColor):
		self.weight = newWeight
		self.color = newColor
		self.name = newName

	#print对象时，打印的内容
	def __str__(self):
		return "哈哈哈，我是小狗..."

	def bark(self):
		print("汪汪汪...")

	def run(self):
		print("狗在疯狂的跑...")

	def eat(self):
		print("吃东西...")
		
		#在方法中，可以对属性进行修改
		self.weight += 5

	def printName(self):
		print("名字是：%s"%self.name)

#定义一个函数
def test(temp):
	temp.printName()

#创建一个对象
xiaogou = Dog('大白',5,'黄色')

test(xiaogou)

print('_'*50)
print(xiaogou)
print('_'*50)
#xiaogou.printName()

'''
#调用对象的一个方法
xiaogou.bark()
xiaogou.run()

#添加属性
xiaogou.weight = 5
xiaogou.color = '黄颜色'
'''

'''
#获取对象的属性
print(xiaogou.weight)
print(xiaogou.color)

#调用eat方法，这个方法会对weight这个属性进行修改
xiaogou.eat()
print(xiaogou.weight)

#验证能否直接修改属性
xiaogou.weight += 5
print(xiaogou.weight)
'''
wangcai = Dog('小黑',10,'黑色')
#wangcai.printName()
#print(wangcai.weight)
#print(wangcai.color)

test(wangcai)










