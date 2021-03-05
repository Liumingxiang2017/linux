# samba 文件服务器

## 入门概述

### windows网上邻居

#### 工作原理

通过SMB协议共享传输文件，具有自己的主机名称解析系统(wins)。

SMB (Server Messsage Block)/CIFS (Common Internet File System)是基于Netbios协议的，所以不能跨越子网通信。

认证模式

工作组模式：用户账号密码存放在每台主机上，通过对方主机的认证授权。
域服务器模式：用户账号集中存放在域服务器，每台主机通过域服务器认证授权。

跟linux共享必须安装TCP/IP

直接输入\\server\sharename

#### 设置共享文件夹

1. 文件夹右键属性
2. 共享标签卡---高级共享---勾选共享此文件夹

#### 设置可访问用户

默认所有人都可以访问，删除everyone，然后指定用户权限。

1. 文件夹右键属性
2. 共享标签卡---高级共享---权限
3. 删除everyone---添加用户并指定权限

### Linux访问网上邻居

- 需要samba客户端
- 挂载

```shell
# 方式1
mount -t smbfs //server/sharename /localdir
# 方式2
smbmount //server/sharename /localname
```

- 使用smbclient

```shell
smbclient //server/sharename -U name%passwd
```

## samba工具集

samba软件与工具介绍

samba为windows提供共享

安全级别

用户账号与认证

samba项目开发 http://www.samba.org

相关软件包

samba 服务器软件包
samba-client 客户端工具
samba-common 通用工具和库

## 安装Samba软件包

安装samba软件包

    rpm -ivh --aid samba*.rpm

检查软件包内容

    rpm -ql samba | more
    rpm -ql samba-common | more
    rpm -ql samba-client | more

    启动脚本 /etc/rc.d/init.d/smb

## Samba客户端工具

smbtree

作用：显示局域网中所有共享主机和目录列表

用法：smbtree [-b] [-D] [-U username%password]

nmblookup

作用：显示一台主机的netbios主机名

smbclient

作用：显示/登录共享局域网中的共享文件夹

用法：

    smbclient -L host
    smbclient //HOST/SHARE

smbtar

作用：远程备份网上邻居中的文件
用法：

    smbtar -s SERVER -u USER -p PASSWORD -x SHARENAME -t output
    
    smbtar -s win2000 -u redhat -p redhat -x lmxshare -t lmxshare.tar

smbmount

作用：挂载远程目录，之后类似于磁盘映射

smbmount //host/share /mnt -o username=USERNAME%PASSWORD

## Samba服务器配置

修改配置文件/etc/samba/smb.conf

    workgroup = WORKGROUP
    security = share
    [docs]
        path = /usr/share/doc
        comment = share documents
        public = yes

重启smb服务器

    service smb restart
    chkconfig smb on

测试

    smbclient -L localhost

本章目录结构 

12.1 SAMBA文件共享服务
12.1.1 配置共享资源
12.1.2 Windows挂载共享
12.1.3 Linux挂载共享
12.2 NFS网络文件系统
12.3 AutoFs自动挂载服务
12.1 SAMBA文件共享服务

FTP文件传输服务确实可以让主机之间的文件传输变得简单方便，但是FTP协议的本质是传输文件，而非共享文件，因此要想通过客户端直接在服务器上修改文件内容还是一件比较麻烦的事情。

1987年，微软公司和英特尔公司共同制定了SMB（Server Messages Block，服务器消息块）协议，旨在解决局域网内的文件或打印机等资源的共享问题，这也使得在多个主机之间共享文件变得越来越简单。到了1991年，当时还在读大学的Tridgwell为了解决Linux系统与Windows系统之间的文件共享问题，基于SMB协议开发出了SMBServer服务程序。这是一款开源的文件共享软件，经过简单配置就能够实现Linux系统与Windows系统之间的文件共享工作。当时，Tridgwell想把这款软件的名字SMBServer注册成为商标，但却被商标局以SMB是没有意义的字符而拒绝了申请。后来Tridgwell不断翻看词典，突然看到一个拉丁舞蹈的名字—Samba，而且这个热情洋溢的舞蹈名字中又恰好包含了“SMB”，于是Samba服务程序的名字由此诞生（见图12-1）。Samba服务程序现在已经成为在Linux系统与Windows系统之间共享文件的最佳选择。

图12-1  Samba服务程序的logo

Samba服务程序的配置方法与之前讲解的很多服务的配置方法类似，首先需要先通过Yum软件仓库来安装Samba服务程序（Samba服务程序的名字也恰巧是软件包的名字）：

