
class SweetPotato:

	#初始化，用来设置默认的属性
	def __init__(self):

		'这是烤地瓜的类'

		self.cookedLevel = 0
		self.cookedString = "生的"
		self.condiments = []

	#定制print打印这个对象的时候，显示的内容
	def __str__(self):

		#msg = '您的地瓜已经处于xxx状态，已经添加的佐料为xxxx'

		msg = '您的🍠地瓜已经处于' + self.cookedString + '的状态' 
		
		if len(self.condiments)>0:
			msg += '，添加的佐料为'

			for temp in self.condiments:
				msg += temp + ', '
			msg = msg.strip(', ')

		return msg

	#用火烤地瓜
	def cook(self,time):
		
		self.cookedLevel += time

		if self.cookedLevel>8:
			self.cookedString = '烤糊了'
		elif self.cookedLevel>6:
			self.cookedString = '熟了'
		elif self.cookedLevel>3:
			self.cookedString = '半生不熟'
		else:
			self.cookedString = '生的'

	def addCondiments(self,temp):
		self.condiments.append(temp)

#创建一个地瓜对象

digua = SweetPotato()
print(digua)

'''
print(digua.cookedLevel)
print(digua.cookedString)
print(digua.condiments)
'''
print('____________接下来开始烤地瓜——————————————')

print('----烤2分钟----')
digua.cook(2)
#print(digua.cookedString)
print(digua)

print('----又烤2分钟----')
digua.cook(2)
#print(digua.cookedString)
print(digua)

print('---添加番茄酱---')
digua.addCondiments('🍅番茄酱')
print(digua)

print('---添加芥末酱---')
digua.addCondiments('芥末酱')
print(digua)

print('----又烤2分钟----')
digua.cook(3)
#print(digua.cookedString)
print(digua)


'''
总结：
禁止使用对象直接修改属性
应该使用方法修改属性，等于隐藏了数据
'''

