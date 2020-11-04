
class Base(object):
	"""docstring for Base"""
	def test(self):
		print('-----Base test-----')
		
class A(Base):
	"""docstring for A"""
	def testA(self):
		print('-----A test-----')

	def test2(self):
		print('-----testA test-----')


class B(Base):
	def testB(self):
		print('-----B test-----')

	def test3(self):
		print('-----testB test-----')


class C(A, B):
	"""docstring for C"""
	pass

c = C()
c.testA()
c.testB()
c.test()


print(C.__mro__) #类的遍历顺序 

#广度遍历 把兄弟节点找一次