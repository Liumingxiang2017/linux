# bash

shell编程：

shell作为编译器，解释器

编程语言：机器语言、汇编语言、高级语言

静态语言：编译型语言

    强类型(变量)：变量在使用前，必须事先声明，甚至还需要初始化；
    事先转换成可执行格式
    C、C++、JAVA、C#

动态语言：解释型语言， on the fly，在计算机专业中on the fly的意思为:即时生效或在运行

    弱类型：变量用时声明，甚至不区分类型；
    边解释边执行
    PHP、SHELL、python、perl

面向过程：Shell, C

面向对象: JAVA, Python, perl, C++

shell: 弱类型编程语言

变量：内存空间，命名

内存：编址的存储单元

变量类型：事先确定数据的存储格式和长度

    字符
    数值
        整型
        浮点型: 11.23， 1.123*10^1, 0.1123*10^2
    2013/10/10, 64bit
    99999: 24bit, 
    真、假

站在用户登录的角度来说，SHELL的类型：

登录式shell:

    正常通常某终端登录
    su - USERNAME 
    su -l USERNAME

非登录式shell:

    su USERNAME
    图形终端下打开命令窗口
    自动执行的shell脚本

bash的配置文件：

全局配置

    /etc/profile, /etc/profile.d/*.sh, /etc/bashrc

个人配置

    ~/.bash_profile, ~/.bashrc

profile类的文件：

    设定环境变量
    运行命令或脚本

bashrc类的文件：

    设定本地变量
    定义命令别名

登录式shell如何读取配置文件？

    /etc/profile --> /etc/profile.d/*.sh --> ~/.bash_profile --> ~/.bashrc --> /etc/bashrc

非登录式shell如何配置文件?

    ~/.bashrc --> /etc/basrc --> /etc/profile.d/*.sh

profile: 定义环境变量、运行程序或脚本

bashrc：定义本地变量、命令别名

## 光标跳转

Ctrl+a：跳到命令行首
Ctrl+e：跳到命令行尾
Ctrl+u: 删除光标至命令行首的内容
Ctrl+k: 删除光标至命令行尾的内容
Ctrl+l: 清屏

命令补全，路径补全
命令补全：搜索PATH环境变量所指定的每个路径下以我们给出的字符串开头的可执行文件，如果多于一个，两次tab，可以给出列表；否则将直接补全；
路径补全：搜索我们给出的起始路径下的每个文件名，并试图补全；

## history : 查看命令历史

-c：清空命令历史

-d OFFSET [n]: 删除指定位置的命令

-w：保存命令历史至历史文件中

HISTSIZE

当前用户命令记录~/.bash_history

!n：执行命令历史中的第n条命令；

!-n:执行命令历史中的倒数第n条命令；

!!: 执行上一条命令；

!string：执行命令历史中最近一个以指定字符串开头的命令

!$:引用前一个命令的最后一个参数;

Esc+. 执行上一条命令

Alt+. 动态上翻命令历史

## 命令别名

alias 设置别名

alias CMDALIAS='COMMAND [options] [arguments]'

在shell中定义的别名仅在当前shell生命周期中有效；别名的有效范围仅为当前shell进程；

ualias 取消别名

ualias CMDALIAS

\CMD

命令替换: $(COMMAND), 反引号：\`COMMAND\`

把命令中某个子命令替换为其执行结果的过程

file-2013-02-28-14-53-31.txt

## bash支持的引号

``: 命令替换
"": 弱引用，可以实现变量替换
'': 强引用，不完成变量替换

## 文件名通配, globbing

    man 7 glob
    *: 任意长度的任意字符
    ?：任意单个字符
    []：匹配指定范围内的任意单个字符
    [abc], [a-m], [a-z], [A-Z], [0-9], [a-zA-Z], [0-9a-zA-Z]
    [:space:]：空白字符
    [:punct:]：标点符号
    [:lower:]：小写字母
    [:upper:]: 大写字母
    [:alpha:]: 大小写字母
    [:digit:]: 数字
    [:alnum:]: 数字和大小写字母
    [^]: 匹配指定范围之外的任意单个字符
    [[:alpha:]]*[[:space:]]*[^[:alpha:]]

## 练习

1、显示所有以a或m开头的文件；

    ls [am]*

2、显示所有文件名中包含了数字的文件；

    ls *[0-9]* 
    ls *[[:digit:]]*

3、显示所有以数字结尾且文件名中不包含空白的文件；

    ls *[^[:space:]]*[0-9]   ?????????

4、显示文件名中包含了非字母或数字的特殊符号的文件；

    ls *[^[:alnum:]]*


## chmod [who] operator [permission] file

- who (u,g,o,a)
- operator (+,-,=)
- permission (r,w,x,s,t)

## chmod mode file

- r=4,w=2,x=1
- u,g的s分别为4，2,t是1

## chown [-R] user.group file/directory

## chgrp group file/directory

## umask

- default value 022,file没有默认没有执行权限
- /etc/profile($HOME/.profile $HOME/.bash_profile)(cat /etc/profile |grep "umask")

## 符号链接 (ln [-s] source-path target-path)

## alias command=""

- $HMOE/.bashrc 

## 后台永久处理

- nohup command &
- & ： 指在后台运行
- nohup (no hang up)： 不挂断的运行，注意并没有后台运行的功能，，就是指，用nohup运行命令可以使命令永久的执行下去，和用户终端没有关系

## 特殊字符

- 双引号： 去除$,`,\的特殊含义
- 单引号： 去除所有字符特殊含义
- 反引号： 用于替换命令的执行结果
- 反斜杠： 不解读特殊含义字符：& * + ^ $ ` " | ?
- 分号： 连续运行命令
- & ： 命令后台执行
- 括号：创建成组的命令
- 大括号：创建命令块

## 系统设定

默认输出设备：标准输出，STDOUT, 1

默认输入设备：标准输入, STDIN, 0

标准错误输出：STDERR, 2

标准输入：键盘

标准输出和错误输出：显示器

2>: 重定向错误输出

2>>: 追加方式

&>: 重定向标准输出或错误输出至同一个文件

<：输入重定向

<<：Here Document

## bash变量类型

- 环境变量
- 本地变量(局部变量)
- 位置变量
- 特殊变量

### 环境变量

- 环境变量用于所有用户进程及其子进程

- $HOME/.bash_profile(/etc/profile)

- 设置环境变量使用export命令

```bash
export VARNAME=VALUE
# 或者 先简单定义后"导出"
VARNAME=VALUE
export VARNAME
```

- 查看环境变量，env或者export

PATH：命令搜索路径

HISTSIZE: 命令历史缓冲区大小

### 本地变量（局部变量）

- 作用域：当前bash进程生命周期
- varibal-name=value
- set 显示本地所有的变量 readonly -p
- readonly variable 使变量只读

### 变量替换

- ${variable name} 变量值
- ${variable name:+value} 如果设置了variable name，则显示其值value；否则为空
- ${variable name:?message} 如果未设置variable name，则显示message
- ${variable name:-message} 如果未设置variable name，则显示message；否则为空  
- ${variable name:=value} 如果未设置variable name，则设置其值value；否则为空

### 变量清除

#### unset variable-name

- -- 表明选项结束
- -f 删除只读变量，但不能删除保留的环境变量

### 位置变量

$0 | $1 | $2 | ...
-|:-:|:-:|-
脚本名| first | second | third

### 标准变量

- /etc/profile
- EXINIT vi的参数
- HOME 主目录
- IFS 系统默认间隔符
- LOGNAME 登录名
- MAIL 当前用户邮箱位置
- MAILCHECK 每隔多少秒检查是否有新邮件
- TERM 终端类型
- PATH 可执行文件寻找的路径
- TZ 时区
- PS1 提示符

### 特殊变量

- $# 脚本的参数个数
- $* 脚本全部参数
- $$ 进程ID号
- $? 显示最后命令的退出状态。0表示没有错误，其他任何值表示有错误

## 影响变量的命令

### declare （与typeset相同）

- 设置或者显示变量
- -f 只显示函数名
- -r 创建只读变量
- -x 创建export变量
- -i 创建整数变量
- 使用+代替-，可以颠倒选项的含义

### export

- 用于创建传递给子shell的变量
- -p 显示全局变量列表

### readonly

- 用于显示或者设置只读变量
- -- 表明选项结束
- -f 创建只读变量

### set

set用于设置各种shell

set -C: 禁止对已经存在文件使用覆盖重定向；强制覆盖输出，则使用 >|

set +C: 关闭上述功能

### shift [n]

- 移动位置变量，后面参数往前移动n位

## 运算符

- 按位运算符

operator | Notes
-| :-:
~op1|取反
op1<<op2|左移op2位，忽略最左端，最右端补0，相当于实现op1乘以2
op1>>op2|右移op2位，忽略最右端，最左端补0，相当于实现op1除以2
op1&op2 |与
op1^op2 |异或
op1\|op2 |或

- $[  ] 表示括号中的表达式求值，等于$(())

- [base#n]可以表示基数为2到36的值

- 逻辑运算符

运算符 | 说明
-|:-:
&& | 与运算符
\|\| | 或运算符
>,==,<,!= | 大于，等于，小于，不等于

## 赋值运算符

- =、+=

- let $count = $count + $change

练习：

1、统计/usr/bin/目录下的文件个数；

    ls /usr/bin | wc -l

2、取出当前系统上所有用户的shell，要求，每种shell只显示一次，并且按顺序进行显示；

    cut -d: -f7 /etc/passwd | sort -u

3、思考：如何显示/var/log目录下每个文件的内容类型？

4、取出/etc/inittab文件的第6行；

    head -6 /etc/inittab | tail -1

5、取出/etc/passwd文件中倒数第9个用户的用户名和shell，显示到屏幕上并将其保存至/tmp/users文件中；

    tail -9 /etc/passwd | head -1 | cut -d: -f1,7 | tee /tmp/users

6、显示/etc目录下所有以pa开头的文件，并统计其个数；

    ls -d /etc/pa* | wc -l

7、不使用文本编辑器，将alias cls=clear一行内容添加至当前用户的.bashrc文件中

    echo "alias cls=clear" >> ~/.bashrc