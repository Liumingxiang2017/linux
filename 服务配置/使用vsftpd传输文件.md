# 使用vsftpd传输文件

## 查看软件包

- 查看软件是否安装：rpm -qa | grep ftp
  - vsftpd
  - ftpd
  - lftp

- 查看软件内容：rpm -ql vsftpd | more

## 启动服务

- service vsftpd start 或者 /etc/init.d/vsftpd start

下载文件：get filename

上传文件：put filename

退出： bye

ftp允许linux真实用户上传、下载、创建，并访问整个文件系统。身份验证采用真实系统用户密码。

将真实用户的/etc/passwd中/bin/bash改成/sbin/nologin，用户就不可登录了。

### 配置文件

anonymous_enable=YES，local_enable=YES 默认用户ftp无需密码登录，目录为/var/ftp/，只能下载不能上传。匿名用户已经使用了chroot功能。

chroot_list_enable=YES, chroot_list_file=/etc/vsftpd/chroot_list取消注释，重启服务。编辑/etc/vsftpd/chroot_list 每个用户名占用一行，可以改变根。

/etc/vsftpd/ftpusers 不允许通过ftp登录的用户，即黑名单，默认不允许root登录ftp因为其权限太大!

/etc/vsftpd/userlist 默认也是为黑名单，即当/etc/vsftpd/vsftpd.conf中的userlist_enable=YES时为黑名单，反之为白名单。

不安全服务

- telnet 账户口令通过明文传输
- http 网站信息明文传输，发展为https
- ftp 文件口令均为明文传输，发展为vsftpd (very safe),对口令加密，匿名用户，本地用户，虚拟用户（知道口令也不能登录服务器）

嗅探数据包软件：wireshark snifer

上传下载 flashfxp

协议ftp，软件包和服务名均为vsftpd

开启两个端口

- 端口号21用于远程控制
- 端口号20用于数据传输

## 文件传输协议

一般来讲，人们将计算机联网的首要目的就是获取资料，而文件传输是一种非常重要的获取资料的方式。今天的互联网是由几千万台个人计算机、工作站、服务器、小型机、大型机、巨型机等具有不同型号、不同架构的物理设备共同组成的，而且即便是个人计算机，也可能会装有Windows、Linux、UNIX、Mac等不同的操作系统。为了能够在如此复杂多样的设备之间解决问题解决文件传输问题，文件传输协议（FTP）应运而生。

FTP是一种在互联网中进行文件传输的协议，基于客户端/服务器模式，默认使用20、21号端口，其中端口20（数据端口）用于进行数据传输，端口21（命令端口）用于接受客户端发出的相关FTP命令与参数。FTP服务器普遍部署于内网中，具有容易搭建、方便管理的特点。而且有些FTP客户端工具还可以支持文件的多点下载以及断点续传技术，因此FTP服务得到了广大用户的青睐。FTP协议的传输拓扑如图11-1所示。

图11-1  FTP协议的传输拓扑

FTP服务器是按照FTP协议在互联网上提供文件存储和访问服务的主机，FTP客户端则是向服务器发送连接请求，以建立数据传输链路的主机。

FTP协议有下面两种工作模式。

- 主动模式：FTP服务器主动向客户端发起连接请求。(可以绕过防火墙INPUT策略)

- 被动模式：FTP服务器等待客户端发起连接请求（FTP的默认工作模式）。

第8章在学习防火墙服务配置时曾经讲过，防火墙一般是用于过滤从外网进入内网的流量，因此有些时候需要将FTP的工作模式设置为主动模式，才可以传输数据。

vsftpd（very secure ftp daemon，非常安全的FTP守护进程）是一款运行在Linux操作系统上的FTP服务程序，不仅完全开源而且免费，此外，还具有很高的安全性、传输速度，以及支持虚拟用户验证等其他FTP服务程序不具备的特点。

在配置妥当Yum软件仓库之后，就可以安装vsftpd服务程序了。

```shell
[root@linuxprobe ~]# yum install vsftpd
Loaded plugins: langpacks, product-id, subscription-manager
………………省略部分输出信息………………
================================================================================
 Package Arch Version Repository Size
================================================================================
Installing:
 vsftpd x86_64 3.0.2-9.el7 rhel 166 k
Transaction Summary
================================================================================
Install 1 Package
Total download size: 166 k
Installed size: 343 k
Is this ok [y/d/N]: y
Downloading packages:
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
 Installing : vsftpd-3.0.2-9.el7.x86_64 1/1 
 Verifying : vsftpd-3.0.2-9.el7.x86_64 1/1 
Installed:
 vsftpd.x86_64 0:3.0.2-9.el7 
Complete!
```

iptables防火墙管理工具默认禁止了FTP传输协议的端口号，因此在正式配置vsftpd服务程序之前，为了避免这些默认的防火墙策略“捣乱”，还需要清空iptables防火墙的默认策略，并把当前已经被清理的防火墙策略状态保存下来：

