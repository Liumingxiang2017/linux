# 使用Postfix与Dovecot部署邮件系统

发信
RHEL5/6 sendmail
RHEL7 postfix

收信 dovecot

本章目录结构 [收起]

15.1 电子邮件系统
15.2.1 配置Postfix服务程序
15.2.2 配置Dovecot服务程序
15.2.3 客户使用电子邮件系统
15.3 设置用户别名邮箱
15.1 电子邮件系统

20世纪60年代，美苏两国正处于冷战时期。美国军方认为应该在科学技术上保持其领先的地位，这样有助于在未来的战争中取得优势。美国国防部由此发起了一项名为ARPANET的科研项目，即大家现在所熟知的阿帕网计划。阿帕网是当今互联网的雏形，它也是世界上第一个运营的封包交换网络。但是很快在1971年阿帕网遇到了严峻的问题，如图15-1所示，参与阿帕网科研项目的科学家分布在美国不同的地区，甚至还会因为时差的影响而不能及时分享各自的研究成果，因此科学家们迫切需要一种能够借助于网络在计算机之间传输数据的方法。

尽管本书第10章和第11章介绍的Web服务和FTP文件传输服务也能实现数据交换，但是这些服务的数据传输方式就像“打电话”那样，需要双方同时在线才能完成传输工作。如果对方的主机宕机或者科研人员因故离开，就有可能错过某些科研成果了。好在当时麻省理工学院的Ray Tomlinson博士也参与到了阿帕网计划的科研项目中，他觉得有必要设计一种类似于“信件”的传输服务，并为信件准备一个“信箱”，这样即便对方临时离线也能完成数据的接收，等上线后再进行处理即可。于是，Ray Tomlinson博士用了近一年的时间完成了电子邮件（Email）的设计，并在1971年秋天使用SNDMSG软件向自己的另一台计算机发送出了人类历史上第一封电子邮件—电子邮件系统在互联网中由此诞生！

图15-1  1971年阿帕网科研项目运营情况历史资料图片

既然要在互联网中给他人发送电子邮件，那么对方用户用于接收电子邮件的名称必须是唯一的，否则电子邮件可能会同时发给多个重名的用户，也或者干脆大家都收不到邮件了。因此，Ray Tomlinson博士决定选择使用“姓名@计算机主机名称”的格式来规范电子信箱的名称。选择使用@符号作为间隔符的原因其实也很简单，因为Ray Tomlinson博士觉得人类的名字和计算机主机名称中应该不会有这么一个@符号，所以就选择了这个符号。

电子邮件系统基于邮件协议来完成电子邮件的传输，常见的邮件协议有下面这些。

简单邮件传输协议（Simple Mail Transfer Protocol，SMTP）：用于发送和中转发出的电子邮件，占用服务器的25/TCP端口。

邮局协议版本3（Post Office Protocol 3）：用于将电子邮件存储到本地主机，占用服务器的110/TCP端口。

Internet消息访问协议版本4（Internet Message Access Protocol 4）：用于在本地主机上访问邮件，占用服务器的143/TCP端口。

在电子邮件系统中，为用户收发邮件的服务器名为邮件用户代理（Mail User Agent，MUA）。另外，既然电子邮件系统能够让用户在离线的情况下依然可以完成数据的接收，肯定得有一个用于保存用户邮件的“信箱”服务器，这个服务器的名字为邮件投递代理（Mail Delivery Agent，MDA），其工作职责是把来自于邮件传输代理（Mail Transfer Agent，MTA）的邮件保存到本地的收件箱中。其中，这个MTA的工作职责是转发处理不同电子邮件服务供应商之间的邮件，把来自于MUA的邮件转发到合适的MTA服务器。例如，我们从新浪信箱向谷歌信箱发送一封电子邮件，这封电子邮件的传输过程如图15-2所示。

总的来说，一般的网络服务程序在传输信息时就像拨打电话，需要双方同时保持在线，而在电子邮件系统中，当用户发送邮件后不必等待投递工作完成即可下线。如果对方邮件服务器（MTA）宕机或对方临时离线，则发件服务器（MTA）就会把要发送的内容自动的暂时保存到本地，等检测到对方邮件服务器恢复后会立即再次投递，期间一般无需运维人员维护处理，随后收信人（MUA）就能在自己的信箱中找到这封邮件了。

图15-2  电子邮件的传输过程

大家在生产环境中部署企业级的电子邮件系统时，有4个注意事项请留意。