```shell
[root@linuxprobe ~ ]# yum install samba
Loaded plugins: langpacks, product-id, subscription-manager
………………省略部分输出信息………………
Installing:
 samba x86_64 4.1.1-31.el7 rhel 527 k
Transaction Summary
================================================================================
Install 1 Package
Total download size: 527 k
Installed size: 1.5 M
Is this ok [y/d/N]: y
Downloading packages:
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
 Installing : samba-4.1.1-31.el7.x86_64 1/1 
 Verifying : samba-4.1.1-31.el7.x86_64 1/1 
Installed:
 samba.x86_64 0:4.1.1-31.el7 
Complete!
```

安装完毕后打开Samba服务程序的主配置文件，发现竟然有320行之多！有没有被吓到？但仔细一看就会发现，其实大多数都是以井号（#）开头的注释信息行。有刘遄老师在，肯定是不会让大家去“死啃”这些内容的。

```shell
[root@linuxprobe ~]# cat /etc/samba/smb.conf 
# This is the main Samba configuration file. For detailed information about the
# options listed here, refer to the smb.conf(5) manual page. Samba has a huge
# number of configurable options, most of which are not shown in this example.
#
# The Official Samba 3.2.x HOWTO and Reference Guide contains step-by-step
# guides for installing, configuring, and using Samba:
# http://www.samba.org/samba/docs/Samba-HOWTO-Collection.pdf
#
# The Samba-3 by Example guide has working examples for smb.conf. This guide is
# generated daily: http://www.samba.org/samba/docs/Samba-Guide.pdf
#
# In this file, lines starting with a semicolon (;) or a hash (#) are
# comments and are ignored. This file uses hashes to denote commentary and
# semicolons for parts of the file you may wish to configure.
#
# Note: Run the "testparm" command after modifying this file to check for basic
# syntax errors.
#
………………省略部分输出信息………………
```

由于在Samba服务程序的主配置文件中，注释信息行实在太多，不便于分析里面的重要参数，因此先把主配置文件改个名字，然后使用cat命令读入主配置文件，再在grep命令后面添加-v参数（反向选择），分别去掉所有以井号（#）和分号（;）开头的注释信息行，对于剩余的空白行可以使用^$参数来表示并进行反选过滤，最后把过滤后的可用参数信息通过重定向符覆盖写入到原始文件名称中。执行过滤后剩下的Samba服务程序的参数并不复杂，为了更方便读者查阅参数的功能，表12-1罗列了这些参数以及相应的注释说明。

表12-1    Samba服务程序中的参数以及作用

```shell
[global]		#全局参数。
workgroup = MYGROUP	#工作组名称
server string = Samba Server Version %v	#服务器介绍信息，参数%v为显示SMB版本号
log file = /var/log/samba/log.%m	#定义日志文件的存放位置与名称，参数%m为来访的主机名
max log size = 50	#定义日志文件的最大容量为50KB
security = user	#安全验证的方式，总共有4种
#share：来访主机无需验证口令；比较方便，但安全性很差
#user：需验证来访主机提供的口令后才可以访问；提升了安全性
#server：使用独立的远程主机验证来访主机提供的口令（集中管理账户）
#domain：使用域控制器进行身份验证
passdb backend = tdbsam	#定义用户后台的类型，共有3种
#smbpasswd：使用smbpasswd命令为系统用户设置Samba服务程序的密码
#tdbsam：创建数据库文件并使用pdbedit命令建立Samba服务程序的用户
#ldapsam：基于LDAP服务进行账户验证
load printers = yes	#设置在Samba服务启动时是否共享打印机设备
cups options = raw	#打印机的选项
[homes]		#共享参数
comment = Home Directories	#描述信息
browseable = no	#指定共享信息是否在“网上邻居”中可见
writable = yes	#定义是否可以执行写入操作，与“read only”相反
[printers]		#打印机共享参数
comment = All Printers	
path = /var/spool/samba	#共享文件的实际路径(重要)。
browseable = no	
guest ok = no	#是否所有人可见，等同于"public"参数。
writable = no	
printable = yes	
```

```shell
[root@linuxprobe ~]# mv /etc/samba/smb.conf /etc/samba/smb.conf.bak
[root@linuxprobe ~]# cat /etc/samba/smb.conf.bak | grep -v "#" | grep -v ";" | grep -v "^$" > /etc/samba/smb.conf
[root@linuxprobe ~]# cat /etc/samba/smb.conf
```

### 配置共享资源

