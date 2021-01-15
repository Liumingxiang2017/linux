# Vim 文本编辑器
<!-- TOC -->

1. [Vim 文本编辑器](#vim-文本编辑器)
    1. [Vim模式](#vim模式)
    2. [模式转换：](#模式转换)
    3. [配置文件](#配置文件)
    4. [命令模式](#命令模式)
    5. [编辑模式](#编辑模式)
    6. [末行模式](#末行模式)
        1. [地址定界](#地址定界)
        2. [查找](#查找)
        3. [查找并替换](#查找并替换)
    7. [按功能分类：](#按功能分类)
        1. [打开文件](#打开文件)
        2. [关闭文件](#关闭文件)
        3. [光标跳转(命令模式)](#光标跳转命令模式)
2. [COMMAND: 移动#个字符；](#command-移动个字符)
3. [w:向下移动#个单词](#w向下移动个单词)
        1. [翻屏](#翻屏)
        2. [编辑命令](#编辑命令)
            1. [删除单个字符x](#删除单个字符x)
            2. [删除命令: d](#删除命令-d)
            3. [粘贴命令 p](#粘贴命令-p)
            4. [复制命令 y](#复制命令-y)
            5. [修改c](#修改c)
            6. [替换：r replace](#替换r-replace)
            7. [撤消编辑操作 u](#撤消编辑操作-u)
            8. [撤消最近一次撤消操作：Ctrl+r](#撤消最近一次撤消操作ctrlr)
            9. [重复前一次编辑操作](#重复前一次编辑操作)
        3. [可视化模式](#可视化模式)
        4. [查找](#查找-1)
        5. [查找并替换](#查找并替换-1)
        6. [多文件模式](#多文件模式)
        7. [单文件窗口分隔](#单文件窗口分隔)
        8. [窗口分隔模式](#窗口分隔模式)
    1. [定制vim的工作特性](#定制vim的工作特性)
        1. [配置文件](#配置文件-1)
        2. [末行模式：当前vim进程有效](#末行模式当前vim进程有效)
    2. [vim补充](#vim补充)

<!-- /TOC -->

Vim: Visual Interface iMproved 文本编辑器，全屏编辑器，模式化编辑器，字处理器，

文本：ASCII，Unicode

文本编辑器种类：
- 行编辑器：sed
- 全屏编辑器：nano, vi

## Vim模式

- 命令模式(Command Mode)： 控制光标移动，删除- 符，段落复制。
- 输入模式(Insert Mode)： 新增文字及修改文字。
- 末行模式(Last Line Mode)：内置的命令行接口，保存文件，离开vi，- 及其他设置。

## 模式转换：

命令模式-->输入模式：

- i: insert 在当前光标所在字符的前面，转为输入模式；
- a: append 在当前光标所在字符的后面增加（add），转为输入模式；
- o: open 在当前光标所在行的下方，新建一行，并转为输入模式；
- I：在当前光标所在行的行首，转换为输入模式
- A：在当前光标所在行的行尾，转换为输入模式
- O：在当前光标所在行的上方，新建一行，并转为输入模式；
- c: change
- C：change

输入模式-->命令模式：ESC

命令-->末行：：

末行模式-->命令模式：ESC, ESC

末行模式-->输入模式：ESC, i/a/o


vi -o file1 file2 同时打开2个文件，横排

vi -O file1 file2 同时打开2个文件，竖排

ctrl+ww 切换窗口

## 配置文件

 ~/.vimrc 

- 显示行号 set nu
- 关闭语法 syn off
- 创建快捷键 map ^P i#\<ESC>
- 注释是双引号"

## 命令模式

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
 dw   |  删除delete光标所在的一个单词word
 d$   |  删除光标到行尾
 dd   |  删除光标所在行
ndd   |  从光标所在行向下删除n行，为数字
dG    |  删除光标所在行到末尾
 D    |  删除光标所在处到行尾
 r    |  取代光标处的一个字符
 R    |  从光标处向后替换，按Esc结束
 u    |  取消上步的操作
 U    |  取消目前的所有操作
 y    |  复制选中的内容到剪贴板
 yy，Y   |  复制光标所在行
 nyy，nY |  复制光标所在行以下n行
 p    |  将复制或者删除的内容放在光标所在行的下行
 s|替换光标所在处字符，并进入文本输入方式
 S|替换光标所在全行，按ESC结束
 u|取消上一步操作，取消到上次打开文件的点，ctrl+r重做
 U|取消当前行的所有操作
 ZZ| 保存并退出文件  
 /string，?string    |   搜索string, n,N搜索方向不同

## 编辑模式

命令   |    说明
-|:-:
 a    |       在光标后插入文本
 A    |       在光标所在行后插入文本
 i    |       在光标前插入文本
 I    |       在光标所在行前插入文本
 o    |       在光标所在行下插入新行(小写字母o)
 O    |       在光标所在行上插入新行(大写字母O)

## 末行模式

内建命令行接口

### 地址定界
- :start_pos,end_pos
- m: 具体第m行
- m,n: 从m行到n行
- m,+p: 从第m行到m+p行
- .: .表示当前行
- $：最后一行
- .,$-1：当前行到倒数第二行
- %：全文，相当于1,$
- /pat1/,/pat2/：从第一次被pat1模式匹配到的行开始，一直到第一次被pat2匹配到的行结束
- #,/pat/
- /pat/,$
	
使用方式：地址定界后，后跟一个编辑命令
- :d
- :y
- :w /path/to/somewhere 把定界范围内的行另存至指定文件中
- :r /paht/from/somefile 在指定位置插入指定文件中的所有内容

:1,4s/old/new/g 


### 查找

- /PATTERN 从当前光标所在处向文件尾部查找
- ?PATTERN 从当前光标所在处向文件首部查找

- n：与命令同方向
- N：与命令反方向

### 查找并替换

s: 在末行模式下完成查找替换操作

地址定界s/要查找的内容/要替换为的内容/修饰符

- 要查找的内容：可以使用模式
- 替换为的内容：不能使用模式，但可以使用\1,\2,...等后向引用符号，还可以使用“&”引用前面查找到的整个内容
- 修饰符：
	- i: 忽略大小写
	- g：全局替换，默认情况下，每一行只替换第一次出现；
- 分隔符/：可以替换为其他字符，s@@@ s###


可以配合地址定界进行查找替换。


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
 :set nohlsearch |   不高亮显示搜索结果
 :nu       |   跳转到第nu行
 :n1,n2d   |   删除n1到n2行 
 :%s/old/new/g | 替换
 :r filename | 插入文件

:r !ls 插入ls命令的结果
:r !nl % 插入对当前文本编号的结果。（nl表示对文件编号，%表示当前文件）

## 按功能分类：

### 打开文件

- vim [OPTIONS] /path/to/somefile
- vim +n FILE :打开文件，并定位于第n行 
- vim +: FILE :打开文件，定位至最后一行，或者vim + FILE
- vim +/PATTERN FILE : 打开文件，定位至第一次被PATTERN匹配到的行的行首

默认处于编辑模式

### 关闭文件

1. 末行模式关闭文件

	- :q  退出
	- :wq 保存并退出
	- :q! 不保存并退出
	- :w 保存
	- :w! 强行保存
	- :wq 保存退出
	- :x 保存退出
	- :w /path/to/somewhere 保存至指定文件

2. 命令模式下退出

    ZZ: 保存并退出

### 光标跳转(命令模式)

1、逐字符移动：

- h: 左
- l: 右
- j: 下
- k: 上
	
#COMMAND: 移动#个字符；
 
2、单词间跳转

- w: 移至下一个单词的词首
- e: 跳至当前或下一个单词的词尾
- b: 跳至当前或前一个单词的词首
	
#w:向下移动#个单词 
	
3、行首行尾跳转

- 0: 绝对行首
- ^: 行首的第一个非空白字符
- $: 绝对行尾

4、行间跳转

- #G：跳转至第#行；
- G：最后一行
- 1G,gg：第一行
	
末行模式下，直接给出行号即可

5、句间移动：
- ) 下一句
- ( 上一句

6、段落间移动
- } 下一段
- { 上一段

### 翻屏

一屏
- Ctrl+f: forward 向下翻一屏
- Ctrl+b: backward 向上翻一屏

半屏
- Ctrl+d: downward 向下翻半屏
- Ctrl+u: up 向上翻半屏

### 编辑命令

#### 删除单个字符x

- x: 删除光标所在处的单个字符
- #x: 删除光标所在处及向后的共#个字符
- xp: 删除当前字符，并在下一个字符粘贴paste；等于交换字符

#### 删除命令: d

d命令跟跳转命令组合使用；
- d$：删除到行尾
- d^：删除到行首（第一个非空白字符）
- d0：删除到行首（绝对行首）
- #dw 删除单词（w表示下一个单词词首）
- #de 删除单词（ 跳至当前或下一个单词的词尾）
- #db
- #d)
- #db

- dd: 删除当前光标所在行，完全删除
- #dd: 删除包括当前光标所在行在内的#行；
- D：删除当前光标所在行，保留空白行

末行模式下：
StartADD,EndADDd
	.: 表示当前行
	$: 最后一行
	+#: 向下的#行
	
#### 粘贴命令 p

- 小p: 如果删除或复制为整行内容，则粘贴至光标所在行的下方，如果复制或删除的内容为非整行，则粘贴至光标所在字符的后面；
- 大P: 如果删除或复制为整行内容，则粘贴至光标所在行的上方，如果复制或删除的内容为非整行，则粘贴至光标所在字符的前面；

#### 复制命令 y

用法同d命令
- y$
- y0
- y^
- ye
- yw
- yb
- yy 复制整行
- #yy 复制多行	
	
#### 修改c

先删除内容，再转换为输入模式。

c: change用法同d命令
- c$
- c^
- c0
- cw
- ce
- cb
- cc
- #cc

#### 替换：r replace
r与x很相似，替换光标所在处字符

R: 替换模式

#### 撤消编辑操作 u

- u：撤消前一次的编辑操作；连续u命令可撤消此前的n次编辑操作
- #u: 直接撤消最近#次编辑操作

#### 撤消最近一次撤消操作：Ctrl+r

#### 重复前一次编辑操作
.

### 可视化模式
用于选定内容，结合编辑命令使用。先选中再编辑。
- v: 按字符选取
- V：按矩形选取，整行选定

### 查找
/PATTERN
?PATTERN
	n 向下查找
	N 向上查找，等于 shift+n

### 查找并替换
在末行模式下使用s命令
ADDR1,ADDR2s@PATTERN@string@gi
1,$
%：表示全文


### 多文件模式

使用vim编辑多个文件

vim FILE1 FILE2 FILE3

vim /tmp/{file1,file2,file3} 命令行展开

- :next 切换至下一个文件
- :prev 切换至前一个文件
- :last 切换至最后一个文件
- :first 切换至第一个文件

退出
:wall 保存所有
:qall 退出所有

:qa 全部退出

### 单文件窗口分隔

分屏显示一个文件

- Ctrl+w, s: 水平拆分窗口 split
- Ctrl+w, v: 垂直拆分窗口 vertical

在窗口间切换光标：
Ctrl+w, ARROW

:qa 关闭所有窗口

### 窗口分隔模式

分窗口编辑多个文件 vim -o|-O file1 file2 ...
- vim -o : 水平分割显示
- vim -O : 垂直分割显示

在窗口键切换，ctrl+w, arrow

配合单文件切割，



二十一、跟shell交互
:! COMMAND


## 定制vim的工作特性

### 配置文件
永久有效
- 全局：/etc/vimrc
- 个人：~/.vimrc, 该文件不存在，需要自行创建，最对个人用户有效

### 末行模式：当前vim进程有效

1、显示或取消显示行号
- :set number
- :set nu 显示行号简写
- :set nonumber
- :set nonu

2、显示忽略或区分字符大小写，默认不忽略，因为linux本身区分大小写
- :set ignorecase
- :set ic
- :set noignorecase 
- :set noic

3、设定自动缩进（对于程序员重要）
- :set autoindent
- :set ai
- :set noai

4、查找到的文本高亮显示或取消
- :set hlsearch
- :set nohlsearch

5、语法高亮显示 （对于程序员重要）
- :syntax on
- :syntax off

6、括号匹配
- :set showmatch 显示匹配，简写为 :set sm
- :set nosm 取消匹配

## vim补充

自学命令：vimtutor

帮助：末行模式下
- :help
- :help keyword

ctrl+g 显示所处行数，和位置占比

可视行

shift+v 可视行操作。

块操作


按ctrl+v，进入可视块状态，按j向下，l向右，定义一个块，x删除块

按v进入可视状态，j向下选择行


F1 在任何模式下进入帮助模式，在帮助模式下 :help w 针对w命令查看帮助信息

emacs 

以前被称为编辑器之神，特点：全面，复杂，大量快捷键。可以写代码，编译程序，发邮件，甚至打游戏，几乎等于一个系统。



练习：

将/etc/yum.repos.d/server.repo文件中的ftp://instructor.example.com/pub替换为http://172.16.0.1/yum

```shell
%s/ftp:\/\/instructor\.example\.com\/pub/http:\/\/172.16.0.1\/yum/g
%s@ftp://instructor\.example\.com/pub@http://172.16.0.1/yum@g
```

文件内容如下：
```
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
```

如何设置tab缩进为4个字符？

