# python

进阶篇承上启下

为什么要使用方法？

合理的抽象，可复用性

	如果程序里，并不是多次用到同一种解决方案，我们就不需要将这个解决方案，我们就不需要将这个解决方案封装起来。

语句即逻辑，结构即存储

步骤其实就是伪代码

	geturl http://www.126.com

	获取数据 urllib2

		访问网页 

			访问不成功做一个log

 			访问成功 进入下一步流程

	分析数据 正则 和beautifulsoup

	入库 储存到文本或者数据库

数据结构

	考虑清楚数据的结构

	dict

	list

	tuple



virtualenv

python开发的沙盒环境，适合多项目并行管理。

安装及使用：

- sudo pip install virtualenv
- virtualenv test1
- virtualenv test2
- cd test 2
- source bin/activate  激活沙盒
- sudo pip install tornado 沙盒环境安装需要的程序

推荐参考书

基础知识

- 程序员的数学（初中水平）
- 大话数据结构（数据结构）大话设计模式 
- C语言  （相关的都行）

python方面

- python标准库
- python基础教程
- docs.python.org
- 啄木鸟社区的邮件列表

边界检查
	在程序设计中是指在使用某一个变量前，用来检查该变量是否处在一个特定范围之内的过程。



进阶篇函数第一节

函数

    def func_name():
    	pass


# *num将参数转换为一个tuple
def add(*num):
    d = 0
    for i in num:
        d += i
    return d
print add(1,2,3,4,5)
    

参数分必选参数和可选参数

必选参数 是没有默认值的
	有默认值和没有默认值得区别在于“=”

可选参数 是有默认值的，可以避免重复设定。
	var1 = None


可维护性健壮性：考虑到一些误操作。

def add(num1,num2):
    if isinstance(num1,int) and isinstance(num2,int):
        return num1+num2
    else:
        return '参数中有非数字类型'
print add('a',(1,2,3))
print add(1,2)


#断言是程序中常用的测试方法，是否返回了想要的结果。
assert add(1,2) == 3