Samba服务程序的主配置文件与前面学习过的Apache服务很相似，包括全局配置参数和区域配置参数。全局配置参数用于设置整体的资源共享环境，对里面的每一个独立的共享资源都有效。区域配置参数则用于设置单独的共享资源，且仅对该资源有效。创建共享资源的方法很简单，只要将表12-2中的参数写入到Samba服务程序的主配置文件中，然后重启该服务即可。

表12-2    用于设置Samba服务程序的参数以及作用

参数	作用
[database]	共享名称为database
comment = Do not arbitrarily modify the database file	警告用户不要随意修改数据库
path = /home/database	共享目录为/home/database
public = no	关闭“所有人可见”
writable = yes	允许写入操作
第1步：创建用于访问共享资源的账户信息。在RHEL 7系统中，Samba服务程序默认使用的是用户口令认证模式（user）。这种认证模式可以确保仅让有密码且受信任的用户访问共享资源，而且验证过程也十分简单。不过，只有建立账户信息数据库之后，才能使用用户口令认证模式。另外，Samba服务程序的数据库要求账户必须在当前系统中已经存在，否则日后创建文件时将导致文件的权限属性混乱不堪，由此引发错误。

pdbedit命令用于管理SMB服务程序的账户信息数据库，格式为“pdbedit [选项] 账户”。在第一次把账户信息写入到数据库时需要使用-a参数，以后在执行修改密码、删除账户等操作时就不再需要该参数了。pdbedit命令中使用的参数以及作用如表12-3所示。

表12-3                                       用于pdbedit命令的参数以及作用

参数	作用
-a 用户名	建立Samba用户
-x 用户名	删除Samba用户
-L	列出用户列表
-Lv	列出用户详细信息的列表

```shell
[root@linuxprobe ~]# id linuxprobe
uid=1000(linuxprobe) gid=1000(linuxprobe) groups=1000(linuxprobe)
[root@linuxprobe ~]# pdbedit -a -u linuxprobe
new password:此处输入该账户在Samba服务数据库中的密码
retype new password:再次输入密码进行确认
Unix username: linuxprobe
NT username: 
Account Flags: [U ]
User SID: S-1-5-21-507407404-3243012849-3065158664-1000
Primary Group SID: S-1-5-21-507407404-3243012849-3065158664-513
Full Name: linuxprobe
Home Directory: \\localhost\linuxprobe
HomeDir Drive: 
Logon Script: 
Profile Path: \\localhost\linuxprobe\profile
Domain: LOCALHOST
Account desc: 
Workstations: 
Munged dial: 
Logon time: 0
Logoff time: Wed, 06 Feb 2036 10:06:39 EST
Kickoff time: Wed, 06 Feb 2036 10:06:39 EST
Password last set: Mon, 13 Mar 2017 04:22:25 EDT
Password can change: Mon, 13 Mar 2017 04:22:25 EDT
Password must change: never
Last bad password : 0
Bad password count : 0
Logon hours : FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
```

第2步：创建用于共享资源的文件目录。在创建时，不仅要考虑到文件读写权限的问题，而且由于/home目录是系统中普通用户的家目录，因此还需要考虑应用于该目录的SELinux安全上下文所带来的限制。在前面对Samba服务程序配置文件中的注释信息进行过滤时，这些过滤的信息中就有关于SELinux安全上下文策略的说明，我们只需按照过滤信息中有关SELinux安全上下文策略中的说明中给的值进行修改即可。修改完毕后执行restorecon命令，让应用于目录的新SELinux安全上下文立即生效。

```shell
[root@linuxprobe ~]# mkdir /home/database
[root@linuxprobe ~]# chown -Rf linuxprobe:linuxprobe /home/database
[root@linuxprobe ~]# semanage fcontext -a -t samba_share_t /home/database
[root@linuxprobe ~]# restorecon -Rv /home/database
restorecon reset /home/database context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:samba_share_t:s0
```

第3步：设置SELinux服务与策略，使其允许通过Samba服务程序访问普通用户家目录。执行getsebool命令，筛选出所有与Samba服务程序相关的SELinux域策略，根据策略的名称（和经验）选择出正确的策略条目进行开启即可：

```shell
[root@linuxprobe ~]# getsebool -a | grep samba
samba_create_home_dirs --> off
samba_domain_controller --> off
samba_enable_home_dirs --> off
samba_export_all_ro --> off
samba_export_all_rw --> off
samba_portmapper --> off
samba_run_unconfined --> off
samba_share_fusefs --> off
samba_share_nfs --> off
sanlock_use_samba --> off
use_samba_home_dirs --> off
virt_sandbox_use_samba --> off
virt_use_samba --> off
[root@linuxprobe ~]# setsebool -P samba_enable_home_dirs on
```