添加反垃圾与反病毒模块：它能够很有效地阻止垃圾邮件或病毒邮件对企业信箱的干扰。
对邮件加密：可有效保护邮件内容不被黑客盗取和篡改。
添加邮件监控审核模块：可有效地监控企业全体员工的邮件中是否有敏感词、是否有透露企业资料等违规行为。
保障稳定性：电子邮件系统的稳定性至关重要，运维人员应做到保证电子邮件系统的稳定运行，并及时做好防范分布式拒绝服务（Distributed Denial of Service，DDoS）攻击的准备。

## 15.2 部署基础的电子邮件系统

一个最基础的电子邮件系统肯定要能提供发件服务和收件服务，为此需要使用基于SMTP协议的Postfix服务程序提供发件服务功能，并使用基于POP3协议的Dovecot服务程序提供收件服务功能。这样一来，用户就可以使用Outlook Express或Foxmail等客户端服务程序正常收发邮件了。电子邮件系统的工作流程如图15-3所示。

图15-3  电子邮件系统的工作流程

在RHEL 5、RHEL 6以及诸多早期的Linux系统中，默认使用的发件服务是由Sendmail服务程序提供的，而在RHEL 7系统中已经替换为Postfix服务程序。相较于Sendmail服务程序，Postfix服务程序减少了很多不必要的配置步骤，而且在稳定性、并发性方面也有很大改进。

一般而言，我们的信箱地址类似于“root@linuxprobe.com”这样，也就是按照“用户名@主机地址（域名）”格式来规范的。如果您给我一串“root@192.168.10.10”的信息，我可能猜不到这是一个信箱地址，没准会将它当作SSH协议的连接信息。因此，要想更好地检验电子邮件系统的配置效果，需要先部署bind服务程序，为电子邮件服务器和客户端提供DNS域名解析服务。

### 第1步：配置服务器主机名称

配置服务器主机名称，需要保证服务器主机名称与发信域名保持一致：

```shell
[root@linuxprobe ~]# vim /etc/hostname
mail.linuxprobe.com
[root@linuxprobe ~]# hostname
mail.linuxprobe.com
```

### 第2步：清空防火墙策略

清空iptables防火墙默认策略，并保存策略状态，避免因防火墙中默认存在的策略阻止了客户端DNS解析域名及收发邮件：

```shell
[root@localhost ~]# iptables -F
[root@localhost ~]# service iptables save
iptables: Saving firewall rules to /etc/sysconfig/iptables:[  OK  ]
```

第3步：为电子邮件系统提供域名解析。由于第13章已经讲解了bind-chroot服务程序的配置方法，因此这里只提供主配置文件、区域配置文件和域名数据文件的配置内容，其余配置步骤请大家自行完成。

```shell
 [root@linuxprobe ~]# cat /etc/named.conf
 1 //
 2 // named.conf
 3 //
 4 // Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
 5 // server as a caching only nameserver (as a localhost DNS resolver only).
 6 //
 7 // See /usr/share/doc/bind*/sample/ for example named configuration files.
 8 //
 9 
 10 options {
 11 listen-on port 53 { any; };
 12 listen-on-v6 port 53 { ::1; };
 13 directory "/var/named";
 14 dump-file "/var/named/data/cache_dump.db";
 15 statistics-file "/var/named/data/named_stats.txt";
 16 memstatistics-file "/var/named/data/named_mem_stats.txt";
 17 allow-query { any; };
 18 
 ………………省略部分输出信息………………
[root@linuxprobe ~]# cat /etc/named.rfc1912.zones
zone "linuxprobe.com" IN {
type master;
file "linuxprobe.com.zone";
allow-update {none;};
};
[root@linuxprobe ~]# cat /var/named/linuxprobe.com.zone
$TTL 1D				
@	IN SOA	linuxprobe.com.	root.linuxprobe.com.	(
0;serial
1D;refresh
1H;retry
1W;expire
3H);minimum
NS	ns.linuxprobe.com.	
ns	IN A	192.168.10.10	
# 定义邮局   10 是优先级
@	IN MX 10	mail.linuxprobe.com.	
mail	IN A	192.168.10.10	
[root@linuxprobe ~]# systemctl restart named
[root@linuxprobe ~]# systemctl enable named
ln -s '/usr/lib/systemd/system/named.service' 
'/etc/systemd/system/multi-user.target.wants/named.service'
```

修改好配置文件后记得重启bind服务程序，这样电子邮件系统所对应的服务器主机名即为mail.linuxprobe.com，而邮件域为@linuxprobe.com。把服务器的DNS地址修改成本地IP地址，如图15-4所示。

图15-4  配置服务器的DNS地址

### 配置Postfix服务程序