```shell
[root@linuxprobe ~]# iptables -F
[root@linuxprobe ~]# service iptables save
iptables: Saving firewall rules to /etc/sysconfig/iptables:[ OK ]
```

vsftpd服务程序的主配置文件（/etc/vsftpd/vsftpd.conf）内容总长度达到123行，但其中大多数参数在开头都添加了井号（#），从而成为注释信息，大家没有必要在注释信息上花费太多的时间。我们可以在grep命令后面添加-v参数，过滤并反选出没有包含井号（#）的参数行（即过滤掉所有的注释信息），然后将过滤后的参数行通过输出重定向符写回原始的主配置文件中：

```shell
[root@linuxprobe ~]# mv /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.conf_bak
[root@linuxprobe ~]# grep -v "#" /etc/vsftpd/vsftpd.conf_bak > /etc/vsftpd/vsftpd.conf
[root@linuxprobe ~]# cat /etc/vsftpd/vsftpd.conf
# 是否允许匿名用户
anonymous_enable=YES
# 是否允许本地用户
local_enable=YES
# 写入操作
write_enable=YES
# 文件反掩码
local_umask=022
dirmessage_enable=YES
# 是否保存日志/var/log/messages
xferlog_enable=YES
# 是否通过20端口传输
connect_from_port_20=YES
# 日志是否采用标准格式
xferlog_std_format=YES
# 是否监听，不需要监听，只有报错是才需要YES
listen=NO
# 是否支持ipv6
listen_ipv6=YES
# pam可插拔式认证模块
pam_service_name=vsftpd
# 用户列表（ftpusers，user_list 列表中用户被禁止访问）
userlist_enable=YES
# 是否受到tcp_wrappers防火墙限制
tcp_wrappers=YES
```

表11-1中罗列了vsftpd服务程序主配置文件中常用的参数以及作用。当前大家只需要简单了解即可，在后续的实验中将演示这些参数的用法，以帮助大家熟悉并掌握。

表11-1  vsftpd服务程序常用的参数以及作用

参数	作用
listen=[YES|NO]	是否以独立运行的方式监听服务
listen_address=IP地址	设置要监听的IP地址
listen_port=21	设置FTP服务的监听端口
download_enable＝[YES|NO]	是否允许下载文件
userlist_enable=[YES|NO]
userlist_deny=[YES|NO]	设置用户列表为“允许”还是“禁止”操作
max_clients=0	最大客户端连接数，0为不限制
max_per_ip=0	同一IP地址的最大连接数，0为不限制
anonymous_enable=[YES|NO]	是否允许匿名用户访问
anon_upload_enable=[YES|NO]	是否允许匿名用户上传文件
anon_umask=022	匿名用户上传文件的umask值
anon_root=/var/ftp	匿名用户的FTP根目录
anon_mkdir_write_enable=[YES|NO]	是否允许匿名用户创建目录
anon_other_write_enable=[YES|NO]	是否开放匿名用户的其他写入权限（包括重命名、删除等操作权限）
anon_max_rate=0	匿名用户的最大传输速率（字节/秒），0为不限制
local_enable=[YES|NO]	是否允许本地用户登录FTP
local_umask=022	本地用户上传文件的umask值
local_root=/var/ftp	本地用户的FTP根目录
chroot_local_user=[YES|NO]	是否将用户权限禁锢在FTP目录，以确保安全
local_max_rate=0	本地用户最大传输速率（字节/秒），0为不限制
11.2 Vsftpd服务程序
vsftpd作为更加安全的文件传输的服务程序，允许用户以三种认证模式登录到FTP服务器上。

匿名开放模式：是一种最不安全的认证模式，任何人都可以无需密码验证而直接登录到FTP服务器。

本地用户模式：是通过Linux系统本地的账户密码信息进行认证的模式，相较于匿名开放模式更安全，而且配置起来也很简单。但是如果被黑客破解了账户的信息，就可以畅通无阻地登录FTP服务器，从而完全控制整台服务器。

虚拟用户模式：是这三种模式中最安全的一种认证模式，它需要为FTP服务单独建立用户数据库文件，虚拟出用来进行口令验证的账户信息，而这些账户信息在服务器系统中实际上是不存在的，仅供FTP服务程序进行认证使用。这样，即使黑客破解了账户信息也无法登录服务器，从而有效降低了破坏范围和影响。

ftp是Linux系统中以命令行界面的方式来管理FTP传输服务的客户端工具。我们首先手动安装这个ftp客户端工具，以便在后续实验中查看结果。