第4步：在Samba服务程序的主配置文件中，根据表12-2所提到的格式写入共享信息。在原始的配置文件中，[homes]参数为来访用户的家目录共享信息，[printers]参数为共享的打印机设备。这两项如果在今后的工作中不需要，可以像刘遄老师一样手动删除，这没有任何问题。

```shell
[root@linuxprobe ~]# vim /etc/samba/smb.conf 
[global]
 workgroup = MYGROUP
 server string = Samba Server Version %v
 log file = /var/log/samba/log.%m
 max log size = 50
 security = user
 passdb backend = tdbsam
 load printers = yes
 cups options = raw
[database]
 comment = Do not arbitrarily modify the database file
 path = /home/database
 public = no
 writable = yes
```

第5步：Samba服务程序的配置工作基本完毕。接下来重启smb服务（Samba服务程序在Linux系统中的名字为smb）并清空iptables防火墙，然后就可以检验配置效果了。

```shell
[root@linuxprobe ~]# systemctl restart smb
[root@linuxprobe ~]# systemctl enable smb
 ln -s '/usr/lib/systemd/system/smb.service' '/etc/systemd/system/multi-user.target.wants/smb.service'
[root@linuxprobe ~]# iptables -F
[root@linuxprobe ~]# service iptables save
iptables: Saving firewall rules to /etc/sysconfig/iptables:[ OK ]
```

### Windows挂载共享

无论Samba共享服务是部署Windows系统上还是部署在Linux系统上，通过Windows系统进行访问时，其步骤和方法都是一样的。下面假设Samba共享服务部署在Linux系统上，并通过Windows系统来访问Samba服务。Samba共享服务器和Windows客户端的IP地址可以根据表12-4来设置。

表12-4               Samba服务器和Windows客户端使用的操作系统以及IP地址

主机名称	操作系统	IP地址
Samba共享服务器	RHEL 7	192.168.10.10
Linux客户端	RHEL 7	192.168.10.20
Windows客户端	Windows 7	192.168.10.30
要在Windows系统中访问共享资源，只需在Windows的“运行”命令框中输入两个反斜杠，然后再加服务器的IP地址即可，如图12-2所示。

图12-2  在Windows系统中访问共享资源

如果已经清空了Linux系统上iptables防火墙的默认策略（即执行iptables -F命令），现在就应该能看到Samba共享服务的登录界面了。刘遄老师在这里先使用linuxprobe账户的系统本地密码尝试登录，结果出现了如图12-3所示的报错信息。由此可以验证，在RHEL 7系统中，Samba服务程序使用的果然是独立的账户信息数据库。所以，即便在Linux系统中有一个linuxprobe账户，Samba服务程序使用的账户信息数据库中也有一个同名的linuxprobe账户，大家也一定要弄清楚它们各自所对应的密码。

第12章 使用Samba或NFS实现文件共享。第12章 使用Samba或NFS实现文件共享。
图12-3  访问Samba共享服务时，提示出错

正确输入linuxprobe账户名以及使用pdbedit命令设置的密码后，就可以登录到共享界面中了，如图12-4所示。此时，我们可以尝试执行查看、写入、更名、删除文件等操作。

第12章 使用Samba或NFS实现文件共享。第12章 使用Samba或NFS实现文件共享。
图12-4  成功访问Samba共享服务

由于Windows系统的缓存原因，有可能您在第二次登录时提供了正确的账户和密码，依然会报错，这时只需要重新启动一下Windows客户端就没问题了（如果Windows系统依然报错，请检查上述步骤是否有做错的地方）。

### Linux挂载共享

上面的实验操作可能会让各位读者误以为Samba服务程序只是为了解决Linux系统和Windows系统的资源共享问题而设计的。其实，Samba服务程序还可以实现Linux系统之间的文件共享。请各位读者按照表12-5来设置Samba服务程序所在主机（即Samba共享服务器）和Linux客户端使用的IP地址，然后在客户端安装支持文件共享服务的软件包（cifs-utils）。

表12-5           Samba共享服务器和Linux客户端各自使用的操作系统以及IP地址

主机名称	操作系统	IP地址
Samba共享服务器	RHEL 7	192.168.10.10
Linux客户端	RHEL 7	192.168.10.20
Windows客户端	Windows 7	192.168.10.30

