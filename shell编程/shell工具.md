## 日志文件

以时间为标志的日志文件

```shell
#!/bin/bash
#datelog.sh
#当前的日期
current_date=`date "+%Y%m%d"`
toudaylog="log/${current_date}.log"
if [ ! -f $todaylog ]
then
    touch $todaylog
fi
log_time_format=`date "+%Y-%m-%d %T"`
echo "${log_time_format} 命令开始" >> $todaylog
#command blocks
sleep 4
lgo_time_format=`date "+%Y-%m-%d %T"`
echo "${log_time_format} 命令结束" >> $todaylog
```

以进程号为标识的临时文件

```shell
#！/bin/bash
#kill_process.sh
current_PID=$$
ps -aux|grep "/usr/sbin/httpd"|grep -v "grep"|awk "{print $2}">/tmp/${current_PID}.txt

for pid in `cat /tmp/${current_PID}.txt`
do
{
    echo "kill -9 $pid"
    kill -9 $pid
}
done
rm -f /tmp/${current_PID}.txt
```

## 信号

信号就是系统向脚本或者命令发出的消息，告知他们某个事件发生。

kill -l 列出所有信号

信号 | 信号名 | 含义
- |:-:|-
0 |         | 退出shell，通常使用exit或者\<CTRL-D\>  
1 | SIGHUP  | 挂起或者父进程被杀死
1 | SIGINT  | 来自键盘的中断信号，通常是\<CTRL-C\>
3 | SIGQUIT | 从键盘退出
9 | SIGKILL | 无条件杀死进程

```shell
kill -s SIGKILL pidnumber
kill -9 pid number
```

## trap捕捉信号

trap使你可以在脚本中捕获信号。命令形式：trap 'function_name' signals

```shell
#!/bin/bash
#trap1.sh
trap 'exitprocess' 2
LOOP=0
function exitprocess()
{
    echo "You just hit <CTRL-C>,at number $LOOP, I will exit now."
    exit 1
}
while :
do 
    LOOP=$[$LOOP+1]
    echo $LOOP
done
```

## eval

Usage: eval [arg ...]

Excute arguments as a shell command

Example: eval "ls -l"

## logger

logger命令向/var/log/messages文件发送消息。

命令形式：logger -p -i "message"

-p: 优先级
-i：在每个消息中记录发送消息的进程号