```shell
[root@linuxprobe ~]# yum install ftp
Loaded plugins: langpacks, product-id, subscription-manager
………………省略部分输出信息………………
Installing:
 ftp x86_64 0.17-66.el7 rhel 61 k
Transaction Summary
================================================================================
Install 1 Package
Total download size: 61 k
Installed size: 96 k
Is this ok [y/d/N]: y
Downloading packages:
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
 Installing : ftp-0.17-66.el7.x86_64 1/1 
 Verifying : ftp-0.17-66.el7.x86_64 1/1
Installed:
 ftp.x86_64 0:0.17-66.el7
Complete!
```

11.2.1 匿名访问模式
前文提到，在vsftpd服务程序中，匿名开放模式是最不安全的一种认证模式。任何人都可以无需密码验证而直接登录到FTP服务器。这种模式一般用来访问不重要的公开文件（在生产环境中尽量不要存放重要文件）。当然，如果采用第8章中介绍的防火墙管理工具（如Tcp_wrappers服务程序）将vsftpd服务程序允许访问的主机范围设置为企业内网，也可以提供基本的安全性。

vsftpd服务程序默认开启了匿名开放模式，我们需要做的就是开放匿名用户的上传、下载文件的权限，以及让匿名用户创建、删除、更名文件的权限。需要注意的是，针对匿名用户放开这些权限会带来潜在危险，我们只是为了在Linux系统中练习配置vsftpd服务程序而放开了这些权限，不建议在生产环境中如此行事。表11-2罗列了可以向匿名用户开放的权限参数以及作用。

表11-2                                 可以向匿名用户开放的权限参数以及作用

参数	作用
anonymous_enable=YES	允许匿名访问模式
anon_umask=022	匿名用户上传文件的umask值
anon_upload_enable=YES	允许匿名用户上传文件
anon_mkdir_write_enable=YES	允许匿名用户创建目录
anon_other_write_enable=YES	允许匿名用户修改目录名称或删除目录

```shell
[root@linuxprobe ~]# vim /etc/vsftpd/vsftpd.conf
1 anonymous_enable=YES
# 匿名用户上传文件的权限掩码
2 anon_umask=022
# 是否允许匿名用户上传文件
3 anon_upload_enable=YES
# 匿名用户是否允许新建目录文件
4 anon_mkdir_write_enable=YES
# 匿名用户是否允许删除修改重命名文件
5 anon_other_write_enable=YES
6 local_enable=YES
7 write_enable=YES
8 local_umask=022
9 dirmessage_enable=YES
10 xferlog_enable=YES
11 connect_from_port_20=YES
12 xferlog_std_format=YES
13 listen=NO
14 listen_ipv6=YES
15 pam_service_name=vsftpd
16 userlist_enable=YES
17 tcp_wrappers=YES
```

在vsftpd服务程序的主配置文件中正确填写参数，然后保存并退出。还需要重启vsftpd服务程序，让新的配置参数生效。在此需要提醒各位读者，在生产环境中或者在RHCSA、RHCE、RHCA认证考试中一定要把配置过的服务程序加入到开机启动项中，以保证服务器在重启后依然能够正常提供传输服务：

[root@linuxprobe ~]# systemctl restart vsftpd
[root@linuxprobe ~]# systemctl enable vsftpd
 ln -s '/usr/lib/systemd/system/vsftpd.service' '/etc/systemd/system/multi-user.target.wants/vsftpd.service
现在就可以在客户端执行ftp命令连接到远程的FTP服务器了。在vsftpd服务程序的匿名开放认证模式下，其账户统一为anonymous，密码为空。而且在连接到FTP服务器后，默认访问的是/var/ftp目录。我们可以切换到该目录下的pub目录中，然后尝试创建一个新的目录文件，以检验是否拥有写入权限：

```shell
[root@linuxprobe ~]# ftp 192.168.10.10
Connected to 192.168.10.10 (192.168.10.10).
220 (vsFTPd 3.0.2)
Name (192.168.10.10:root): anonymous
331 Please specify the password.
Password:此处敲击回车即可
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> cd pub
250 Directory successfully changed.
ftp> mkdir files
550 Permission denied.
```

系统显示拒绝创建目录！我们明明在前面清空了iptables防火墙策略，而且也在vsftpd服务程序的主配置文件中添加了允许匿名用户创建目录和写入文件的权限啊。建议大家先不要着急往下看，而是自己思考一下这个问题的解决办法，以锻炼您的Linux系统排错能力。

前文提到，在vsftpd服务程序的匿名开放认证模式下，默认访问的是/var/ftp目录。查看该目录的权限得知，只有root管理员才有写入权限。怪不得系统会拒绝操作呢！下面将目录的所有者身份改成系统账户ftp即可（该账户在系统中已经存在），这样应该可以了吧：

