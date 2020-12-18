# shell基本特性
<!-- TOC -->

1. [shell基本特性](#shell基本特性)
    1. [命令历史](#命令历史)
    2. [命令补全](#命令补全)
    3. [路径补全](#路径补全)
    4. [命令行展开](#命令行展开)
    5. [命令的执行结果状态](#命令的执行结果状态)
    6. [命令别名](#命令别名)
    7. [bash支持的引号](#bash支持的引号)
    8. [glob/globbing 文件名通配符](#globglobbing-文件名通配符)
    9. [bash快捷键](#bash快捷键)
    10. [bash的I/O重定向及管道](#bash的io重定向及管道)
        1. [标准输入、输出、错误](#标准输入输出错误)
        2. [I/O重定向](#io重定向)
    11. [管道](#管道)
        1. [echo [option] string](#echo-option-string)
        2. [read](#read)
        3. [cat](#cat)
        4. [tee](#tee)
        5. [exec](#exec)
    12. [练习](#练习)
    13. [后台永久处理](#后台永久处理)
    14. [特殊字符](#特殊字符)
    15. [运算符](#运算符)
    16. [赋值运算符](#赋值运算符)
2. [!/bin/bash](#binbash)
3. [!/bin/bash](#binbash-1)
4. [!/bin/bash](#binbash-2)
5. [!/bin/bash](#binbash-3)
6. [!/bin/bash](#binbash-4)

<!-- /TOC -->

1. 提供编程环境，shell程序提供了编程能力，解释执行。

程序编程风格
- 面向过程：以指令为中心，数据服务于指令。例如：Shell, C
- 面向对象: 以数据为中心，指令服务于数据。由数据设计类，由类设计方法。例如：JAVA, Python（可面向过程，可面向对象）, perl, C++

shell编程：

shell作为编译器，解释器

静态语言：编译型语言

    强类型(变量)：变量在使用前，必须事先声明，甚至还需要初始化；
    事先转换成可执行格式
    C、C++、JAVA、C#

动态语言：解释型语言， on the fly，在计算机专业中on the fly的意思为:即时生效或在运行

    弱类型：变量用时声明，甚至不区分类型；
    边解释边执行
    PHP、SHELL、python、perl

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


> #！魔数行，制定解释器位置

## 命令历史 
命令历史是shell提供的功能。

history : 查看命令历史

环境变量：
- HISTSIZE：命令历史记录的条数
- HISTFILE: ~/.bash_history， 当前用户命令记录~/.bash_history
- HISTFILESIZE: 命令历史文件记录历史的条数

参数：
- -c：清空命令历史
- -d OFFSET [n]: 删除指定位置的命令
- hisotry #：显示历史中最近#条命令；
- -a 手动追加当前会话缓冲区的命令历史至历史文件中；
- -w：保存命令历史至历史文件中

调用历史中的命令:
- !n：重复执行命令历史中的第n条命令；
- !-n:执行命令历史中的倒数第n条命令；
- !!: 执行上一条命令；
- !string：执行命令历史中最近一个以指定字符串开头的命令

调用上一条命令最后一个参数：
- !$: 引用前一个命令的最后一个参数;
- Esc . 执行上一条命令
- alt + .

控制命令历史的记录方式：

对应环境变量：HISTCONTROL 
- ignoredups 忽略重复命令(连续且相同为“重复”)
- ignorespace 忽略所有以空白字符开头的命令；
- ignoreboth 忽略二者

修改HISTCONTROL环境变量值: export HISTCONTROL="值"

变量赋值：把赋值符号后面的数据存储于变量名指向的内存空间。

## 命令补全
bash执行命令：
- 内部命令
- 外部命令：bash根据PATH环境变量定义的路径，自左而右在每个路径下搜索以给定命令命令的文件，第一次找到的即为要为执行的命令。

命令补全：

搜索PATH环境变量所指定的每个路径下以我们给出的字符串开头的可执行文件，如果多于一个，两次tab，可以给出列表；否则将直接补全；
- 直接补全：tab，用户给定的字符串只有一条唯一对应命令
- 以用户给定字串为开头对应的命令不唯一，再次tab，给出列表

## 路径补全
路径补全：搜索我们给出的起始路径下的每个文件名，并试图补全；
- 如果唯一，直接补全
- 否则，tab给出列表

## 命令行展开

- ~：展开为用户主目录，~USERNAME: 展开为指定用户的主目录
- {}：可承载一个以逗号分隔的列表，并将其展开为多个路径。 比如/tmp/{a,b} = /tmp/a /tmp/b

linux管理员必用的是大技巧之一：花括号展开

花括号展开的表达式可以看作一个由 花括号、逗号 和 小写英文字母 组成的字符串，定义下面几条语法规则：

如果只给出单一的元素 x，那么表达式表示的字符串就只有 "x"。 

    例如，表达式 {a} 表示字符串 "a"。

    而表达式 {ab} 就表示字符串 "ab"。

当两个或多个表达式并列，以逗号分隔时，我们取这些表达式中元素的并集。

    例如，表达式 {a,b,c} 表示字符串 "a","b","c"。

    而表达式 {a,b},{b,c} 也可以表示字符串 "a","b","c"。

要是两个或多个表达式相接，中间没有隔开时，我们从这些表达式中各取一个元素依次连接形成字符串。

    例如，表达式 {a,b}{c,d} 表示字符串 "ac","ad","bc","bd"。

表达式之间允许嵌套，单一元素与表达式的连接也是允许的。

    例如，表达式 a{b,c,d} 表示字符串 "ab","ac","ad"​​​​​​。

    例如，表达式 {a{b,c}}{{d,e}f{g,h}} 可以代换为 {ab,ac}{dfg,dfh,efg,efh}，表示字符串 "abdfg", "abdfh", "abefg", "abefh", "acdfg", "acdfh", "acefg", "acefh"。

    /mnt/test2/
    a_b, a_c, d_b, d_c
    (a+d)(b+c)=ab+ac+db+dc
    {a,d}_{b,c}

## 命令的执行结果状态

只有两种执行结果状态：
- 成功
- 失败

bash使用功能特殊变量$?保存最近一条命令的执行状态结果
- 0：成功
- 1-255：失败

程序执行的两类结果：
- 程序的返回值
  - 成功时，返回所需要的结果
  - 失败时，返回报错信息
- 程序的执行状态结果

## 命令别名

alias 设置别名 

type alias: a shell builtin

1. alias 显示当前shell进程所有可用命令别名
2. alias CMDALIAS='COMMAND [options] [arguments]' 定义命令别名

注意：在shell中定义的别名仅在当前shell生命周期中有效；别名的有效范围仅为当前shell进程；如果想永久有效，要定义在配置文件中：
- 仅对当前用户有效：~/.bashrc，
- 对所有用户有效：/etc/bashrc

编辑配置文件不会立即生效需要重读。

bash进程重读配置文件
- source /path/to/config_file
- . /path/to/config_file

ualias 撤销别名

- SYNOPSIS ualias [-a] CMDALIAS
- -a 撤销所有别名

如果别名同原命令名称，则要执行原命令，可使用 \CMD

命令替换: $(COMMAND), 反引号：\`COMMAND\`

把命令中某个子命令替换为其执行结果的过程

file-2013-02-28-14-53-31.txt


## bash支持的引号

- ``: 命令替换
- "": 弱引用，可以实现变量替换
- '': 强引用，不完成变量替换

## glob/globbing 文件名通配符

bash中用于实现文件名通配的机制。

whatis glob

man 7 glob

通配类型
- classes 类别
- ranges 范围
- complementation 补全

通配符
```
- *: 任意长度的任意字符
- ?：任意单个字符
- []：匹配指定范围内的任意单个字符
  - [abc], [a-z]不区分大小写, [A-Z]仅大写, [0-9]
- [^]: 匹配指定范围之外的 任意单个字符
  - [^0-9] 非数字
  - [^0-9a-z] 特殊字符（非数字非字母）
- 字符集合，需要在集合外再加上[]，比如[[:space:]]
  - [:space:]：空白字符
  - [:punct:]：标点符号
  - [:lower:]：小写字母
  - [:upper:]: 大写字母
  - [:alpha:]: 大小写字母
  - [:digit:]: 数字
  - [:alnum:]: 数字和大小写字母
  - [[:alpha:]]*[[:space:]]*[^[:alpha:]]
```

## bash快捷键

- Ctrl+l: 清屏, 相当于clear
- Ctrl+a：跳到命令行首ahead
- Ctrl+e：跳到命令行尾end
- Ctrl+u: 删除光标至命令行首的内容
- Ctrl+k: 删除光标至命令行尾的内容

## bash的I/O重定向及管道

### 标准输入、输出、错误

每个文件都有一个fd：file descriptor（文件描述符）。

文件 |文件描述符
-|:-:
标准输入| 0（缺省是键盘 keyboard）
标准输出| 1（缺省是屏幕 monitor）
标准错误| 2（缺省是屏幕 monitor）

### I/O重定向

- I/O重定向：改变标准位置
```
输出重定向： COMMAND > NEW_POS , COMMAND >> NEW_POS
  > 覆盖重定向，新内容会被追加至目标尾部
    >| 强制覆盖
  >> 追加重定向，目标文件中原内容会被清除；

```
- 禁止覆盖
  - set -C：禁止将内容覆盖输出值已有文件中。
  - set +C：关闭禁止覆盖功能。

- 错误重定向
  - 2>：覆盖重定向错误输出数据流
  - 2>>：追加重定向错误输出数据流

- 标准输出和错误输出各自定向至不同位置：COMMAND > /path/to/file.out 2> /path/to/file.err

- 合并标准输出和错误输出为同一个输出流进行重定向：
  - &> 覆盖重定向
  - &>> 追加重定向

- 输入重定向 <

- HERE Docmentation 此处生成文档：<<
  - cat << EOF: 以EOF作为结束符，输入
  - cat >> /tmp/test.out << EOF

举例
- cat file1 file2 1>file.out 2>file.err
  - 如果有标准输出输出到file.out,如果有标准错误输出到file.err
- command > file.out 2> &1 
  - 把标准输出和标准错误一起重定向到file
- command < file1 > file2
  - command命令以file1作为标准输入，file2作为标准输出
- command << delimiter
  - 从标准输入中读入，直到遇到delimiter分界符，常用分隔符为EOF（EndOfFile）
- command<&m 
  - 把文件描述符m作为标准输入
- command>&m
  - 把标准输出重定向到文件描述符m
- command <&-
  - 关闭标准输入

## 管道
COMMAND1 | COMMAND2 | COMMAND3 

Note: 最后一个命令在当前shell进程的子进程中执行。

### echo [option] string

- -e 解析转义字符
- -n 回车不换行，linux默认回车换行

### read

- 从键盘或者文件的某一行文本中读入信息，并将其赋给一个变量
- read variable1 variable ... 按顺序赋值

### cat 

- -v 显示控制字符
- cat [option] file1 file2 ...
    - 同时输入file1 file2

### tee
从标准输入读数据，输出到标准输出，并拷贝到文件。这种情况在配合管道时有用，即能将输出到屏幕中且能输出到指定文件。

tee [OPTIONS]... [files]...
- tee -a files
    - -a, --append (append to the given files, do not overwrite)

### exec
- 用来替代当前shell，使用时任何环境变量将被清除
- exec command
    - command 通常是一个脚本
    - 只有在对文件描述符操作时，才不会覆盖当前shell


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

    echo "user1" | passwd --stdin user1 &> /dev/null

3、每个用户添加完成后，都要显示用户某某已经成功添加；

    echo "Add user1 successfully."

如果用户存在，就显示用户已存在；否则，就添加此用户；
id user1 && echo "user1 exists." || useradd user1

如果用户不存在，就添加；否则，显示其已经存在；
! id user1 && useradd user1 || echo "user1 exists."

如果用户不存在，添加并且给密码；否则，显示其已经存在；
! id user1 && useradd user1 && echo "user1" | passwd --stdin user1 || echo "user1 exists."

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

练习：写一个脚本
判定命令历史中历史命令的总条目是否大于1000；如果大于，则显示“Some command will gone.”；否则显示“OK”。

shell中如何进行算术运算：

A=3,B=6

1、let 算术运算表达式

    let C=$A+$B

2、$[算术运算表达式]

    C=$[$A+$B]

3、$((算术运算表达式))

    C=$(($A+$B))

4、expr 算术运算表达式，表达式中各操作数及运算符之间要有空格，而且要使用命令引用

    C=`expr $A + $B`