```shell
[root@linuxprobe ~]# yum install cifs-utils
Loaded plugins: langpacks, product-id, subscription-manager
rhel | 4.1 kB 00:00 
Resolving Dependencies
--> Running transaction check
---> Package cifs-utils.x86_64 0:6.2-6.el7 will be installed
--> Finished Dependency Resolution
Dependencies Resolved
================================================================================
 Package Arch Version Repository Size
================================================================================
Installing:
 cifs-utils x86_64 6.2-6.el7 rhel 83 k
Transaction Summary
================================================================================
Install 1 Package
Total download size: 83 k
Installed size: 174 k
Is this ok [y/d/N]: y
Downloading packages:
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
 Installing : cifs-utils-6.2-6.el7.x86_64 1/1 
 Verifying : cifs-utils-6.2-6.el7.x86_64 1/1 
Installed:
 cifs-utils.x86_64 0:6.2-6.el7 
Complete!
```

在Linux客户端，按照Samba服务的用户名、密码、共享域的顺序将相关信息写入到一个认证文件中。为了保证不被其他人随意看到，最后把这个认证文件的权限修改为仅root管理员才能够读写：

```shell
[root@linuxprobe ~]# vim auth.smb
username=linuxprobe
password=redhat
domain=MYGROUP
[root@linuxprobe ~]# chmod -Rf 600 auth.smb
```

现在，在Linux客户端上创建一个用于挂载Samba服务共享资源的目录，并把挂载信息写入到/etc/fstab文件中，以确保共享挂载信息在服务器重启后依然生效：

```shell
[root@linuxprobe ~]# mkdir /database
[root@linuxprobe ~]# vim /etc/fstab
#
# /etc/fstab
# Created by anaconda on Wed May 4 19:26:23 2017
#
# Accessible filesystems, by reference, are maintained under '/dev/disk'
# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
#
/dev/mapper/rhel-root / xfs defaults 1 1
UUID=812b1f7c-8b5b-43da-8c06-b9999e0fe48b /boot xfs defaults 1 2
/dev/mapper/rhel-swap swap swap defaults 0 0
/dev/cdrom /media/cdrom iso9660 defaults 0 0 
//192.168.10.10/database /database cifs credentials=/root/auth.smb 0 0
[root@linuxprobe ~]# mount -a
```

Linux客户端成功地挂载了Samba服务的共享资源。进入到挂载目录/database后就可以看到Windows系统访问Samba服务程序时留下来的文件了（即文件Memo.txt）。当然，我们也可以对该文件进行读写操作并保存。

```shell
[root@linuxprobe ~]# cat /database/Memo.txt
i can edit it .
```


## NFS网络文件系统

如果大家觉得Samba服务程序的配置太麻烦，而且恰巧需要共享文件的主机都是Linux系统，刘遄老师非常推荐大家在客户端部署NFS服务来共享文件。NFS（网络文件系统）服务可以将远程Linux系统上的文件共享资源挂载到本地主机的目录上，从而使得本地主机（Linux客户端）基于TCP/IP协议，像使用本地主机上的资源那样读写远程Linux系统上的共享文件。

由于RHEL 7系统中默认已经安装了NFS服务，外加NFS服务的配置步骤也很简单，因此刘遄老师在授课时会将NFS戏谑为Need For Speed。接下来，我们准备配置NFS服务。首先请使用Yum软件仓库检查自己的RHEL 7系统中是否已经安装了NFS软件包：

```shell
[root@linuxprobe ~]# yum install nfs-utils
Loaded plugins: langpacks, product-id, subscription-manager
(1/2): rhel7/group_gz | 134 kB 00:00
(2/2): rhel7/primary_db | 3.4 MB 00:00
Package 1:nfs-utils-1.3.0-0.el7.x86_64 already installed and latest version
Nothing to do
```

### 第1步：设置试验环境

为了检验NFS服务配置的效果，我们需要使用两台Linux主机（一台充当NFS服务器，一台充当NFS客户端），并按照表12-6来设置它们所使用的IP地址。

表12-6                             两台Linux主机所使用的操作系统以及IP地址

主机名称	操作系统	IP地址
NFS服务端	RHEL 7	192.168.10.10
NFS客户端	RHEL 7	192.168.10.20
另外，不要忘记清空NFS服务器上面iptables防火墙的默认策略，以免默认的防火墙策略禁止正常的NFS共享服务。

```shell
[root@linuxprobe ~]# iptables -F
[root@linuxprobe ~]# service iptables save
iptables: Saving firewall rules to /etc/sysconfig/iptables:[ OK ]
```

### 第2步：服务器建立共享目录

在NFS服务器上建立用于NFS文件共享的目录，并设置足够的权限确保其他人也有写入权限。

```shell
[root@linuxprobe ~]# mkdir /nfsfile
[root@linuxprobe ~]# chmod -Rf 777 /nfsfile
[root@linuxprobe ~]# echo "welcome to linuxprobe.com" > /nfsfile/readme
```

