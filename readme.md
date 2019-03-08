
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

### 命令行中常用快捷键
* ctrl+a 光标移动到行首
* ctrl+e 光标移动到行尾
* ctrl+l 清屏相当于clear
* ctrl+u 删除到行首部
* ctrl+y 粘贴ctrl+u剪切的内容

### UUID（唯一标识符）冲突：
```
vi /etc/sysconfig/network-scripts/ifcfg-eth0
#删除MAC地址行
rm -rf /etc/udev/rules.d/70-persistent-net.rules
#删除MAC地址和UUID绑定文件
reboot
#重启Linux
```
本地图形终端 tty7  ctrl+alt+F7（按住三秒）

## 常见系统痕迹日志
* /var/log/wtmp 对应last命令，查询系统所有登录过的用户的信息
* /var/run/utmp 对应w,who命令
* /var/log/btmp  对应lastb，查询错误登录信息
* /var/log/lastlog 对应lastlog，查看所有用户的最后一次登录信息

load average 按照经验值不应该超过服务器CPU总核数。

计算机的70/90原则指，cpu不超过70%，内存不超过90%。

光盘设备文件名，Centos5.x以前是/dev/hdc, Centos6.x以后是/dev/sr0

U盘挂载，通过fdisk -l来查看usb设备，对于FAT32需要指定vfat，还要中文编码utf8，mount -t vfat -o iocharset=utf8 usb设备 /dev/usb/ 

## Linux的驱动加载顺序：
1. 驱动直接放入内核中，这种驱动主要是系统启动加载需要的内存，数量较少。
2. 驱动以模块的形式放入硬盘，大多数驱动都以这种方式保存，保存位置/lib/modules/kernelid/kernel/ 以.ko文件保存。
3. 驱动可以被Linux识别，但是系统认为这种驱动一般不常用，默认不加载。如果需要加载这种驱动，需要重新编译内核，而NTFS文件系统的驱动就属于这种情况。
4. 硬件不能被Linux内核识别，需要手工安装驱动。当然前提是厂商提供了该硬件针对Linux的驱动，否则就需要自己开发驱动了。

## 使用NTFS-3G安装NTFS文件系统模块
* 下载NTFS-3G插件，我们从网站http://www.tuxera.com/community/ntfs-3g-download/下载NTFS-3G插件到linux服务器上。
* 安装NTFS-3G插件，安装命令如下，要保证gcc编译器已经安装
```
tar -zxvf ntfs-3g_ntfsprogs-2013.1.13.tgz
#解压
cd ntfs-3g_ntfsprogs-2013.1.13
#进入解压目录
./configure
#编译器准备。没有指定安装目录，安装到默认位置中
make
#编译
make install
#编译安装
* 安装完就可以挂载使用Windows的NTFS分区了，不过挂载分区是文件系统不是ntfs，而是ntfs-3g。挂载命令如下：
```
mount -t ntfs-3g 分区设备文件名　挂载点

## vi
* a追加，i插入，o在下面。
* wq!强制保存退出，当文件的所有者或者root用户，对文件没有写权限的时候，强制写入数据。
* 退出ZZ。
* ^移动到行首，$移动到行尾,同正则。
* ：n移动到第几行。x删除字母，nx删除n个字母。
* dd删除行或者剪切,ndd删除多行或者剪切，：n1,n2d删除指定行，yy复制行，nyy复制多行
* p在下面粘贴，P在上面粘贴
* dG从当前行删除到文件首
* u撤销，Ctrl+r反撤销
* r替换光标所在处字符，R进入替换模式，从光标处开始替换，ESC退出 
* :set nu或:set nonu 显示或隐藏行号
* :syntax on或:syntax off 显示语法颜色
* :set hlsearch或set nohlsearch 是否高亮显示搜索
* :set ruler或:set noruler 设置是否显示右下角的状态栏。默认是:set ruler显示
* :set showmode或:set noshowmode 设置是否显示左下角的状态栏。默认是:set showmode
* :set list或:set nolist 设置是否显示隐藏字符（Tab键用“^I”表示，回车符用”$“表示）。默认是nolist，类似cat -A 文件名。
* / 查找内容，从光标所在行向下查找，? 查找内容，从光标所在行向上查找
* :1,10s/old/new/g 替换1到10行的所有old为new，:%s/old/new/g 替换真个文件的old为new，批量注释:1,10s/^/#/g，批量取消注释:1,10s/^#//g，在C或者PHP等语言中，使用“//”开头作为注释，批量注释:1,10s/^/\/\//g，批量取消注释:1,10s/^\/\///g
* :r filename 导入其他文件的内容
* :! 在vim中执行系统命令
* :r !命令 导入命令的执行结果
* :map 快捷键 快捷键执行的命令，自定义快捷键，常用的自定义快捷键有:map ^P I#<ESC> 按住ctrl+p时，在行首加入注释，:map ^B ^x，按住ctrl+b删除行首第一个字母（删除注释）,注意^p不能手工输入，需要ctrl+v，然后ctrl+p，^b也是一样。而且如果需要永久生效，需要写入配置文件~/.vimrc
* 字符替换 :ab 原字符 替换字符，比如 :ab mymail liumingxiang@qq.com 注意原字符不可以太短
* 多文件打开，vim -o abc bcd上下分屏打开两个文件，vim -O abc bcd 左右分屏打开两个文件，如果时上下打开，可以通过先按ctrl+w，再按上下箭头来切换，如果时左右，可以通过先按ctrl+w，再按左右箭头来切换。

