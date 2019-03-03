
MAC Media Access Control

ARP Address Resolve Protocal

Socket  ip:port

OSI

TCP/IP

MTU

TTL Time-To-Live

TCP Transmission Control Protocal
UDP User Datagram Protocal

DHCP Dynamic Host Configuration Protocal

/etc/sysconfig/network-scripts/ifcfg-eth0
/etc/sysconfig/network-scripts/route-eth0
/etc/resolv.conf
/etc/hosts
/etc/sysconfig/network

usr universal shared read-only

/bin /sbin
/lib
/etc
/usr/share/man

/usr/bin /usr/sbin /usr/lib /usr/etc

/usr/local/bin /usr/local/sbin /usr/local/lib /usr/local/etc /usr/local/man

Redhat SUSE : RPM (Redhat Package Manager) , (RPM is Package Manager)
Debian : dpt (debian package tools)

yum : Yellowdog Update Modifier
apt-get 

yum repository

createrepo

XML eXtended Mark Language
JSON 

meta data
primary.xml.gz

/etc/yum.conf
/etc/yum.repos.d/

yum repolist 
yum install -y 
yum install --nogpgcheck

yum localinstall [--nogpgcheck] filename

gcc GNU C Complier,  C
g++ C++

make : project management tool 
	makefile : define how make to complie source

automake --> makefile.in
autoconf --> configure

make install


compile tree steps:
# tar
# cd
./configure
	--help
	--prefix=/path/to/somewhere
	--sysconfdir=/path/to/conffile
	function : 1. choose compile functions 2. check environment
# make
# make install


tar xvf tengine-1.4.2.tar.gz
cd tengine-1.4.2
./configure --prefix=/usr/local/tengine --conf-path=/etc/tengine/tengine.conf
make
make install
/usr/local/tengine/sbin/nginx
	/etc/profile
	PATH=$PATH:/usr/local/tengine/sbin


1 PATH 
	/etc/profile
	/etc/profile.d  xxx.sh export PATH=$PATH:/path/to/somewhere
2 /lib /usr/lib  
	/etc/ld.so.conf.d/xxx.conf
	ldconfig -v : inform system to research library files
3 /usr/include
	ln -s /usr/local/tengine/include/* /usr/include/
	ln -s /usr/local/tengine/include /usr/include/tengine
4 /usr/share/man
	man -M /path/to/man_dir command
	/etc/man.config MANPATH

httpd
apachectl start

while usage 1
while :;do

done

while usage 2
while read LINE; do

done < /path/to/somefile

task structure

MMU : Memory Management Unit

TLB : 

Context Switch

vsz : virtual size
rss : resident size

process
tread

Linux Process/Tread Model

Stop
Ready
Executing
Sleep
	Uninterruptible sleep
	Interruptible sleep
Zombie

pstree

O
	O(1)
	O(n)
	O(logn)
	O(n^2)
	O(2^x)

0~99

100~139
	nice value : -20 ~ 19

PID : Process ID 


ps : process state
	BSD style : 
	a : list all processes with a terminal 
	u : 
	x : list all process without a terminal
	
	SysV styel :
	-ef
	
process status:

	D: uninterruptible sleep
	R: executing or ready
	S: interruptible sleep
	T: stop
	Z: zombie

pstree;gprep;pidof;top

IPC Inter Process Communication
	memory shared
	signal
	semaphore

kill -l
	1: SIGHUP
	2: SIGINT
	9: SIGKILL
	15:SIGTERM  

kill PID

killall COMMAND

nice
	renice NI PID
	nice -n NI COMMAND
free

pkill

bg JOBID
Ctrl+z
COMMAND &
fg JOBID
Kill %JOBID

vmstat

uptime

cat /proc/meminfo

cat /proc/cpuinfo

cat /proc/x/maps

alias配置文件在~/.bashrc

常用快捷键
	ctrl+a 光标移动到行首
	ctrl+e 光标移动到行尾
	ctrl+l 清屏相当于clear
	ctrl+u 删除到行首部

ctrl+y 粘贴ctrl+u剪切的内容

UUID（唯一标识符）冲突：

	vi /etc/sysconfig/network-scripts/ifcfg-eth0
	#删除MAC地址行
	rm -rf /etc/udev/rules.d/70-persistent-net.rules
	#删除MAC地址和UUID绑定文件
	reboot
	#重启Linux

本地图形终端 tty7  ctrl+alt+F7（按住三秒）

## 常见系统痕迹日志
* /var/log/wtmp 对应last命令，查询系统所有登录过的用户的信息
* /var/run/utmp 对应w,who命令
* /var/log/btmp  对应lastb，查询错误登录信息
* /var/log/lastlog 对应lastlog，查看所有用户的最后一次登录信息

load average 按照经验值不应该超过服务器CPU总核数。

计算机的70/90原则指，cpu不超过70%，内存不超过90%。

光盘设备文件名，Centos5.x以前是/dev/hdc, Centos6.x以后是/dev/sr0