### 第3步：修改配置文件

NFS服务程序的配置文件为/etc/exports，默认情况下里面没有任何内容。我们可以按照“共享目录的路径 允许访问的NFS客户端（共享权限参数）”的格式，定义要共享的目录与相应的权限。

例如，如果想要把/nfsfile目录共享给192.168.10.0/24网段内的所有主机，让这些主机都拥有读写权限，在将数据写入到NFS服务器的硬盘中后才会结束操作，最大限度保证数据不丢失，以及把来访客户端root管理员映射为本地的匿名用户等，则可以按照下面命令中的格式，将表12-7中的参数写到NFS服务程序的配置文件中。

表12-7  用于配置NFS服务程序配置文件的参数

参数	作用
ro	只读
rw	读写
root_squash	当NFS客户端以root管理员访问时，映射为NFS服务器的匿名用户
no_root_squash	当NFS客户端以root管理员访问时，映射为NFS服务器的root管理员
all_squash	无论NFS客户端使用什么账户访问，均映射为NFS服务器的匿名用户
sync	同时将数据写入到内存与硬盘中，保证不丢失数据
async	优先将数据保存到内存，然后再写入硬盘；这样效率更高，但可能会丢失数据
请注意，NFS客户端地址与权限之间没有空格。

```shell
[root@linuxprobe ~]# vim /etc/exports
/nfsfile 192.168.10.*(rw,sync,root_squash)
```

### 第4步：启动服务

启动和启用NFS服务程序。由于在使用NFS服务进行文件共享之前，需要使用RPC（Remote Procedure Call，远程过程调用）服务将NFS服务器的IP地址和端口号等信息发送给客户端。因此，在启动NFS服务之前，还需要顺带重启并启用rpcbind服务程序，并将这两个服务一并加入开机启动项中。

```shell
[root@linuxprobe ~]# systemctl restart rpcbind
[root@linuxprobe ~]# systemctl enable rpcbind
[root@linuxprobe ~]# systemctl start nfs-server
[root@linuxprobe ~]# systemctl enable nfs-server
ln -s '/usr/lib/systemd/system/nfs-server.service' '/etc/systemd/system/nfs.target.wants/nfs-server.service'
```

NFS客户端的配置步骤也十分简单。先使用showmount命令（以及必要的参数，见表12-8）查询NFS服务器的远程共享信息，其输出格式为“共享的目录名称 允许使用客户端地址”。

表12-8    showmount命令中可用的参数以及作用

参数	作用
-e	显示NFS服务器的共享列表
-a	显示本机挂载的文件资源的情况NFS资源的情况
-v	显示版本号

```shell
[root@linuxprobe ~]# showmount -e 192.168.10.10
Export list for 192.168.10.10:
/nfsfile 192.168.10.*
```

然后在NFS客户端创建一个挂载目录。使用mount命令并结合-t参数，指定要挂载的文件系统的类型，并在命令后面写上服务器的IP地址、服务器上的共享目录以及要挂载到本地系统（即客户端）的目录。

```shell
[root@linuxprobe ~]# mkdir /nfsfile
[root@linuxprobe ~]# mount -t nfs 192.168.10.10:/nfsfile /nfsfile
```

挂载成功后就应该能够顺利地看到在执行前面的操作时写入的文件内容了。如果希望NFS文件共享服务能一直有效，则需要将其写入到fstab文件中：

```shell
[root@linuxprobe ~]# cat /nfsfile/readme
welcome to linuxprobe.com
[root@linuxprobe ~]# vim /etc/fstab 
#
# /etc/fstab
# Created by anaconda on Wed May 4 19:26:23 2017
#
# Accessible filesystems, by reference, are maintained under '/dev/disk'
# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
#
/dev/mapper/rhel-root / xfs defaults 1 1
UUID=812b1f7c-8b5b-43da-8c06-b9999e0fe48b /boot xfs defaults 1 2
/dev/mapper/rhel-swap swap swap defaults 0 0
/dev/cdrom /media/cdrom iso9660 defaults 0 0 
192.168.10.10:/nfsfile /nfsfile nfs defaults 0 0
```

## AutoFs自动挂载服务

无论是Samba服务还是NFS服务，都要把挂载信息写入到/etc/fstab中，这样远程共享资源就会自动随服务器开机而进行挂载。虽然这很方便，但是如果挂载的远程资源太多，则会给网络带宽和服务器的硬件资源带来很大负载。如果在资源挂载后长期不使用，也会造成服务器硬件资源的浪费。可能会有读者说，“可以在每次使用之前执行mount命令进行手动挂载”。这是一个不错的选择，但是每次都需要先挂载再使用，您不觉得麻烦吗？