```shell
[root@linuxprobe ~]# ls -ld /var/ftp/pub
drwxr-xr-x. 3 root root 16 Jul 13 14:38 /var/ftp/pub
[root@linuxprobe ~]# chown -Rf ftp /var/ftp/pub
[root@linuxprobe ~]# ls -ld /var/ftp/pub
drwxr-xr-x. 3 ftp root 16 Jul 13 14:38 /var/ftp/pub
[root@linuxprobe ~]# ftp 192.168.10.10
Connected to 192.168.10.10 (192.168.10.10).
220 (vsFTPd 3.0.2)
Name (192.168.10.10:root): anonymous
331 Please specify the password.
Password:此处敲击回车即可
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> cd pub
250 Directory successfully changed.
ftp> mkdir files
550 Create directory operation failed.
```

系统再次报错！尽管我们在使用ftp命令登入FTP服务器后，再创建目录时系统依然提示操作失败，但是报错信息却发生了变化。在没有写入权限时，系统提示“权限拒绝”（Permission denied）所以刘遄老师怀疑是权限的问题。但现在系统提示“创建目录的操作失败”（Create directory operation failed），想必各位读者也应该意识到是SELinux服务在“捣乱”了吧。

下面使用getsebool命令查看与FTP相关的SELinux域策略都有哪些：

```shell
[root@linuxprobe ~]# getsebool -a | grep ftp
ftp_home_dir --> off
ftpd_anon_write --> off
ftpd_connect_all_unreserved --> off
ftpd_connect_db --> off
ftpd_full_access --> off
ftpd_use_cifs --> off
ftpd_use_fusefs --> off
ftpd_use_nfs --> off
ftpd_use_passive_mode --> off
httpd_can_connect_ftp --> off
httpd_enable_ftp_server --> off
sftpd_anon_write --> off
sftpd_enable_homedirs --> off
sftpd_full_access --> off
sftpd_write_ssh_home --> off
tftp_anon_write --> off
tftp_home_dir --> off
```

我们可以根据经验（需要长期培养，别无它法）和策略的名称判断出是ftpd_full_access--> off策略规则导致了操作失败。接下来修改该策略规则，并且在设置时使用-P参数让修改过的策略永久生效，确保在服务器重启后依然能够顺利写入文件。

```shell
[root@linuxprobe ~]# setsebool -P ftpd_full_access=on
```

再次提醒各位读者，在进行下一次实验之前，一定记得将虚拟机还原到最初始的状态，以免多个实验相互产生冲突。

现在便可以顺利执行文件创建、修改及删除等操作了。

```shell
[root@linuxprobe ~]# ftp 192.168.10.10
Connected to 192.168.10.10 (192.168.10.10).
220 (vsFTPd 3.0.2)
Name (192.168.10.10:root): anonymous
331 Please specify the password.
Password:此处敲击回车即可
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> cd pub
250 Directory successfully changed.
ftp> mkdir files
257 "/pub/files" created
ftp> rename files database
350 Ready for RNTO.
250 Rename successful.
ftp> rmdir database
250 Remove directory operation successful.
ftp> exit
221 Goodbye.
```

### 本地用户模式

相较于匿名开放模式，本地用户模式要更安全，而且配置起来也很简单。如果大家之前用的是匿名开放模式，现在就可以将它关了，然后开启本地用户模式。针对本地用户模式的权限参数以及作用如表11-3所示。

表11-3  本地用户模式使用的权限参数以及作用

参数	作用
anonymous_enable=NO	禁止匿名访问模式
local_enable=YES	允许本地用户模式
write_enable=YES	设置可写权限
local_umask=022	本地用户模式创建文件的umask值
userlist_deny=YES	启用“禁止用户名单”，名单文件为ftpusers和user_list
userlist_enable=YES	开启用户作用名单文件功能
[root@linuxprobe ~]# vim /etc/vsftpd/vsftpd.conf
1 anonymous_enable=NO
2 local_enable=YES
3 write_enable=YES
4 local_umask=022
5 dirmessage_enable=YES
6 xferlog_enable=YES
7 connect_from_port_20=YES
8 xferlog_std_format=YES
9 listen=NO
10 listen_ipv6=YES
11 pam_service_name=vsftpd
12 userlist_enable=YES
13 tcp_wrappers=YES
在vsftpd服务程序的主配置文件中正确填写参数，然后保存并退出。还需要重启vsftpd服务程序，让新的配置参数生效。在执行完上一个实验后还原了虚拟机的读者，还需要将配置好的服务添加到开机启动项中，以便在系统重启自后依然可以正常使用vsftpd服务。

[root@linuxprobe ~]# systemctl restart vsftpd
[root@linuxprobe ~]# systemctl enable vsftpd
 ln -s '/usr/lib/systemd/system/vsftpd.service' '/etc/systemd/system/multi-user.target.wants/vsftpd.service
按理来讲，现在已经完全可以本地用户的身份登录FTP服务器了。但是在使用root管理员登录后，系统提示如下的错误信息：

