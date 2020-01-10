# Vim编辑器

Vim: Visual Interface iMproved

文本编辑器，全屏编辑器，模式化编辑器，字处理器，ASCII

nano，sed

## Vim模式

- 命令模式(Command Mode)：  控制光标移动，删除- 符，段落复制。
- 输入模式(Insert Mode)：   新增文字及修改文字。
- 末行模式(Last Line Mode)：保存文件，离开vi，- 及其他设置。

## 模式转换：

命令-->输入：

	i: 在当前光标所在字符的前面，转为输入模式；
	a: 在当前光标所在字符的后面，转为输入模式；
	o: 在当前光标所在行的下方，新建一行，并转为输入模式；
	
	I：在当前光标所在行的行首，转换为输入模式
	A：在当前光标所在行的行尾，转换为输入模式
	O：在当前光标所在行的上方，新建一行，并转为输入模式；

输入-->命令：ESC

命令-->末行：：

末行-->命令：ESC, ESC


vi -o file1 file2 同时打开2个文件，横排

vi -O file1 file2 同时打开2个文件，竖排

ctrl+ww 切换窗口

## 配置文件

 ~/.vimrc 

- 显示行号 set nu
- 关闭语法 syn off
- 创建快捷键 map ^P i#\<ESC>
- 注释是双引号"

## 命令模式命令

命令  |  说明
-|:-:
 h    |  将光标向左移动一格
 l    |  将光标向右移动一格
 j    |  将光标向下移动一格
 k    |  将光标向上移动一格
 0    |  数字0，将光标移动到该行的行首
 $    |  将光标移动到该行的行末
 H    |  将光标移动到该屏幕的顶端
 M    |  将光标移动到该屏幕的中间
 L    |  将光标移动到该屏幕的底端
 gg   |  将光标移动到文章的首行
 G    |  将光标移动到文章的尾行
 nG   |  将光标移动到第n行
w或W  |  将光标移动到下一单词
 x    |  删除光标所在处的字符
 X    |  删除光标前的字符
 dd   |  删除光标所在行
ndd   |  从光标所在行向下删除n行，为数字
dG    |  删除光标所在行到末尾
 D    |  删除光标所在处到行尾
 r    |  取代光标处的一个字符
 R    |  从光标处向后替换，按Esc结束
 u    |  取消上步的操作
 U    |  取消目前的所有操作
 yy，Y   |  复制光标所在行
 nyy，nY |  复制光标所在行以下n行
 p    |  将复制或者删除的内容放在光标所在行的下行
 s|替换光标所在处字符，并进入文本输入方式
 S|替换光标所在全行，按ESC结束
 u|取消上一步操作，取消到上次打开文件的点，ctrl+r重做
 U|取消当前行的所有操作
 ZZ| 保存并退出文件  
 /string，?string    |   搜索string, n,N搜索方向不同

## 编辑模式命令

命令   |    说明
-|:-:
 a    |       在光标后插入文本
 A    |       在光标所在行后插入文本
 i    |       在光标前插入文本
 I    |       在光标所在行前插入文本
 o    |       在光标所在行下插入新行(小写字母o)
 O    |       在光标所在行上插入新行(大写字母O)

## 末行命令

命令      | 说明
-|:-:
 :e        |   创建新文件
 :n        |   加载新文件
 :w        |   保存文件
 :w new_filename | 另存为
 :!command        |   执行命令
 :w!       |   强行保存文件
 :q  |   退出
 :q!       |   强行退出
 :wq, :x   |   保存退出
 :wq new_filename | 另存为并退出
 :wq!      |   强行保存退出
 :set nu   |   显示行号
 :set hlsearch   |   高亮显示搜索结果
 :set nonu |   不显示行号
 :set nohlserach |   不高亮显示搜索结果
 :nu       |   跳转到第nu行
 :n1,n2d   |   删除n1到n2行 
 :%s/old/new/g | 替换
 :r filename | 导入文件

一、打开文件

    vim /path/to/somefile
    vim +n FILE :打开文件，并定位于第n行 
    vim +: FILE :打开文件，定位至最后一行
    vim +/PATTERN FILE : 打开文件，定位至第一次被PATTERN匹配到的行的行首

默认处于编辑模式

二、关闭文件

1、末行模式关闭文件

    :q  退出
    :wq 保存并退出
    :q! 不保存并退出
    :w 保存
    :w! 强行保存
    :wq --> :x

2、编辑模式下退出

    ZZ: 保存并退出

三、移动光标(编辑模式)

1、逐字符移动：

	h: 左
	l: 右
	j: 下
	k: 上
 #h: 移动#个字符；
 