autofs自动挂载服务可以帮我们解决这一问题。与mount命令不同，autofs服务程序是一种Linux系统守护进程，当检测到用户试图访问一个尚未挂载的文件系统时，将自动挂载该文件系统。换句话说，我们将挂载信息填入/etc/fstab文件后，系统在每次开机时都自动将其挂载，而autofs服务程序则是在用户需要使用该文件系统时才去动态挂载，从而节约了网络资源和服务器的硬件资源。

```shell
[root@linuxprobe ~]# yum install autofs
Loaded plugins: langpacks, product-id, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
rhel | 4.1 kB 00:00 
Resolving Dependencies
--> Running transaction check
---> Package autofs.x86_64 1:5.0.7-40.el7 will be installed
--> Processing Dependency: libhesiod.so.0()(64bit) for package: 1:autofs-5.0.7-40.el7.x86_64
--> Running transaction check
---> Package hesiod.x86_64 0:3.2.1-3.el7 will be installed
--> Finished Dependency Resolution
Dependencies Resolved
================================================================================
 Package Arch Version Repository Size
================================================================================
Installing:
 autofs x86_64 1:5.0.7-40.el7 rhel 550 k
Installing for dependencies:
 hesiod x86_64 3.2.1-3.el7 rhel 30 k
Transaction Summary
================================================================================
Install 1 Package (+1 Dependent package)
Total download size: 579 k
Installed size: 3.6 M
Is this ok [y/d/N]: y
Downloading packages:
--------------------------------------------------------------------------------
Total 9.4 MB/s | 579 kB 00:00 
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
 Installing : hesiod-3.2.1-3.el7.x86_64 1/2 
 Installing : 1:autofs-5.0.7-40.el7.x86_64 2/2 
 Verifying : hesiod-3.2.1-3.el7.x86_64 1/2 
 Verifying : 1:autofs-5.0.7-40.el7.x86_64 2/2 
Installed:
 autofs.x86_64 1:5.0.7-40.el7
Dependency Installed:
 hesiod.x86_64 0:3.2.1-3.el7
Complete!
```

处于生产环境中的Linux服务器，一般会同时管理许多设备的挂载操作。如果把这些设备挂载信息都写入到autofs服务的主配置文件中，无疑会让主配置文件臃肿不堪，不利于服务执行效率，也不利于日后修改里面的配置内容，因此在autofs服务程序的主配置文件中需要按照“挂载目录 子配置文件”的格式进行填写。挂载目录是设备挂载位置的上一级目录。例如，光盘设备一般挂载到/media/cdrom目录中，那么挂载目录写成/media即可。对应的子配置文件则是对这个挂载目录内的挂载设备信息作进一步的说明。子配置文件需要用户自行定义，文件名字没有严格要求，但后缀建议以.misc结束。具体的配置参数如第7行的加粗字所示。

```shell
[root@linuxprobe ~]# vim /etc/auto.master
#
# Sample auto.master file
# This is an automounter map and it has the following format
# key [ -mount-options-separated-by-comma ] location
# For details of the format look at autofs(5).
#
/media /etc/iso.misc
/misc /etc/auto.misc
#
# NOTE: mounts done from a hosts map will be mounted with the
# "nosuid" and "nodev" options unless the "suid" and "dev"
# options are explicitly given.
#
/net -hosts
#
# Include /etc/auto.master.d/*.autofs
#
+dir:/etc/auto.master.d
#
# Include central master map if it can be found using
# nsswitch sources.
#
# Note that if there are entries for /net or /misc (as
# above) in the included master map any keys that are the
# same will not be seen as the first read key seen takes
# precedence.
#
+auto.master
```

在子配置文件中，应按照“挂载目录 挂载文件类型及权限 :设备名称”的格式进行填写。例如，要把光盘设备挂载到/media/iso目录中，可将挂载目录写为iso，而-fstype为文件系统格式参数，iso9660为光盘设备格式，ro、nosuid及nodev为光盘设备具体的权限参数，/dev/cdrom则是定义要挂载的设备名称。配置完成后再顺手将autofs服务程序启动并加入到系统启动项中：

```shell
[root@linuxprobe ~]# vim /etc/iso.misc
# /media/iso目录缩写 -fstype=文件系统类型  硬件设备
# nosuid，nodev 如果文件由suid或者硬件设备不要加载，保证安全
# :/dev/cdrom :后面是设备
iso   -fstype=iso9660,ro,nosuid,nodev :/dev/cdrom
[root@linuxprobe ~]# systemctl start autofs
[root@linuxprobe ~]# systemctl enable autofs
ln -s '/usr/lib/systemd/system/autofs.service' '/etc/systemd/system/multi-user.target.wants/autofs.service'
```