[root@linuxprobe ~]# ftp 192.168.10.10
Connected to 192.168.10.10 (192.168.10.10).
220 (vsFTPd 3.0.2)
Name (192.168.10.10:root): root
530 Permission denied.
Login failed.
ftp>
可见，在我们输入root管理员的密码之前，就已经被系统拒绝访问了。这是因为vsftpd服务程序所在的目录中默认存放着两个名为“用户名单”的文件（ftpusers和user_list）。不知道大家是否已看过一部日本电影“死亡笔记”（刘遄老师在上学期间的最爱），里面就提到有一个黑色封皮的小本子，只要将别人的名字写进去，这人就会挂掉。vsftpd服务程序目录中的这两个文件也有类似的功能—只要里面写有某位用户的名字，就不再允许这位用户登录到FTP服务器上。

```shell
[root@linuxprobe ~]# cat /etc/vsftpd/user_list 
1 # vsftpd userlist
2 # If userlist_deny=NO, only allow users in this file
3 # If userlist_deny=YES (default), never allow users in this file, and
4 # do not even prompt for a password.
5 # Note that the default vsftpd pam config also checks /etc/vsftpd/ftpusers
6 # for users that are denied.
7 root
8 bin
9 daemon
10 adm
11 lp
12 sync
13 shutdown
14 halt
15 mail
16 news
17 uucp
18 operator
19 games
20 nobody
[root@linuxprobe ~]# cat /etc/vsftpd/ftpusers 
# Users that are not allowed to login via ftp
1 root
2 bin
3 daemon
4 adm
5 lp
6 sync
7 shutdown
8 halt
9 mail
10 news
11 uucp
12 operator
13 games
14 nobody
```

果然如此！vsftpd服务程序为了保证服务器的安全性而默认禁止了root管理员和大多数系统用户的登录行为，这样可以有效地避免黑客通过FTP服务对root管理员密码进行暴力破解。如果您确认在生产环境中使用root管理员不会对系统安全产生影响，只需按照上面的提示删除掉root用户名即可。我们也可以选择ftpusers和user_list文件中没有的一个普通用户尝试登录FTP服务器：

[root@linuxprobe ~]# ftp 192.168.10.10 
Connected to 192.168.10.10 (192.168.10.10).
220 (vsFTPd 3.0.2)
Name (192.168.10.10:root): linuxprobe
331 Please specify the password.
Password:此处输入该用户的密码
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> mkdir files
550 Create directory operation failed.
在采用本地用户模式登录FTP服务器后，默认访问的是该用户的家目录，也就是说，访问的是/home/linuxprobe目录。而且该目录的默认所有者、所属组都是该用户自己，因此不存在写入权限不足的情况。但是当前的操作仍然被拒绝，是因为我们刚才将虚拟机系统还原到最初的状态了。为此，需要再次开启SELinux域中对FTP服务的允许策略：

[root@linuxprobe ~]# getsebool -a | grep ftp
ftp_home_dir --> off
ftpd_anon_write --> off
ftpd_connect_all_unreserved --> off
ftpd_connect_db --> off
ftpd_full_access --> off
ftpd_use_cifs --> off
ftpd_use_fusefs --> off
ftpd_use_nfs --> off
ftpd_use_passive_mode --> off
httpd_can_connect_ftp --> off
httpd_enable_ftp_server --> off
sftpd_anon_write --> off
sftpd_enable_homedirs --> off
sftpd_full_access --> off
sftpd_write_ssh_home --> off
tftp_anon_write --> off
tftp_home_dir --> off
[root@linuxprobe ~]# setsebool -P ftpd_full_access=on
刘遄老师再啰嗦几句。在实验课程和生产环境中设置SELinux域策略时，一定记得添加-P参数，否则服务器在重启后就会按照原有的策略进行控制，从而导致配置过的服务无法使用。

在配置妥当后再使用本地用户尝试登录下FTP服务器，分别执行文件的创建、重命名及删除等命令。操作均成功！

```shell
[root@linuxprobe ~]# ftp 192.168.10.10
Connected to 192.168.10.10 (192.168.10.10).
220 (vsFTPd 3.0.2)
Name (192.168.10.10:root): linuxprobe
331 Please specify the password.
Password:此处输入该用户的密码
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> mkdir files
257 "/home/linuxprobe/files" created
ftp> rename files database
350 Ready for RNTO.
250 Rename successful.
ftp> rmdir database
250 Remove directory operation successful.
ftp> exit
221 Goodbye.
```

请注意:当您完成本实验后请还原虚拟机快照再进行下一个实验，否则可能导致配置文件冲突而报错。

### 虚拟用户模式

我们最后讲解的虚拟用户模式是这三种模式中最安全的一种认证模式，当然，因为安全性较之于前面两种模式有了提升，所以配置流程也会稍微复杂一些。