Postfix是一款由IBM资助研发的免费开源电子邮件服务程序，能够很好地兼容Sendmail服务程序，可以方便Sendmail用户迁移到Postfix服务上。Postfix服务程序的邮件收发能力强于Sendmail服务，而且能自动增加、减少进程的数量来保证电子邮件系统的高性能与稳定性。另外，Postfix服务程序由许多小模块组成，每个小模块都可以完成特定的功能，因此可在生产工作环境中根据需求灵活搭配它们。

第1步：安装Postfix服务程序。这一步在RHEL7系统中是多余的。刘遄老师之所以还要写上这一步骤，其目的是让大家在学完本书之后不但能掌握RHEL系统，还能立即上手Fedora、CentOS等主流Linux系统。这样，既然这些系统没有默认安装Postfix服务程序，我们也可以自行搞定。在安装完Postfix服务程序后，需要禁用iptables防火墙，否则外部用户无法访问电子邮件系统。

```shell
[root@linuxprobe ~]# yum install postfix
Loaded plugins: langpacks, product-id, subscription-manager
rhel7 | 4.1 kB 00:00
(1/2): rhel7/group_gz | 134 kB 00:00
(2/2): rhel7/primary_db | 3.4 MB 00:00
Package 2:postfix-2.10.1-6.el7.x86_64 already installed and latest version
Nothing to do
[root@linuxprobe ~]# systemctl disable iptables
```

第2步：配置Postfix服务程序。大家如果是首次看到Postfix服务程序主配置文件（/etc/ postfix/main.cf），估计会被679行左右的内容给吓到。其实不用担心，这里面绝大多数的内容依然是注释信息。刘遄老师在本书中一直强调正确学习Linux系统的方法，并坚信“负责任的好老师不应该是书本的搬运工，而应该一名优质内容的提炼者”，因此在翻遍了配置参数的介绍，以及结合多年的运维经验后，最终总结出了7个最应该掌握的参数，如表15-1所示。

表15-1  Postfix服务程序主配置文件中的重要参数

参数	作用
myhostname	邮局系统的主机名
mydomain	邮局系统的域名
myorigin	从本机发出邮件的域名名称
inet_interfaces	监听的网卡接口
mydestination	可接收邮件的主机名或域名
mynetworks	设置可转发哪些主机的邮件
relay_domains	设置可转发哪些网域的邮件
在Postfix服务程序的主配置文件中，总计需要修改5处。首先是在第76行定义一个名为myhostname的变量，用来保存服务器的主机名称。请大家记住这个变量的名称，下边的参数需要调用它：

```shell
[root@linuxprobe ~]# vim /etc/postfix/main.cf
………………省略部分输出信息………………
68 # INTERNET HOST AND DOMAIN NAMES
69 # 
70 # The myhostname parameter specifies the internet hostname of this
71 # mail system. The default is to use the fully-qualified domain name
72 # from gethostname(). $myhostname is used as a default value for many
73 # other configuration parameters.
74 #
75 #myhostname = host.domain.tld
# 定义主机名称
76 myhostname = mail.linuxprobe.com
………………省略部分输出信息………………
然后在第83行定义一个名为mydomain的变量，用来保存邮件域的名称。大家也要记住这个变量名称，下面将调用它：

78 # The mydomain parameter specifies the local internet domain name.
79 # The default is to use $myhostname minus the first component.
80 # $mydomain is used as a default value for many other configuration
81 # parameters.
82 #
83 mydomain = linuxprobe.com
在第99行调用前面的mydomain变量，用来定义发出邮件的域。调用变量的好处是避免重复写入信息，以及便于日后统一修改：

85 # SENDING MAIL
86 # 
87 # The myorigin parameter specifies the domain that locally-posted
88 # mail appears to come from. The default is to append $myhostname,
89 # which is fine for small sites. If you run a domain with multiple
90 # machines, you should (1) change this to $mydomain and (2) set up
91 # a domain-wide alias database that aliases each user to
92 # user@that.users.mailhost.
93 #
94 # For the sake of consistency between sender and recipient addresses,
95 # myorigin also specifies the default domain name that is appended
96 # to recipient addresses that have no @domain part.
97 #
98 #myorigin = $myhostname
99 myorigin = $mydomain
第4处修改是在第116行定义网卡监听地址。可以指定要使用服务器的哪些IP地址对外提供电子邮件服务；也可以干脆写成all，代表所有IP地址都能提供电子邮件服务：

103 # The inet_interfaces parameter specifies the network interface
104 # addresses that this mail system receives mail on. By default,
105 # the software claims all active interfaces on the machine. The
106 # parameter also controls delivery of mail to user@[ip.address].
107 #
108 # See also the proxy_interfaces parameter, for network addresses that
109 # are forwarded to us via a proxy or network address translator.
110 #
111 # Note: you need to stop/start Postfix when this parameter changes.
112 #
113 #inet_interfaces = all
114 #inet_interfaces = $myhostname
115 #inet_interfaces = $myhostname, localhost
116 inet_interfaces = all
最后一处修改是在第164行定义可接收邮件的主机名或域名列表。这里可以直接调用前面定义好的myhostname和mydomain变量（如果不想调用变量，也可以直接调用变量中的值）：

133 # The mydestination parameter specifies the list of domains that this
134 # machine considers itself the final destination for.
135 #
136 # These domains are routed to the delivery agent specified with the
137 # local_transport parameter setting. By default, that is the UNIX
138 # compatible delivery agent that lookups all recipients in /etc/passwd
139 # and /etc/aliases or their equivalent.
140 #
141 # The default is $myhostname + localhost.$mydomain. On a mail domain
142 # gateway, you should also include $mydomain.
143 #
144 # Do not specify the names of virtual domains - those domains are
145 # specified elsewhere (see VIRTUAL_README).
146 #
147 # Do not specify the names of domains that this machine is backup MX
148 # host for. Specify those names via the relay_domains settings for
149 # the SMTP server, or use permit_mx_backup if you are lazy (see
150 # STANDARD_CONFIGURATION_README).
151 #
152 # The local machine is always the final destination for mail addressed
153 # to user@[the.net.work.address] of an interface that the mail system
154 # receives mail on (see the inet_interfaces parameter).
155 #
156 # Specify a list of host or domain names, /file/name or type:table
157 # patterns, separated by commas and/or whitespace. A /file/name
158 # pattern is replaced by its contents; a type:table is matched when
159 # a name matches a lookup key (the right-hand side is ignored).
160 # Continue long lines by starting the next line with whitespace.
161 #
162 # See also below, section "REJECTING MAIL FOR UNKNOWN LOCAL USERS".
163 #
164 mydestination = $myhostname , $mydomain
165 #mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
166 #mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain,
```