接下来将发生一件非常有趣的事情。我们先查看当前的光盘设备挂载情况，确认光盘设备没有被挂载上，而且/media目录中根本就没有iso子目录。但是，我们却可以使用cd命令切换到这个iso子目录中，而且光盘设备会被立即自动挂载上。我们也就能顺利查看光盘内的内容了。

```shell
[root@linuxprobe ~]# df -h
Filesystem Size Used Avail Use% Mounted on
/dev/mapper/rhel-root 18G 3.0G 15G 17% /
devtmpfs 905M 0 905M 0% /dev
tmpfs 914M 140K 914M 1% /dev/shm
tmpfs 914M 8.9M 905M 1% /run
tmpfs 914M 0 914M 0% /sys/fs/cgroup
/dev/sda1 497M 119M 379M 24% /boot
[root@linuxprobe ~]# cd /media
[root@linuxprobe media]# ls
[root@linuxprobe media]# cd iso
[root@linuxprobe iso]# ls -l
total 812
dr-xr-xr-x. 4 root root 2048 May 7 2017 addons
dr-xr-xr-x. 3 root root 2048 May 7 2017 EFI
-r--r--r--. 1 root root 8266 Apr 4 2017 EULA
-r--r--r--. 1 root root 18092 Mar 6 2012 GPL
dr-xr-xr-x. 3 root root 2048 May 7 2017 images
dr-xr-xr-x. 2 root root 2048 May 7 2017 isolinux
dr-xr-xr-x. 2 root root 2048 May 7 2017 LiveOS
-r--r--r--. 1 root root 108 May 7 2017 media.repo
dr-xr-xr-x. 2 root root 774144 May 7 2017 Packages
dr-xr-xr-x. 24 root root 6144 May 7 2017 release-notes
dr-xr-xr-x. 2 root root 4096 May 7 2017 repodata
-r--r--r--. 1 root root 3375 Apr 1 2017 RPM-GPG-KEY-redhat-beta
-r--r--r--. 1 root root 3211 Apr 1 2017 RPM-GPG-KEY-redhat-release
-r--r--r--. 1 root root 1568 May 7 2017 TRANS.TBL
[root@linuxprobe ~]# df -h
Filesystem Size Used Avail Use% Mounted on
/dev/mapper/rhel-root 18G 3.0G 15G 17% /
devtmpfs 905M 0 905M 0% /dev
tmpfs 914M 140K 914M 1% /dev/shm
tmpfs 914M 8.9M 905M 1% /run
tmpfs 914M 0 914M 0% /sys/fs/cgroup
/dev/cdrom 3.5G 3.5G 0 100% /media/iso
/dev/sda1 497M 119M 379M 24% /boot
```

本章节的复习作业

1．要想实现Linux系统与Windows系统之间的文件共享，能否使用NFS服务？

答：不可以，应该使用Samba服务程序，NFS服务仅能实现Linux系统之间的文件共享。

2．用于管理Samba服务程序的独立账户信息数据库的命令是什么？

答：pdbedit命令用于管理Samba服务程序的账户信息数据库。

3．简述在Windows系统中使用Samba服务程序来共享资源的方法。

答：在开始菜单的输入框中按照\\192.168.10.10的格式输入访问命令并回车执行即可。在Windows的“运行”命令框中按照“\\192.168.10.10”的格式输入访问命令并按回车键即可。

4．简述在Linux系统中使用Samba服务程序来共享资源的步骤方法。

答：首先应创建密码认证文件以及挂载目录，然后把挂载信息写入到/etc/fstab文件中，最后执行mount -a命令挂载使用。

5．如果在Linux系统中默认没有安装NFS服务程序，则需要安装什么软件包呢？

答：NFS服务程序的软件包名字为nfs-utils，因此执行yum install nfs-utils命令即可。

6．在使用NFS服务共享资源时，若希望无论NFS客户端使用什么帐户来访问共享资源，都会被映射为本地匿名用户，则需要添加哪个参数。

答：需要添加all_squash参数，以便更好地保证服务器的安全。

7．客户端在查看到远程NFS服务器上的共享资源列表时，需要使用哪个命令？

答：使用showmount命令即可看到NFS服务器上的资源共享情况。

8．简述autofs服务程序的作用。

答：实现动态灵活的设备挂载操作，而且只有检测到用户试图访问一个尚未挂载的文件系统时，才自动挂载该文件系统。