vim支持更多设置参数，可通过:set all查看。如果需要永久生效，需要手工建立~/.vimrc，把参数写入配置文件。

补充：windows下回车符在linux中是用”^M$“符号显示，而不是”$“。这会导致windows编辑的程序脚本，无法在linux中执行。这是可以通过命令dos2unix，把windows格式转为linux格式，反过来unix2dos。这两个命令默认没有安装，需要手工安装才能使用。

## 软件包
### 源码包
* 可以自由选择所需功能
* 软件是编译安装，所有更加适合自己的系统，更加稳定也效率更高。源码包比二进制包效率大概要高5%
* uninstall more conveniently, 删掉目录基本就没有残余了
* have more steps of installing process, especially when installing big software(如LAMP环境搭建), 容易出现错误。
* 编译时间较长，比二进制安装时间长，gentoo linux使用纯源码包安装，需要3天左右。250m的mysql大概要半小时。
* 编译安装一旦出错，难以解决
### 二进制包
#### 二进制包分类
* DPKG包，是由Debian所开发的包管理机制，通过dpkg包，debian就可以进行软件包管理。主要Debian和ubuntu使用
* RPM包，是由red hat开发的包管理系统。fedora，centos，suse等使用。
#### 特点
* 包管理系统简单，安装速度比源码包安装快
* 编译后无法看到源代码，功能选择不灵活，具有依赖性。

选择建议：服务提供大量用户访问，建议源码包，源码包效率更高（LAMP）。
### RPM包依赖
1. 树形依赖 a->b->c
2. 环形依赖 a->b->c->a 将abc一起安装就行
3. 模块依赖（函数库依赖）  查询函数库属于哪个包的网址www.rpmfind.net

避免依赖性：通过yum在线安装,redhat收费，centos免费，也可以通过光盘搭建本地yum源

## rpm安装
### rpm包命名规则
httpd-2.2.15-15.el6.centos.1.i686.rpm
* httpd 软件包名 
* 2.2.15 软件版本
* 15 软件发布次数
* el6 版本发行商，el6是redhat公司发布，适合RHEL6.x和CentOS6.x
* i686 适合的硬件平台，RPM包可以在不同平台安装，i386,i586,i686（奔腾II以上计算机都可以安装，目前所有CPU均为奔腾II以上，所以这个版本居多），x86_64（64位CPU可以安装）和noarch（没有硬件限制）

包全名：如果操作的是未安装软件包，则使用包全名，而且需要注意绝对路径。

包名：如果操作的是已经安装的软件包，则使用包名即可，系统会产生RPM包的数据库/var/lib/rpm,而且可以在任意路径下操作。
### rpm包手工命令安装
#### 默认安装位置
| directory | meaning |
| --- | --- |
| /etc/ | 配置文件安装目录 |
| /usr/bin/ | 可执行的命令安装目录 |
| /usr/lib/ | 程序所使用的函数库保存位置 |
| /usr/share/doc | 基本的软件使用手册保存位置 |
| /usr/share/man | 帮助文件保存位置 |
#### RPM包安装
> rpm -ivh 包全名
>
> 注意一定是包全名，如果跟包全名的命令要注意路径
>
> -i install安装
>
> -v 显示更详细的信息
>
> -h 显示安装进度hash