第3步：创建电子邮件系统的登录账户。Postfix与vsftpd服务程序一样，都可以调用本地系统的账户和密码，因此在本地系统创建常规账户即可。最后重启配置妥当的postfix服务程序，并将其添加到开机启动项中。大功告成！

```shell
[root@linuxprobe ~]# useradd boss
[root@linuxprobe ~]# echo "linuxprobe" | passwd --stdin boss
Changing password for user boss. passwd: all authentication tokens updated successfully.
[root@linuxprobe ~]# systemctl restart postfix
[root@linuxprobe ~]# systemctl enable postfix
ln -s '/usr/lib/systemd/system/postfix.service' '/etc/systemd/system/multi-user.target.wants/postfix.service'
```

### 配置Dovecot服务程序

Dovecot是一款能够为Linux系统提供IMAP和POP3电子邮件服务的开源服务程序，安全性极高，配置简单，执行速度快，而且占用的服务器硬件资源也较少，因此是一款值得推荐的收件服务程序。

第1步：安装Dovecot服务程序软件包。大家可自行配置Yum软件仓库、挂载光盘镜像到指定目录，然后输入要安装的dovecot软件包名称即可：

```shell
[root@linuxprobe ~]# yum install dovecot
Loaded plugins: langpacks, product-id, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
rhel | 4.1 kB 00:00 
Resolving Dependencies
--> Running transaction check
---> Package dovecot.x86_64 1:2.2.10-4.el7 will be installed
--> Processing Dependency: libclucene-core.so.1()(64bit) for package: 1:dovecot-2.2.10-4.el7.x86_64
--> Processing Dependency: libclucene-shared.so.1()(64bit) for package: 1:dovecot-2.2.10-4.el7.x86_64
--> Running transaction check
---> Package clucene-core.x86_64 0:2.3.3.4-11.el7 will be installed
--> Finished Dependency Resolution
Dependencies Resolved
================================================================================
 Package Arch Version Repository Size
================================================================================
Installing:
 dovecot x86_64 1:2.2.10-4.el7 rhel 3.2 M
Installing for dependencies:
 clucene-core x86_64 2.3.3.4-11.el7 rhel 528 k
Transaction Summary
================================================================================
Install 1 Package (+1 Dependent package)
Total download size: 3.7 M
Installed size: 12 M
Is this ok [y/d/N]: y
Downloading packages:
--------------------------------------------------------------------------------
Total 44 MB/s | 3.7 MB 00:00 
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
 Installing : clucene-core-2.3.3.4-11.el7.x86_64 1/2 
 Installing : 1:dovecot-2.2.10-4.el7.x86_64 2/2 
 Verifying : 1:dovecot-2.2.10-4.el7.x86_64 1/2 
 Verifying : clucene-core-2.3.3.4-11.el7.x86_64 2/2 
Installed:
 dovecot.x86_64 1:2.2.10-4.el7 
Dependency Installed:
 clucene-core.x86_64 0:2.3.3.4-11.el7 
Complete!
```

