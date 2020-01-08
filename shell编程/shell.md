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

根据变量生效范围等划分变量类型：set：查看所有变量（全局变量，局部变量还有函数）

- 环境变量
- 本地变量
- 局部变量
- 位置变量
- 特殊变量

### 环境变量(全局变量)

- 生效范围为当前shell进程及其子进程

- $HOME/.bash_profile(/etc/profile)

- 设置环境变量

```bash
# 第一种定义方法
VARNAME=VALUE
export VARNAME
# 第二种定义方法
export VARNAME=VALUE
# 第三种定义方法
declare -x VARNAME=VALUE
```

- 查看环境变量

```bash
printenv
env
export
```

PATH：命令搜索路径

HISTSIZE: 命令历史缓冲区大小

### 本地变量

- 作用域：当前bash进程生命周期
- VARNAME=VALUE
- set 显示本地所有的变量 readonly -p
- readonly variable 使变量只读

### 局部变量

局部变量在脚本或命令中定义，仅在当前shell实例中有效，其他shell启动的程序不能访问局部变量。

bash的变量默认都是全局变量，使用local关键词，可以定义只在函数内有效的局部变量，函数执行结束后，变量消失。

使用local，就相当于在函数开始的时候定义变量，在函数返回之前做unset。

local VARNAME=VALUE：作用域为当前代码段；

### 位置变量

用于让脚本在脚本代码中调用通过命令行传递给它的参数

$0 | $1 | $2 | ...
-|:-:|:-:|-
脚本名| first | second | third

### 特殊变量(预定义变量)

shell预先定义的特殊变量，不能重定义它。所有预定义变量都是由$符和另一个符号组成的，常用的shell预定义变量有：

- $#：脚本的参数个数
- $*：脚本的全部参数
- $?：显示上一个命令的退出状态。0表示正确执行，非0值表示执行有误
- $$：当前进程ID号，可用pstree -p验证
- $PPID :父进程编号
- $!：后台运行的最后一个进程号
- $0：当前执行的进程名

程序执行，可能有两类返回值：

    程序执行结果
    程序状态返回代码（0-255）
        0: 正确执行
        1-255：错误执行，1，2，127系统预留

“$$”变量最常见的用途是用作临时文件的名字以保证临时文件不会重复。

### 变量替换

- ${variable name} 变量值
- ${variable name:+value} 如果设置了variable name，则显示其值value；否则为空
- ${variable name:?message} 如果未设置variable name，则显示message
- ${variable name:-message} 如果未设置variable name，则显示message；否则为空  
- ${variable name:=value} 如果未设置variable name，则设置其值value；否则为空

### 变量清除

- unset VARNAME
- -- 表明选项结束
- -f 删除只读变量，但不能删除保留的环境变量

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

变量赋值：name=‘value’

可以使用引用value:

    (1) 可以是直接字串; name=“root"
    (2) 变量引用：name="$USER" 或者 name=${name}
    (3) 命令引用：name=`COMMAND` name=$(COMMAND)

变量引用：${name} 或者 $name

    ""：弱引用，其中的变量引用会被替换为变量值
    ''：强引用，其中的变量引用不会被替换为变量值，而保持原字符串

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

脚本：命令的堆砌，按实际需要，结合命令流程控制机制实现的源程序

shebang: 魔数, #!/bin/bash

/dev/null: 软件设备， bit bucket，数据黑洞

脚本在执行时会启动一个子shell进程；
  命令行中启动的脚本会继承当前shell环境变量；
  系统自动执行的脚本(非命令行启动)就需要自我定义需要各环境变量；

练习

1、添加5个用户, user1,..., user5

  useradd user1

2、每个用户的密码同用户名，而且要求，添加密码完成后不显示passwd命令的执行结果信息；
3、每个用户添加完成后，都要显示用户某某已经成功添加；

echo "user1" | passwd --stdin user1 &> /dev/null
echo "Add user1 successfully."


条件判断：
	如果用户不存在
		添加用户，给密码并显示添加成功；
	否则
		显示如果已经没在，没有添加；

bash中如何实现条件判断？
条件测试类型：
	整数测试
	字符测试
	文件测试

条件测试的表达式：
	[ expression ]
	[[ expression ]]
	test expression
	
整数比较:
	-eq: 测试两个整数是否相等；比如 $A -eq $B
	-ne: 测试两个整数是否不等；不等，为真；相等，为假；
	-gt: 测试一个数是否大于另一个数；大于，为真；否则，为假；
	-lt: 测试一个数是否小于另一个数；小于，为真；否则，为假；
	-ge: 大于或等于
	-le：小于或等于
	
命令的间逻辑关系：
	逻辑与： &&
		第一个条件为假时，第二条件不用再判断，最终结果已经有；
		第一个条件为真时，第二条件必须得判断；
	逻辑或： ||
	
如果用户user6不存在，就添加用户user6
! id user6 && useradd user6
id user6 || useradd user6

如果/etc/inittab文件的行数大于100，就显示好大的文件；
[ `wc -l /etc/inittab | cut -d' ' -f1` -gt 100 ] && echo "Large file."

变量名称：
	1、只能包含字母、数字和下划线，并且不能数字开头；
	2、不应该跟系统中已有的环境变量重名；
	3、最好做到见名知义；

如果用户存在，就显示用户已存在；否则，就添加此用户；
id user1 && echo "user1 exists." || useradd user1

