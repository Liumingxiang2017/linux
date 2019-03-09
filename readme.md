
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
#### RPM包手工安装
rpm -ivh 包全名
```
注意一定是包全名，如果跟包全名的命令要注意路径

* -i install安装
* -v 显示更详细的信息
* -h 显示安装进度hash
* -nodeps 不检测依赖性，不建议这么做
* --force 强制安装。不管是否已经安装，都强制重新安装。为了弥补重要文件丢失的情况，卸载再安装可能会把已经配好的文件。
* --test 只检测依赖性
* --prefix 指定安装路径，不建议使用
```
##### RPM包安装的Apache
1. 启动
	* service httpd start|stop|restart|status
	* 所有执行文件都需要绝对路径，服务也是如此，/etc/rc.d/init.d/httpd  start|stop|restart|status，其中 /etc/rc.d/init.d/httpd=/etc/init.d/httpd
2. 网页位置 
	/var/www/html/, 添加index.html文件，不需要重启服务，是否需要重启看是否修改了配置文件，此处只是修改网页文件，并不影响配置。
3. 配置文件
	/etc/httpd/conf/httpd.conf
4. 安装顺序
	1. httpd-tools-2.2.15
	2. httpd-2.2.15
	3. httpd-manual-2.2.15
	4. httpd-devel-2.2.15
##### RPM包建议安装在默认路径中（必须） 
1. 默认安装位置是系统的习惯位置 
2. RPM包管理系统是有卸载命令的（数据库记录安装位置，-e就可以完全卸载），但源码包必须指定位置，虽然也有默认位置，但是没有数据库，没有卸载命令，而是通过rm来删除目录。 

#### RPM包升级
```
rpm -Uvh 包全名

-U 升级安装，如果没有安装过，系统直接安装。如果安装过的版本较旧，则升级到新版本（Upgrade）

rpm -Fvh packageFullName

-F 升级安装，如果没有安装过，则不会安装。必须安装过较旧版本，才能升级（freshen）
```
#### 卸载
```
rpm -e 包名

卸载顺序和安装顺序相反，卸载依然有依赖性。另外初学者不建议使用yum直接卸载，建议rpm一个一个卸载。

--nodeps 不检测依赖性，生产环境不可以使用。

-e 卸载
```
#### 查询
rpm安装，升级，卸载，都可以用yum替代，但查询不一样,rpm -q 查询的是本地，yum查询的是服务器
* 查询软件包否安装
```
rpm -q 包名 

-q 查询（query）
```
* 查询系统中所有的安装软件包
```
rpm -qa

选项：-a 所有（all）
```
当然可以使用管道符查询某个包，rpm -qa | grep httpd
* 查询已安装软件包的详细信息
```
rpm -qi 包名

查询软件包详细信息-i information
``` 
* 查询未安装软件包的详细信息
```
rpm -qip packageFullName

选项：-p package
```
* 查询软件包中的文件列表

可以查询已经安装的软件包的文件列表和完整的安装目录。
```
rpm -ql packageName

选项： -l 列出软件包中所有的文件列表和软件所安装的目录（list）
```
也可以查询未安装的软件保的文件列表和打算安装的位置
```
rpm -qlp packageFullName

option: -p package
```
* 查询系统文件属于哪个RPM包
```
rpm -qf systemFileName

option: -f 查询系统文件file属于哪个软件包
```
* 查询软件包所依赖的软件包(不太常用，因为该命令不区分已安装包和未安装包)
```
rpm -qR packageName

option: -R requires
```
#### 验证
```
rpm -Va

	option: -Va 校验本机已经安装的所有软件包

rpm -V installedPackageName

	option: -V verify校验指定RPM包中的文件

rpm -Vf systemFileName

	option: -Vf 校验某个系统文件是否被修改 
```
##### 验证举例
```
rpm -V httpd
S.5....T.      c      /etc/httpd/conf/httpd.conf
验证内容     文件类型     文件名
```
文件类型
* c 表示配置文件config file
* d 普通文档 documentation
* g 鬼文件 ghost file，很少见，就是该文件不应该被这个RPM包包含
* l 授权文件 license file
* r 描述文件 readme
验证内容
* S 文件大小是否改变 size
* M 文件类型或者文件权限（rwx）是否改变
* 5 MD5校验和是否改变（可以看成文件内容是否改变，MD5是一种加密方式，也可以用来做完整性校验
* D 设备的主从代码是否改变 Device
* L 文件路径是否改变 
* U 文件属主是否改变 User
* G 文件的属组是否改变 Group
* T 文件的修改时间时否改变 

