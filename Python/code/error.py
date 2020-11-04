
#捕获异常
try:
	print('----test1------')
	open('123.txt','r')
	print('-----test2-----')
except IOError:
	print('亲，您要的文件不存在')

print('*'*50)

try:
	print(num)
except (IOError,NameError) as errMsg:
	print('[2018-03-25 22:22:22]')
	print(errMsg)

'''
try:
	#可能出现的异常代码
	pass
except （exception1, exception2, exception3） as erroMsg:
	#如果出现了异常，会执行的代码
	pass
else:
	#没有出现异常执行的代码
	pass
finally:
	#不管是否出现异常，都会被执行
	pass
'''



#抛出异常

class ShortInputException(Exception):
	'''你定义的异常类'''
	def __init__(self, length, atleast):
		Exception.__init__(self)
		self.length = length
		self.atleast = atleast
try:

	s = input('请输入 ---》')

	if len(s) < 3:
		#raise引发一个你定义的异常
		raise ShortInputException(len(s), 3)

except EOFError:
	print('你输入了一个结束标记EOF')

except ShortInputException as x: #x这个变量被绑定到了错误的实例
	print('ShortInputException: 输入的长度是 %d, 长度至少是 %d'%(x.length, x.atleast))
else:
	print('没有异常发生')
finally:
	print('**************************')