第2步：配置部署Dovecot服务程序。在Dovecot服务程序的主配置文件中进行如下修改。首先是第24行，把Dovecot服务程序支持的电子邮件协议修改为imap、pop3和lmtp。然后在这一行下面添加一行参数，允许用户使用明文进行密码验证。之所以这样操作，是因为Dovecot服务程序为了保证电子邮件系统的安全而默认强制用户使用加密方式进行登录，而由于当前还没有加密系统，因此需要添加该参数来允许用户的明文登录。

```shell
[root@linuxprobe ~]# vim /etc/dovecot/dovecot.conf
………………省略部分输出信息………………
23 # Protocols we want to be serving.
24 protocols = imap pop3 lmtp
25 disable_plaintext_auth = no
………………省略部分输出信息………………
在主配置文件中的第48行，设置允许登录的网段地址，也就是说我们可以在这里限制只有来自于某个网段的用户才能使用电子邮件系统。如果想允许所有人都能使用，则不用修改本参数：

44 # Space separated list of trusted network ranges. Connections from these
45 # IPs are allowed to override their IP addresses and ports (for logging and
46 # for authentication checks). disable_plaintext_auth is also ignored for
47 # these networks. Typically you'd specify your IMAP proxy servers here.
48 login_trusted_networks = 192.168.10.0/24
第3步：配置邮件格式与存储路径。在Dovecot服务程序单独的子配置文件中，定义一个路径，用于指定要将收到的邮件存放到服务器本地的哪个位置。这个路径默认已经定义好了，我们只需要将该配置文件中第24行前面的井号（#）删除即可。

[root@linuxprobe ~]# vim /etc/dovecot/conf.d/10-mail.conf
1 ##
2 ## Mailbox locations and namespaces
3 ##
4 # Location for users' mailboxes. The default is empty, which means that Dovecot
5 # tries to find the mailboxes automatically. This won't work if the user
6 # doesn't yet have any mail, so you should explicitly tell Dovecot the full
7 # location.
8 #
9 # If you're using mbox, giving a path to the INBOX file (eg. /var/mail/%u)
10 # isn't enough. You'll also need to tell Dovecot where the other mailboxes are
11 # kept. This is called the "root mail directory", and it must be the first
12 # path given in the mail_location setting.
13 #
14 # There are a few special variables you can use, eg.:
15 #
16 # %u - username
17 # %n - user part in user@domain, same as %u if there's no domain
18 # %d - domain part in user@domain, empty if there's no domain
19 # %h - home directory
20 #
21 # See doc/wiki/Variables.txt for full list. Some examples:
22 #
23 # mail_location = maildir:~/Maildir
24 mail_location = mbox:~/mail:INBOX=/var/mail/%u
25 # mail_location = mbox:/var/mail/%d/%1n/%n:INDEX=/var/indexes/%d/%1n/%n
………………省略部分输出信息………………
然后切换到配置Postfix服务程序时创建的boss账户，并在家目录中建立用于保存邮件的目录。记得要重启Dovecot服务并将其添加到开机启动项中。至此，对Dovecot服务程序的配置部署步骤全部结束。

[root@linuxprobe ~]# su - boss
Last login: Sat Aug 15 16:15:58 CST 2017 on pts/1
[boss@mail ~]$ mkdir -p mail/.imap/INBOX
[boss@mail ~]$ exit
[root@linuxprobe ~]# systemctl restart dovecot 
[root@linuxprobe ~]# systemctl enable dovecot 
ln -s '/usr/lib/systemd/system/dovecot.service' '/etc/systemd/system/multi-user.target.wants/dovecot.service'
```

15.2.3 客户使用电子邮件系统
如何得知电子邮件系统已经能够正常收发邮件了呢？可以使用Windows操作系统中自带的Outlook软件来进行测试（也可以使用其他电子邮件客户端来测试，比如Foxmail）。请按照表15-2来设置电子邮件系统及DNS服务器和客户端主机的IP地址，以便能正常解析邮件域名。设置后的结果如图15-5所示。

表15-2                                    服务器与客户端的操作系统与IP地址

主机名称	操作系统	IP地址
电子邮件系统及DNS服务器	RHEL 7	192.168.10.10
客户端主机	Windows 7	192.168.10.30
第15章 使用Postfix与Dovecot部署邮件系统。第15章 使用Postfix与Dovecot部署邮件系统。

