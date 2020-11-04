#coding=utf-8

a = {'key1':'value1', 'key2':'value2'}
print a

for x,y in a.item():
    print x,y

#列表排序
a = {'a':'haha', 'b':'xixi', 'd':'qiqi', 'c':'xiaxia'}

key_list = a.keys()

#list是可变数据对象，所以它支持原地修改，不需要复制给新的list
key_list.sort()

for x in key_list:
	print x,a[x]

'''

1.根据字典的值得到字典的键
2.字典索引的是键，而不是值->迭代，穷举
3.一个值可能对应n（n>1）个键

'''

a = {'a':'haha', 'b':'xixi', 'd':'qiqi', 'c':'xiaxia', 'e':'haha'}

search_value = 'haha'

key_list = []

for x,y in a.items():
	if y == search_value:
		key_list.append(x)

print key_list[0]

'''
Python list内置sort()方法用来排序，也可以用python内置的全局sorted()方法来对可迭代的序列排序生成新的序列。

sorted(iterable,key=None,reverse=False)，返回新的列表，对所有可迭代的对象均有效

sort(key=None,reverse=False) 就地改变列表  reverse：True反序；False 正序

'''


a = 'i am lilei'

print a.replace('lilei','hanmeimei')


#好玩的translate与maketrans；

import string
a = 'i am lilei'
#maketrans翻译表参数长度要相同，一一对应替换
c = string.maketrans('i','I')
#第一个参数是参数表，第二个参数是删除的字符
print a.translate(c,'lilei')

#新的语句，with

g = open('a.txt','w')
g.write('hah\nhahaaaaaa')
g.close()
#'a'即'append'
with open('a.txt','a') as g:
	g.wirte('xixixixi')