#### 校验证书
上面的校验方法只能对已经安装的RPM包中的文件进行校验，但是如果RPM包本身就被动过手脚，那么校验就不能解决问题了。我们就必须使用校验证书验证。

校验证书有如下特点：
* 首先必须找到原厂的公钥文件，然后进行安装。
* 再安装RPM包，会去提取RPM包中的证书信息，然后和本机安装的原厂证书进行校验。
* 如果验证通过，则允许安装；如果验证不通过，则不允许安装并警告。

1. 校验证书位置
那么校验证书再哪里呢，其实CentOS 6.3的第一张光盘中就有, RM-GPG-KEY-CentOS-6，另外默认也会放在系统中/etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-6

建立一个服务器管理手册，诸如配IP，配防火墙，导入数字证书，做一些关闭服务，做一些优化。
2. 数字证书导入
```
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-6

option: --import 导入数字证书
```
3. 查询安装好的数字证书(重要)
```
rpm -qa | grep gpg-pubkey
gpg-pubkey-c105b9de-4e0fd3a3
```
#### RRM包中文件的提取
##### cpio命令
原本该命令时用于备份还原，但是实际中完全不用做备份还原，但RPM包中文件的提取，必须使用cpio命令。cpio 命令主要有三种基本模型；”-o“模式指的时copy-out模式，就是把数据备份到文件库中; ”-i“模式指的是copy-in模式，就是把数据从文件库中恢复; ”-p“模式指的是复制模式，就是不把数据备份到cpio库，而是直接复制为其他文件。命令如下：
```
cpio -o[vcB] > [文件][设备]

#备份

option:
* -o copy-out模式，备份
* -v 显示备份过程
* -c 使用较新的portable format存储方式
* -B 设定输入输出块为5120bytes，而不是模式的512bytes

cpio -i[vcdu] < [文件|设备]

#还原

option:
* -i copy-in模式，还原
* -v 显示还原过程
* -c 使用较新的portable format存储模式
* -d 还原时自动新建目录
* -u 自动使用较新的文件覆盖较旧的文件

cpio -p 目标目录

* 利用find命令找到文件，备份
find /etc/ -print | cpio -ovcB > /root/etc.cpio

#find指定要备份/etc/目录，使用>导入/etc.cpio文件

* 恢复cpio的备份数据
cpio -idvcu < /root/etc.cpio
```
##### 提取RPM包中的文件
```
rpm2cpio packageFullName | cpio -idv .文件绝对路径

option:
* rpm2cpio 将rpm包转换为cpio格式的命令
* cpio 是一个标准工具，用于创建软件档案文件，和从档案文件中提取文件
```

# RPM包在线安装（yum安装）
## yum文件解析
yum源配置文件保存再/etc/yum/repos.d/目录中，文件扩展名一定是.repo。

CentOS-Base.repo中的base容器解析：
* [base] 容器名称，一定要放在[]中
* name 容器说明，可以自己随便写
* mirrorlist 镜像站点，这个可以注释掉
* baseurl 我们yum原服务器的地址。默认是CentOS官方的yum源服务器，是可以使用的。如果觉得慢，可以改成自己喜欢的yum源地址。
* enabled 此容器是否生效，如果不写或写成enabled=1则表示此容器生效，写成enabled=0则表示此容器不生效
* gpgcheck 如果为1表示RPM的数字证书生效，如果为0表示RMP数字证书不生效
* gpgkey 数字证书的公钥文件保存位置，不用修改。
## 搭建本地光盘yum源
1. 第一步：放入CentOS安装光盘，并挂载到指定位置
```
mkdir /mnt/cdrom 
#创建cdrom目录，作为光盘挂载点
mount /dev/cdrom /mnt/cdrom
#挂载光盘到/mnt/cdrom目录下
```
2. 第二步：修改其他几个yum源配置文件的扩展名，让其失效。因为只有扩展名为.repo的文件才能作为yum源配置文件。当然可以删除其他几个yum源配置程序，但是如果删除了，又想用网络作为yum源时，就没有参考文件了。
```
cd /etc/yum.repos.d/
mv CentOS-Base.repo CenOS-Base.repo.bak
mv CentOS-Debuginfo.repo CenOS-Debuginfo.repo.bak
mv CentOS-Vault.repo CentOS-Vault.repo.bak
```
3. 第三步：修改光盘yum源文件CentOS-Media.repo，参照一下方法修改
```
[c6-media]
name=CentOS-$releasever-Media
baseurl=file:///mnt/cdrom
#地址为自己光盘挂载地址
#       file:///media/cdrom/
#       file:///media/cdrecorder
#注释这两个不存在的地址
gpgcheck=1
enabled=1
#把enabled=0改为1，让这个yum源配置文件生效
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-6
```
