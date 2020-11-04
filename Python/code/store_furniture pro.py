
#定义一个 home家 类
class Home:

	def __init__(self,area):
		self.area = area
		self.rongNaList = []
		#灯的默认状态为 off
		self.light = 'off'

	def __str__(self):
		msg = '家当前可用的面积为：' + str(self.area) + '; 灯的状态为：' + self.light

		if len(self.rongNaList)>0:

			msg += ' ;当前有 ： '

			for temp in self.rongNaList:
				msg += temp.getBedName() + ', '

			msg = msg.strip(', ')

		return msg

	def containItem(self,item):

		#API application programming interface 应用编程接口
		bedArea = item.getBedArea()
		if self.area > bedArea:
			self.rongNaList.append(item)
			self.area -= bedArea
			print('当前添加%s成功....家当前可用面积为：%d'%(item.getBedName(),self.area))
		else:
			print('error:当前%s需要的面积大于家可用面积'%item.getBedName())

	def turnOn(self):
		#把家里的灯打开了
		self.light = 'on'
		#把家里所有的家具都变为亮的状态
		for temp in self.rongNaList:
			temp.setLight()

#定义一个 bed床 类
class Bed:

	def __init__(self,name,area):
		self.area = area
		self.name = name
		self.light = 'off'

	def __str__(self):
		msg = self.name + '床占用的面积为：' + str(self.area) + '; 当前明暗为：' + self.light
		return msg

	def getBedArea(self):
		return self.area

	def getBedName(self):
		return self.name

	def setLight(self):
		self.light = 'on'

	def setLightOff(self):
		self.light = 'off'

home = Home(180)
print(home)

bed = Bed('席梦思床',4)
print(bed)

home.containItem(bed)
print(home)

bed2 = Bed('木板床',10)
home.containItem(bed2)
print(home)

bed3 = Bed('超级大的床', 170)
home.containItem(bed3)
print(home)

home.turnOn()

print(home)
print(bed)
print(bed2)
print(bed3)
#home.turnOff()