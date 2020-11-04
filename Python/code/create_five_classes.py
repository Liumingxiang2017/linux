
#全局变量，保存马的数量，能不用就不用
g_horse_num = 0

class Animal(object):
	"""docstring for Animal"""
	def __init__(self, name = '动物', color = '白色'):
		self.name = name
		self.color = color

		self.setHorseNum()

class Horse(Animal):

	horseNum =  0 #类属性，类里面方法外面，跟着类走

	def __init__(self, name, color = ''):
		super().__init__(name)
		self.name = '我的'+name

		self.horseNum +=1 #实例属性，跟着对象走

	@classmethod
	def setHorseNum(cls):
		cls.horseNum += 1

print('------**-----')
bailongma = Horse('白龙马')
#bailongma.setHorseNum()
print(Horse.horseNum)
print('------**-----')

g_horse_num += 1
print(g_horse_num)

print(bailongma.name)
print(bailongma.color)

#Horse.horseNum += 1
#print(Horse.horseNum)

print('------**-----')
chituma = Horse('赤兔马')
#chituma.setHorseNum()
print(Horse.horseNum)
print('------**-----')

#g_horse_num += 1
#print(g_horse_num)

print(chituma.name)
print(chituma.color)

Horse.horseNum += 1
print(Horse.horseNum)