第1步：创建用于进行FTP认证的用户数据库文件，其中奇数行为账户名，偶数行为密码。例如，我们分别创建出zhangsan和lisi两个用户，密码均为redhat：

```shell
[root@linuxprobe ~]# cd /etc/vsftpd/
[root@linuxprobe vsftpd]# vim vuser.list
# 账户名
zhangsan
# 密码
redhat
lisi
redhat
```

但是，明文信息既不安全，也不符合让vsftpd服务程序直接加载的格式，因此需要使用db_load命令用哈希（hash）算法将原始的明文信息文件转换成数据库文件，并且降低数据库文件的权限（避免其他人看到数据库文件的内容），然后再把原始的明文信息文件删除。

```shell
[root@linuxprobe vsftpd]# db_load -T -t hash -f vuser.list vuser.db
# -T 加密
# -t 指定加密方式
# vuser.db 加密后文件
[root@linuxprobe vsftpd]# file vuser.db
vuser.db: Berkeley DB (Hash, version 9, native byte-order)
[root@linuxprobe vsftpd]# chmod 600 vuser.db
# 收紧权限
[root@linuxprobe vsftpd]# rm -f vuser.list
```

第2步：创建vsftpd服务程序用于存储文件的根目录以及虚拟用户映射的系统本地用户。FTP服务用于存储文件的根目录指的是，当虚拟用户登录后所访问的默认位置。

由于Linux系统中的每一个文件都有所有者、所属组属性，例如使用虚拟账户“张三”新建了一个文件，但是系统中找不到账户“张三”，就会导致这个文件的权限出现错误。为此，需要再创建一个可以映射到虚拟用户的系统本地用户。简单来说，就是让虚拟用户默认登录到与之有映射关系的这个系统本地用户的家目录中，虚拟用户创建的文件的属性也都归属于这个系统本地用户，从而避免Linux系统无法处理虚拟用户所创建文件的属性权限。

为了方便管理FTP服务器上的数据，可以把这个系统本地用户的家目录设置为/var目录（该目录用来存放经常发生改变的数据）。并且为了安全起见，我们将这个系统本地用户设置为不允许登录FTP服务器，这不会影响虚拟用户登录，而且还可以避免黑客通过这个系统本地用户进行登录。

```shell
[root@linuxprobe ~]# useradd -d /var/ftproot -s /sbin/nologin virtual
# -d 映射目录的家目录/var/ftproot
# -s shell设置为 /sbin/nologin，即使知道密码也不可以登录！
# 将虚拟账号映射为本地账号virtual
[root@linuxprobe ~]# ls -ld /var/ftproot/
drwx------. 3 virtual virtual 74 Jul 14 17:50 /var/ftproot/
[root@linuxprobe ~]# chmod -Rf 755 /var/ftproot/
```

第3步：建立用于支持虚拟用户的PAM文件。

PAM（可插拔认证模块）是一种认证机制，通过一些动态链接库和统一的API把系统提供的服务与认证方式分开，使得系统管理员可以根据需求灵活调整服务程序的不同认证方式。要想把PAM功能和作用完全讲透，至少要一个章节的篇幅才可以（对该主题感兴趣的读者敬请关注本书的进阶篇，里面会详细讲解PAM）。

通俗来讲，PAM是一组安全机制的模块，系统管理员可以用来轻易地调整服务程序的认证方式，而不必对应用程序进行任何修改。PAM采取了分层设计（应用程序层、应用接口层、鉴别模块层）的思想，其结构如图11-2所示。

图11-2  PAM的分层设计结构

新建一个用于虚拟用户认证的PAM文件vsftpd.vu，其中PAM文件内的“db=”参数为使用db_load命令生成的账户密码数据库文件的路径，但不用写数据库文件的后缀：

```shell
[root@linuxprobe ~]# vim /etc/pam.d/vsftpd.vu
auth       required     pam_userdb.so db=/etc/vsftpd/vuser
account    required     pam_userdb.so db=/etc/vsftpd/vuser
```

第4步：在vsftpd服务程序的主配置文件中通过pam_service_name参数将PAM认证文件的名称修改为vsftpd.vu，PAM作为应用程序层与鉴别模块层的连接纽带，可以让应用程序根据需求灵活地在自身插入所需的鉴别功能模块。当应用程序需要PAM认证时，则需要在应用程序中定义负责认证的PAM配置文件，实现所需的认证功能。

例如，在vsftpd服务程序的主配置文件中默认就带有参数pam_service_name=vsftpd，表示登录FTP服务器时是根据/etc/pam.d/vsftpd文件进行安全认证的。现在我们要做的就是把vsftpd主配置文件中原有的PAM认证文件vsftpd修改为新建的vsftpd.vu文件即可。该操作中用到的参数以及作用如表11-4所示。

表11-4 利用PAM文件进行认证时使用的参数以及作用

