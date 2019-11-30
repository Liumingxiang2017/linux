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

# 变量
## 本地变量
- 本地变量在用户现在的shell生命周期的脚本中使用
- varibal-name=value
- set 显示本地所有的变量 readonly -p 
- readonly variable 使变量只读
## 环境变量
- 环境变量用于所有用户进程
- $HOME/.bash_profile(/etc/profile)
- export 设置环境变量
- env或者export 查看环境变量
## 变量替换
- ${variable name} 变量值
- ${variable name:+value} 如果设置了variable name，则显示其值value；否则为空
- ${variable name:?message} 如果未设置variable name，则显示message
- ${variable name:-message} 如果未设置variable name，则显示message；否则为空  
- ${variable name:=value} 如果未设置variable name，则设置其值value；否则为空

## 变量清除
### unset variable-name
- -- 表明选项结束
- -f 删除只读变量，但不能删除保留的环境变量
## 位置变量
$0 | $1 | $2 | ...
-|:-:|:-:|-
脚本名| first | second | third
## 标准变量
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
## 特殊变量
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
- 设置或者重设各种shell
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

- $[] 表示括号中的表达式求值，等于$(())

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