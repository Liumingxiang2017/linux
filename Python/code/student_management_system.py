#coding=utf-8

# 1.先把整体的框架考虑清楚


def showInfo():
	print("_"*30)
	print("    学生管理系统 v1.0")
	print(" 1:添加学生的信息")
	print(" 2:删除学生的信息")
	print(" 3:修改学生的信息")
	print(" 4:查询学生的信息")
	print(" 5:遍历所有学生的信息")
	print(" 6:退出系统")
	print("_"*30)

def addNewStu(studentsTemp):
	#完成添加学生信息的功能
	#stuInfo = {"name":xxx,"id":100,"age":20}
	#[{},{},{}]
    
    name = input("请输入姓名：")
    stuId = input("请输入学号：")
    age = input("请输入年龄：")

    #只要有一个字典，并且这个字典中已经准备好数据的话，那么就可以添加
    stuInfo = {}
    stuInfo['name'] = name
    stuInfo['id'] = stuId
    stuInfo['age'] = age

    studentsTemp.append(stuInfo)

def delStuInfo(students):
	delNum = int(input("请输入要删除的序号"))

	del students[delNum]

#定义一个列表用来存储多个学生的信息
students = []

while True:

	# 1.0 先把功能列表显示给用户
	showInfo()

	# 1.1 提示用户选择功能
	# 1.2 获取用户选择的功能
	key = int(input("请选择功能（序号）："))

	# 1.3 根据用户的选择，执行相应的功能
	if key == 1:
		addNewStu(students)

	elif key == 2:
		delStuInfo()
		
	elif key == 3:
		pass
	elif key == 4:
		pass
	elif key == 5:
		
		print("*"*20)
		print("接下来遍历所有学生的信息....")

		print("id   姓名   年龄")
		for temp in students:
			print("%s   %s   %s"%(temp['id'],temp['name'],temp['age']))
	elif key == 6:
		quitConfirm = input("亲，真的要退出吗(yes or no)？")
		if quitConfirm == 'yes':
			break
	else:
		print("输入有误，请重新输入")