图15-5  配置Windows 7系统的网络参数

第1步：在Windows 7系统中运行Outlook软件程序。由于各位读者使用的Windows7系统版本不一定相同，因此刘遄老师决定采用Outlook 2007版本为对象进行实验。如果您想要与这里的实验环境尽量保持一致，可在本书配套站点的软件资源库页面（http://www. linuxprobe.com/ tools）下载并安装。在初次运行该软件时会出现一个“Outlook 2007启动”页面，引导大家完成该软件的配置过程，如图15-6所示。

第15章 使用Postfix与Dovecot部署邮件系统。第15章 使用Postfix与Dovecot部署邮件系统。

图15-6  Outlook 2007启动向导

第2步：配置电子邮件账户。在图15-7所示的“账户设置”页面中单击“是”单选按钮，然后单击“下一步”按钮。

第15章 使用Postfix与Dovecot部署邮件系统。第15章 使用Postfix与Dovecot部署邮件系统。

图15-7  配置电子邮件账户

第3步：选择电子邮件服务的协议类型。在图15-8所示的页面中接受默认设置，然后单击“下一步”按钮。

第15章 使用Postfix与Dovecot部署邮件系统。第15章 使用Postfix与Dovecot部署邮件系统。

图15-8  选择电子邮件服务的协议类型

第4步：填写电子邮件账户信息，在图15-9所示的页面中，“您的姓名”文本框中可以为自定义的任意名字，“电子邮件地址”文本框中则需要输入服务器系统内的账户名外加发件域，“密码”文本框中要输入该账户在服务器内的登录密码。在填写完毕之后，单击“下一步”按钮。

第15章 使用Postfix与Dovecot部署邮件系统。第15章 使用Postfix与Dovecot部署邮件系统。

图15-9  填写电子邮件账户信息

第5步：进行电子邮件服务登录验证。由于当前没有可用的SSL加密服务，因此在Dovecot服务程序的主配置文件中写入了一条参数，让客户可以使用明文登录到电子邮件服务。Outlook软件默认会通过SSL加密协议尝试登录电子邮件服务，所以在进行图15-10所示的“搜索boss@linuxprobe.com服务器设置”大约30～60秒后，系统会出现登录失败的报错信息。此时只需再次单击“下一步”按钮，即可让Outlook软件通过非加密的方式验证登录，如图15-11所示。

第15章 使用Postfix与Dovecot部署邮件系统。第15章 使用Postfix与Dovecot部署邮件系统。

图15-10  进行电子邮件服务验证登录

第15章 使用Postfix与Dovecot部署邮件系统。第15章 使用Postfix与Dovecot部署邮件系统。

图15-11  使用非加密的方式进行电子邮件服务验证登录

第6步：向其他信箱发送邮件。在成功登录Outlook软件后即可尝试编写并发送新邮件了。只需在软件界面的空白处单击鼠标右键，在弹出的菜单中选择“新邮件”命令（见图15-12），然后在邮件界面中填写收件人的信箱地址以及完整的邮件内容后单击“发送”按钮，如图15-13所示。

第15章 使用Postfix与Dovecot部署邮件系统。第15章 使用Postfix与Dovecot部署邮件系统。

图15-12  向其他信箱发送邮件

第15章 使用Postfix与Dovecot部署邮件系统。第15章 使用Postfix与Dovecot部署邮件系统。

图15-13  填写收件人信箱地址并编写完整的邮件内容

当使用Outlook软件成功发送邮件后，便可以在电子邮件服务器上使用mail命令查看到新邮件提醒了。如果想查看邮件的完整内容，只需输入收件人姓名前面的编号即可。

[root@linuxprobe ~]# mail
Heirloom Mail version 12.5 7/5/10.Type ? for help.
"/var/mail/root": 3 messages 3 unread >
U 1 user@localhost.com Fri Jul 10 09:58 1631/123113 "[abrt] full crash r" 
U 2 Anacron Sat Aug 15 13:33 18/624 "Anacron job 'cron.dai" 
U 3 boss Sat Aug 15 19:02 118/3604 "Hello~" 
&> 3
Message 3:
From boss@linuxprobe.com Sat Aug 15 19:02:06 2017 
Return-Path: 
X-Original-To: root@linuxprobe.com 
Delivered-To: root@linuxprobe.com 
From: "boss" 
To: 
Subject: Hello~
Date: Sat, 15 Aug 2017 19:02:06 +0800
Content-Type: text/plain; charset="gb2312" 
………………省略部分输出信息………………
当您收到这封邮件时，证明我的邮局系统实验已经成功！
> quit 
Held 3 messages in /var/mail/root