参数	作用
anonymous_enable=NO	禁止匿名开放模式
local_enable=YES	允许本地用户模式
guest_enable=YES	开启虚拟用户模式
guest_username=virtual	指定虚拟用户账户
pam_service_name=vsftpd.vu	指定PAM文件
allow_writeable_chroot=YES	允许对禁锢的FTP根目录执行写入操作，而且不拒绝用户的登录请求

```shell
[root@linuxprobe ~]# vim /etc/vsftpd/vsftpd.conf
1 anonymous_enable=NO
# 禁止匿名用户登录，不安全
2 local_enable=YES
# 必须允许本地用户登录，因为映射的是本地用户
3 guest_enable=YES
# 允许虚拟用户登录服务器
4 guest_username=virtual
# 虚拟用户映射为本地账户的名称
5 allow_writeable_chroot=YES
# 是否允许牢笼机制，比如bind dns都有chroot技术，牢笼机制，将权限和用户身份进行限制
# 当黑客入侵通过dns或者ftp入侵服务器，其破坏范围最多为dns和ftp
6 write_enable=YES
7 local_umask=022
8 dirmessage_enable=YES
9 xferlog_enable=YES
10 connect_from_port_20=YES
11 xferlog_std_format=YES
12 listen=NO
13 listen_ipv6=YES
14 pam_service_name=vsftpd.vu
15 userlist_enable=YES
16 tcp_wrappers=YES
```

第5步：为虚拟用户设置不同的权限。虽然账户zhangsan和lisi都是用于vsftpd服务程序认证的虚拟账户，但是我们依然想对这两人进行区别对待。比如，允许张三上传、创建、修改、查看、删除文件，只允许李四查看文件。这可以通过vsftpd服务程序来实现。只需新建一个目录，在里面分别创建两个以zhangsan和lisi命名的文件，其中在名为zhangsan的文件中写入允许的相关权限（使用匿名用户的参数）：

```shell
[root@linuxprobe ~]# mkdir /etc/vsftpd/vusers_dir/
[root@linuxprobe ~]# cd /etc/vsftpd/vusers_dir/
[root@linuxprobe vusers_dir]# touch lisi
[root@linuxprobe vusers_dir]# vim zhangsan
anon_upload_enable=YES
# 特指zhangsan用户的上传权限
anon_mkdir_write_enable=YES
anon_other_write_enable=YES
```

然后再次修改vsftpd主配置文件，通过添加user_config_dir参数来定义这两个虚拟用户不同权限的配置文件所存放的路径。为了让修改后的参数立即生效，需要重启vsftpd服务程序并将该服务添加到开机启动项中：

```shell
[root@linuxprobe ~]# vim /etc/vsftpd/vsftpd.conf
anonymous_enable=NO
local_enable=YES
guest_enable=YES
guest_username=virtual
allow_writeable_chroot=YES
write_enable=YES
local_umask=022
dirmessage_enable=YES
xferlog_enable=YES
connect_from_port_20=YES
xferlog_std_format=YES
listen=NO
listen_ipv6=YES
pam_service_name=vsftpd.vu
userlist_enable=YES
tcp_wrappers=YES
user_config_dir=/etc/vsftpd/vusers_dir
# 每个虚拟用户权限文件保存路径
[root@linuxprobe ~]# systemctl restart vsftpd
[root@linuxprobe ~]# systemctl enable vsftpd
# 加入开机启动
 ln -s '/usr/lib/systemd/system/vsftpd.service' '/etc/systemd/system/multi-user.target.wants/vsftpd.service
 ```

第6步：设置SELinux域允许策略，然后使用虚拟用户模式登录FTP服务器。相信大家可以猜到，SELinux会继续来捣乱。所以，先按照前面实验中的步骤开启SELinux域的允许策略，以免再次出现操作失败的情况：

```shell
[root@linuxprobe ~]# getsebool -a | grep ftp
ftp_home_dir –> off
ftpd_anon_write –> off
ftpd_connect_all_unreserved –> off
ftpd_connect_db –> off
ftpd_full_access –> off
ftpd_use_cifs –> off
ftpd_use_fusefs –> off
ftpd_use_nfs –> off
ftpd_use_passive_mode –> off
httpd_can_connect_ftp –> off
httpd_enable_ftp_server –> off
sftpd_anon_write –> off
sftpd_enable_homedirs –> off
sftpd_full_access –> off
sftpd_write_ssh_home –> off
tftp_anon_write –> off
tftp_home_dir –> off
[root@linuxprobe ~]# setsebool -P ftpd_full_access=on
```

此时，不但可以使用虚拟用户模式成功登录到FTP服务器，还可以分别使用账户zhangsan和lisi来检验他们的权限。当然，读者在生产环境中一定要根据真实需求来灵活配置参数，不要照搬这里的实验操作。