如果用户不存在，就添加；否则，显示其已经存在；
! id user1 && useradd user1 || echo "user1 exists."

如果用户不存在，添加并且给密码；否则，显示其已经存在；
! id user1 && useradd user1 && echo "user1" | passwd --stdin user1	|| echo "user1 exists."


练习，写一个脚本，完成以下要求：
1、添加3个用户user1, user2, user3；但要先判断用户是否存在，不存在而后再添加；
2、添加完成后，显示一共添加了几个用户；当然，不能包括因为事先存在而没有添加的；
3、最后显示当前系统上共有多少个用户；



练习，写一个脚本，完成以下要求：
给定一个用户：
	1、如果其UID为0，就显示此为管理员；
	2、否则，就显示其为普通用户；

如果 UID为0；那么
  显示为管理员
否则
  显示为普通用户
  
NAME=user16
USERID=`id -u $NAME`
if [ $USERID -eq 0 ]; then
  echo "Admin"
else
  echo "common user."
fi



NAME=user16
if [ `id -u $NAME` -eq 0 ]; then
  echo "Admin"
else
  echo "common user."
fi


if id $NAME; then
  
练习：写一个脚本
判断当前系统上是否有用户的默认shell为bash；
   如果有，就显示有多少个这类用户；否则，就显示没有这类用户；
grep "bash$" /etc/passwd &> /dev/null
RETVAL=$?
if [ $RETVAL -eq 0 ]; then
   
if grep "bash$" /etc/passwd &> /dev/null; then
	
提示：“引用”一个命令的执行结果，要使用命令引用；比如: RESAULTS=`wc -l /etc/passwd | cut -d: -f1`；
      使用一个命令的执行状态结果，要直接执行此命令，一定不能引用；比如: if id user1一句中的id命令就一定不能加引号；
	  如果想把一个命令的执行结果赋值给某变量，要使用命令引用，比如USERID=`id -u user1`;
      如果想把一个命令的执行状态结果保存下来，并作为命令执行成功与否的判断条件，则需要先执行此命令，而后引用其状态结果，如
		id -u user1
		RETVAL=$?
		此句绝对不可以写为RETVAL=`id -u user1`；
	
	
练习：写一个脚本
判断当前系统上是否有用户的默认shell为bash；
   如果有，就显示其中一个的用户名；否则，就显示没有这类用户；

练习：写一个脚本
给定一个文件，比如/etc/inittab
判断这个文件中是否有空白行；
如果有，则显示其空白行数；否则，显示没有空白行。
#!/bin/bash
A=`grep '^$' /etc/inittab | wc -l`
if [ $A -gt 0 ]; then
 echo "$A"
else
 echo "meiyoukongbaihang"
fi
                 —— by 张帅
				 
#!/bin/bash
FILE=/etc/inittab
if [ ! -e $FILE ]; then
  echo "No $FILE."
  exit 8
fi

if grep "^$" $FILE &> /dev/null; then
  echo "Total blank lines: `grep "^$" $FILE | wc -l`."
else
  echo "No blank line."
fi

练习：写一个脚本
给定一个用户，判断其UID与GID是否一样
如果一样，就显示此用户为“good guy”；否则，就显示此用户为“bad guy”。
#!/bin/bash
USERNAME=user1
USERID=`id -u $USERNAME`
GROUPID=`id -g $USERNAME`
if [ $USERID -eq $GROUPID ]; then
  echo "Good guy."
else
  echo "Bad guy."
fi

进一步要求：不使用id命令获得其id号；

#!/bin/bash
#
USERNAME=user1
if ! grep "^$USERNAME\>" /etc/passwd &> /dev/null; then
  echo "No such user: $USERNAME."
  exit 1
fi

USERID=`grep "^$USERNAME\>" /etc/passwd | cut -d: -f3`
GROUPID=`grep "^$USERNAME\>" /etc/passwd | cut -d: -f4`
if [ $USERID -eq $GROUPID ]; then
  echo "Good guy."
else
  echo "Bad guy."
fi






练习：写一个脚本
给定一个用户，获取其密码警告期限；
而后判断用户密码使用期限是否已经小于警告期限；
	提示：计算方法，最长使用期限减去已经使用的天数即为剩余使用期限；
	
如果小于，则显示“Warning”；否则，就显示“OK”。

圆整：丢弃小数点后的所有内容

#!/bin/bash
W=`grep "student" /etc/shadow | cut -d: -f6`
S=`date +%s`
T=`expr $S/86400`
L=`grep "^student" /etc/shadow | cut -d: -f5`
N=`grep "^student" /etc/shadow | cut -d: -f3`
SY=$[$L-$[$T-$N]]

if [ $SY -lt $W ]; then
  echo 'Warning'
else
  echo 'OK'
fi

						—— by 董利东


练习：写一个脚本
判定命令历史中历史命令的总条目是否大于1000；如果大于，则显示“Some command will gone.”；否则显示“OK”。


shell中如何进行算术运算：
A=3
B=6
1、let 算术运算表达式
	let C=$A+$B
2、$[算术运算表达式]
	C=$[$A+$B]
3、$((算术运算表达式))
	C=$(($A+$B))
4、expr 算术运算表达式，表达式中各操作数及运算符之间要有空格，而且要使用命令引用
	C=`expr $A + $B`