15.3 设置用户别名邮箱
用户别名功能是一项简单实用的邮件账户伪装技术，可以用来设置多个虚拟信箱的账户以接受发送的邮件，从而保证自身的邮件地址不被泄露，还可以用来接收自己的多个信箱中的邮件。刚才我们已经顺利地向root账户送了邮件，下面再向bin账户发送一封邮件，如图15-14所示。

第15章 使用Postfix与Dovecot部署邮件系统。第15章 使用Postfix与Dovecot部署邮件系统。

图15-14  向服务器上的bin账户发送邮件

在邮件发送后登录到服务器，然后尝试以bin账户的身份登录。由于bin账户在Linux系统中是系统账户，默认的Shell终端是/sbin/nologin，因此在以bin账户登录时，系统会提示当前账户不可用。但是，在电子邮件服务器上使用mail命令后，却看到这封原本要发送给bin账户的邮件已经被存放到了root账户的信箱中。

[root@linuxprobe ~]# su - bin 
This account is currently not available. 
[root@linuxprobe ~]# mail
Heirloom Mail version 12.5 7/5/10. 
Type ? for help. 
"/var/mail/root": 4 messages 4 new > 
U 1 user@localhost.com Fri Jul 10 09:58 1630/123103 "[abrt] full crash r" 
U 2 Anacron Wed Aug 19 17:47 17/619 "Anacron job 'cron.dai" 
U 3 boss Sat Aug 15 19:02 118/3604 "Hello~" U 
4 boss Wed Aug 19 18:49 116/3231 "你好，用户Bin。" 
&> 4 
Message 4: 
From boss@linuxprobe.com Wed Aug 19 18:49:05 2017 
Return-Path: <boss@linuxprobe.com> 
X-Original-To: bin@linuxprobe.com 
Delivered-To: bin@linuxprobe.com 
From: "boss" <boss@linuxprobe.com> 
To: <bin@linuxprobe.com>
Subject: 你好，用户Bin。 
Date: Wed, 19 Aug 2017 18:49:05 +0800 
Content-Type: multipart/alternative; boundary="----=_NextPart_000_0006_01D0DAAF.
B9104E90" 
X-Mailer: Microsoft Office Outlook 12.0 Thread-Index: AdDabKrQzUHVBTgRQMaCtUs
VtqfL1Q== Content-Language: zh-cn Status: R Content-Type: text/plain; charset="gb2312"
………………省略部分输出信息………………
这是一封发给用户Bin的文件。
&> quit
Held 4 messages in /var/mail/root
太奇怪了！明明发送给bin账户的邮件怎么会被root账户收到了呢？其实，这就是使用用户别名技术来实现的。在aliases邮件别名服务的配置文件中可以看到，里面定义了大量的用户别名，这些用户别名大多数是Linux系统本地的系统账户，而在冒号（:）间隔符后面的root账户则是用来接收这些账户邮件的人。用户别名可以是Linux系统内的本地用户，也可以是完全虚构的用户名字。

下述命令会显示大量的内容，考虑到篇幅限制，这里已经做了部分删减，其实际的输出名单将是这里的两倍多。

[root@linuxprobe ~]# cat /etc/aliases
#
# Aliases in this file will NOT be expanded in the header from
# Mail, but WILL be visible over networks or from /bin/mail.
#
# >>>>>>>>>> The program "newaliases" must be run after
# >> NOTE >> this file is updated for any changes to
# >>>>>>>>>> show through to sendmail.
#
# Basic system aliases -- these MUST be present.
mailer-daemon: postmaster
postmaster: root
# General redirections for pseudo accounts.
bin: root
daemon: root
adm: root
lp: root
sync: root
shutdown: root
halt: root
mail: root
news: root
uucp: root
operator: root
games: root
gopher: root
ftp: root
nobody: root
radiusd: root
nut: root
dbus: root
vcsa: root
canna: root
wnn: root
rpm: root
nscd: root
pcap: root
apache: root
webalizer: root
dovecot: root
fax: root
quagga: root
radvd: root
pvm: root
amandabackup: root
privoxy: root
ident: root
named: root
xfs: root
gdm: root
mailnull: root
postgres: root
sshd: root
smmsp: root
postfix: root
netdump: root
ldap: root
squid: root
ntp: root
mysql: root
desktop: root
rpcuser: root
rpc: root
nfsnobody: root
ingres: root
system: root
toor: root
manager: root
dumper: root
abuse: root
newsadm: news
newsadmin: news
usenet: news
ftpadm: ftp
ftpadmin: ftp
ftp-adm: ftp
ftp-admin: ftp
www: webmaster
webmaster: root
noc: root
security: root
hostmaster: root
info: postmaster
marketing: postmaster
sales: postmaster
support: postmaster
# trap decode to catch security attacks
decode: root
# Person who should get root's mail
#root: marc
现在大家能猜出是怎么一回事了吧。原来aliases邮件别名服务的配置文件是专门用来定义用户别名与邮件接收人的映射。除了使用本地系统中系统账户的名称外，我们还可以自行定义一些别名来接收邮件。例如，创建一个名为xxoo的账户，而真正接收该账户邮件的应该是root账户。