```shell
[root@linuxprobe ~]# ftp 192.168.10.10
Connected to 192.168.10.10 (192.168.10.10).
220 (vsFTPd 3.0.2)
Name (192.168.10.10:root): lisi
331 Please specify the password.
Password:此处输入虚拟用户的密码
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> mkdir files
550 Permission denied.
ftp> exit
221 Goodbye.
[root@linuxprobe ~]# ftp 192.168.10.10
Connected to 192.168.10.10 (192.168.10.10).
220 (vsFTPd 3.0.2)
Name (192.168.10.10:root): zhangsan
331 Please specify the password.
Password:此处输入虚拟用户的密码
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> mkdir files
257 "/files" created
ftp> rename files database
350 Ready for RNTO.
250 Rename successful.
ftp> rmdir database
250 Remove directory operation successful.
ftp> exit
221 Goodbye.
```

## TFTP简单文件传输协议

简单文件传输协议（Trivial File Transfer Protocol，TFTP）是一种基于UDP协议在客户端和服务器之间进行简单文件传输的协议。顾名思义，它提供不复杂、开销不大的文件传输服务（可将其当作FTP协议的简化版本）。

TFTP的命令功能不如FTP服务强大，甚至不能遍历目录，在安全性方面也弱于FTP服务。而且，由于TFTP在传输文件时采用的是UDP协议，占用的端口号为69，因此文件的传输过程也不像FTP协议那样可靠。但是，因为TFTP不需要客户端的权限认证，也就减少了无谓的系统和网络带宽消耗，因此在传输琐碎（trivial）不大的文件时，效率更高。

接下来在系统上安装TFTP的软件包，进行体验。

```shell
[root@linuxprobe ~]# yum install tftp-server tftp
# tftp-server 服务端工具
# tftp 客户端连接工具
Loaded plugins: langpacks, product-id, subscription-manager
………………省略部分输出信息………………
Installing:
 tftp x86_64 5.2-11.el7 rhel 35 k
 tftp-server x86_64 5.2-11.el7 rhel 44 k
Installing for dependencies:
 xinetd x86_64 2:2.3.15-12.el7 rhel 128 k
Transaction Summary
================================================================================
Install 2 Packages (+1 Dependent package)
Total download size: 207 k
Installed size: 373 k
Is this ok [y/d/N]: y
Downloading packages:
………………省略部分输出信息………………
Installed:
 tftp.x86_64 0:5.2-11.el7 tftp-server.x86_64 0:5.2-11.el7
Dependency Installed:
 xinetd.x86_64 2:2.3.15-12.el7
Complete!
```

在RHEL 7系统中，TFTP服务是使用xinetd服务程序来管理的。xinetd服务可以用来管理多种轻量级的网络服务，而且具有强大的日志功能。简单来说，在安装TFTP软件包后，还需要在xinetd服务程序中将其开启，把默认的禁用（disable）参数修改为no：

```shell
[root@linuxprobe ~]# vim /etc/xinetd.d/tftp
service tftp
{
        socket_type             = dgram
        protocol                = udp
        wait                    = yes
        user                    = root
        server                  = /usr/sbin/in.tftpd
        # 程序软件包所在路径
        server_args             = -s /var/lib/tftpboot
        disable                 = no
        # 服务程序是否禁用
        per_source              = 11
        cps                     = 100 2
        flags                   = IPv4
}
```

然后，重启xinetd服务并将它添加到系统的开机启动项中，以确保TFTP服务在系统重启后依然处于运行状态。考虑到有些系统的防火墙默认没有允许UDP协议的69端口，因此需要手动将该端口号加入到防火墙的允许策略中：

```shell
[root@linuxprobe ~]# systemctl restart xinetd
[root@linuxprobe ~]# systemctl enable xinetd
[root@linuxprobe ~]# firewall-cmd --permanent --add-port=69/udp
success
[root@linuxprobe ~]# firewall-cmd --reload
success
```

TFTP的根目录为/var/lib/tftpboot。我们可以使用刚安装好的tftp命令尝试访问其中的文件，亲身体验TFTP服务的文件传输过程。在使用tftp命令访问文件时，可能会用到表11-5中的参数。

表11-5  tftp命令中可用的参数以及作用

命令	作用
?	帮助信息
put	上传文件
get	下载文件
verbose	显示详细的处理信息
status	显示当前的状态信息
binary	使用二进制进行传输
ascii	使用ASCII码进行传输
timeout	设置重传的超时时间
quit	退出

```shell
[root@linuxprobe ~]# echo "i love linux" > /var/lib/tftpboot/readme.txt
[root@linuxprobe ~]# tftp 192.168.10.10
tftp> get readme.txt
tftp> quit
[root@linuxprobe ~]# ls
anaconda-ks.cfg Documents initial-setup-ks.cfg Pictures readme.txt Videos
Desktop Downloads Music Public Templates
[root@linuxprobe ~]# cat readme.txt 
i love linux
```