2、以单词为单位移动

	w: 移至下一个单词的词首
	e: 跳至当前或下一个单词的词尾
	b: 跳至当前或前一个单词的词首
	
	#w:向下移动#个单词 
	
3、行内跳转：

	0: 绝对行首
	^: 行首的第一个非空白字符
	$: 绝对行尾

4、行间跳转

	#G：跳转至第#行；
	G：最后一行
	
	末行模式下，直接给出行号即可
	
四、翻屏

Ctrl+f: 向下翻一屏
Ctrl+b: 向上翻一屏

Ctrl+d: 向下翻半屏
Ctrl+u: 向上翻半屏

五、删除单个字符

x: 删除光标所在处的单个字符
#x: 删除光标所在处及向后的共#个字符

六、删除命令: d

d命令跟跳转命令组合使用；
#dw, #de, #db

dd: 删除当前光标所在行
#dd: 删除包括当前光标所在行在内的#行；

末行模式下：
StartADD,EndADDd
	.: 表示当前行
	$: 最后一行
	+#: 向下的#行
	
七、粘贴命令 p

p: 如果删除或复制为整行内容，则粘贴至光标所在行的下方，如果复制或删除的内容为非整行，则粘贴至光标所在字符的后面；
P: 如果删除或复制为整行内容，则粘贴至光标所在行的上方，如果复制或删除的内容为非整行，则粘贴至光标所在字符的前面；

八、复制命令 y

	用法同d命令
	
九、修改：先删除内容，再转换为输入模式

	c: 用法同d命令

十、替换：r
R: 替换模式

十一、撤消编辑操作 u
u：撤消前一次的编辑操作
	连续u命令可撤消此前的n次编辑操作
#u: 直接撤消最近#次编辑操作

撤消最近一次撤消操作：Ctrl+r

十二、重复前一次编辑操作
.

十三、可视化模式
v: 按字符选取
V：按矩形选取

十四、查找
/PATTERN
?PATTERN
	n
	N

十五、查找并替换
在末行模式下使用s命令
ADDR1,ADDR2s@PATTERN@string@gi
1,$
%：表示全文


练习：将/etc/yum.repos.d/server.repo文件中的ftp://instructor.example.com/pub替换为http://172.16.0.1/yum

%s/ftp:\/\/instructor\.example\.com\/pub/http:\/\/172.16.0.1\/yum/g
%s@ftp://instructor\.example\.com/pub@http://172.16.0.1/yum@g

文件内容如下：
# repos on instructor for classroom use

# Main rhel5 server
[base]
name=Instructor Server Repository
baseurl=ftp://172.16.0.1/pub/Server
gpgcheck=0

# This one is needed for xen packages
[VT]
name=Instructor VT Repository
baseurl=ftp://172.16.0.1/pub/VT
gpgcheck=0

# This one is needed for clustering packages
[Cluster]
name=Instructor Cluster Repository
baseurl=ftp://172.16.0.1/pub/Cluster
gpgcheck=0

# This one is needed for cluster storage (GFS, iSCSI target, etc...) packages
[ClusterStorage]
name=Instructor ClusterStorage Repository
baseurl=ftp://172.16.0.1/pub/ClusterStorage
gpgcheck=0

十六、使用vim编辑多个文件
vim FILE1 FILE2 FILE3
:next 切换至下一个文件
:prev 切换至前一个文件
:last 切换至最后一个文件
:first 切换至第一个文件

退出
:qa 全部退出

十七、分屏显示一个文件
Ctrl+w, s: 水平拆分窗口
Ctrl+w, v: 垂直拆分窗口

在窗口间切换光标：
Ctrl+w, ARROW

:qa 关闭所有窗口

十八、分窗口编辑多个文件
vim -o : 水平分割显示
vim -O : 垂直分割显示

十九、将当前文件中部分内容另存为另外一个文件
末行模式下使用w命令
:w
:ADDR1,ADDR2w /path/to/somewhere

二十、将另外一个文件的内容填充在当前文件中
:r /path/to/somefile

二十一、跟shell交互
:! COMMAND

二十二、高级话题
1、显示或取消显示行号
:set number
:set nu

:set nonu

2、显示忽略或区分字符大小写
:set ignorecase
:set ic

:set noic

3、设定自动缩进
:set autoindent
:set ai
:set noai

4、查找到的文本高亮显示或取消
:set hlsearch
:set nohlsearch

5、语法高亮
:syntax on
:syntax off

二十三、配置文件
/etc/vimrc
~/.vimrc

vim: 