[root@linuxprobe ~]# cat /etc/aliases
#
# Aliases in this file will NOT be expanded in the header from
# Mail, but WILL be visible over networks or from /bin/mail.
#
# >>>>>>>>>> The program "newaliases" must be run after
# >> NOTE >> this file is updated for any changes to
# >>>>>>>>>> show through to sendmail.
#
# Basic system aliases -- these MUST be present.
mailer-daemon: postmaster
postmaster: root
# General redirections for pseudo accounts.
xxoo: root
bin: root
daemon: root
adm: root
lp: root
………………省略部分输出信息………………
保存并退出aliases邮件别名服务的配置文件后，需要再执行一下newaliases命令，其目的是让新的用户别名配置文件立即生效。然后再次尝试发送邮件，如图15-15所示：第15章 使用Postfix与Dovecot部署邮件系统。第15章 使用Postfix与Dovecot部署邮件系统。

图15-15  向服务器上的xxoo账户发送邮件

这时，使用root账户在服务器上执行mail命令后，就能看到这封原本要发送给xxoo账户的邮件了。最后，刘遄老师再啰嗦一句，用户别名技术不仅应用广泛，而且配置也很简单。所以更要提醒大家的是，今后千万不要看到有些网站上提供了很多客服信箱就轻易相信别人，没准发往这些客服信箱的邮件会被同一个人收到。

[root@linuxprobe ~]# mail
Heirloom Mail version 12.5 7/5/10. Type ? for help.
"/var/mail/root": 5 messages 1 new 4 unread
U 1 user@localhost.com Fri Jul 10 09:58 1631/123113 "[abrt] full crash report"
U 2 Anacron Wed Aug 19 17:47 18/629 "Anacron job 'cron.daily' on mail.linuxprobe.com"
U 3 boss Wed Aug 19 18:44 114/2975 "hello"
4 boss Wed Aug 19 18:49 117/3242 "你好，用户Bin。"
>N 5 boss Wed Aug 19 19:18 115/3254 "这是一封发送给xxoo用户的邮件。"
出现问题?大胆提问!

因读者们硬件不同或操作错误都可能导致实验配置出错，请耐心再仔细看看操作步骤吧，不要气馁~

Linux技术交流请加A群：560843(满)，B群：340829(推荐)，C群：463590（推荐），点此查看全国群。

*本群特色：通过口令验证确保每一个群员都是《Linux就该这么学》的读者，答疑更有针对性，不定期免费领取定制礼品。

本章节的复习作业(答案就在问题的下一行哦，用鼠标选中即可看到的~)

1．电子邮件服务与HTTP、FTP、NFS等程序的服务模式的最大区别是什么？

答：当对方主机宕机或对方临时离线时，使用电子邮件服务依然可以发送数据。

2．常见的电子邮件协议有那些？

答：SMTP、POP3和IMAP4。

3．电子邮件系统中MUA、MTA、MDA三种服务角色的用途分别是什么？

答：MUA用于收发邮件、MTA用于转发邮件、MDA用于保存邮件。

4．使用Postfix与Dovecot部署电子邮件系统前，需要先做什么？

答：需要先配置部署DNS域名解析服务，以便提供信箱地址解析功能。

5．能否让Dovecot服务程序限制允许连接的主机范围？

答：可以，在Dovecot服务程序的主配置文件中修改login_trusted_networks参数值即可，这样可在不修改防火墙策略的情况下限制来访的主机范围。

6．使用Outlook软件连接电子邮件服务器的地址mail.linuxprobe.com时，提示找不到服务器或连接超时，这可能是什么原因导致的呢？

答：很有可能是DNS域名解析问题引起的连接超时，可在服务器与客户端分别执行ping mail.linuxprobe.com 命令，测试是否可以正常解析出IP地址。

7．如何定义用户别名信箱以及让其立即生效？

答：可直接修改邮件别名服务的配置文件，并在保存退出后执行newaliases命令即可让新的用户别名立即生效。