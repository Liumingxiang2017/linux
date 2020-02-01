# 使用OpenLDAP部署目录服务

本章目录结构 [收起]

23.1 了解目录服务
23.2 目录服务实验
23.2.1 配置LDAP服务端
23.2.2 配置LDAP客户端
23.3 自动挂载用户目录
23.1 了解目录服务

回忆前面所学的章节，我们发现其实目录可以被理解成是一种为查询、浏览或搜索的数据库，但数据库又分为了目录数据库和关系数据库，目录数据库主要用于存储较小的信息（如姓名、电话、主机名等），同时具有很好的读性能，但在写性能方面比较差，所以不适合存放那些需要经常修改的数据。

1. 信息短小
2. 读取多，写入少
3. 不经常修改

目录服务则是由目录数据库和一套能够访问和处理数据库信息的协议组成的服务协议，用于集中的管理主机帐号密码，员工名字等数据，大大的提升了管理工作效率。轻量级目录访问协议LDAP(Lightweight Directory Access Protocol)是在目录访问协议X.500的基础上研发的，主要的优势是：

X.500目录协议功能非常臃肿，消耗大量资源，无法做到快速查询且不支持TCP/IP协议网络。

LDAP采用树状结构存储数据（类似于前面学习的DNS服务程序），用于在IP网络层面实现对分布式目录的访问和管理操作，条目是LDAP协议中最基本的元素，可以想象成字典中的单词或者数据库中的记录，通常对LDAP服务程序的添加、删除、更改、搜索都是以条目为基本对象的。
第23章 使用OpenLDAP部署目录服务。第23章 使用OpenLDAP部署目录服务。

LDAP树状结构存储数据

dn:每个条目的唯一标识符，如上图中linuxprobe的dn值是：

cn=linuxprobe,ou=marketing,ou=people,dc=mydomain,dc=org
rdn:一般为dn值中最左侧的部分，如上图中linuxprobe的rdn值是：

cn=linuxprobe
base DN:此为基准DN值，表示顶层的根部，上图中的base DN值是：

dc=mydomain,dc=org
而每个条目可以有多个属性（如姓名、地址、电话等），每个属性中会保存着对象名称与对应值，LDAP已经为运维人员对常见的对象定义了属性，其中有：

属性名称	属性别名	语法	描述	值（举例）
commonName	cn	Directory String	名字	sean
surname	sn	Directory String	姓氏	Chow
organizationalUnitName	ou	Directory String	单位（部门）名称	IT_SECTION
organization	o	Directory String	组织（公司）名称	linuxprobe
telephoneNumber		Telephone Number	电话号码	911
objectClass			内置属性	organizationalPerson

23.2 目录服务实验
OpenLdap是基于LDAP协议的开源程序，它的程序名称叫做slapd，本次实验需要用到两台主机：

主机名称	操作系统	IP地址
LDAP服务端
(instructor.linuxprobe.com)	红帽RHEL7操作系统	192.168.10.10
LDAP客户端	红帽RHEL7操作系统	192.168.10.20
23.2.1 配置LDAP服务端
安装openldap与相关的软件包：

[root@linuxprobe ~]# yum install -y openldap openldap-clients openldap-servers migrationtools
Loaded plugins: langpacks, product-id, subscription-manager
………………省略部分安装过程………………
Installing:
 migrationtools          noarch        47-15.el7             rhel7         26 k
 openldap-clients        x86_64        2.4.39-3.el7          rhel7        183 k
 openldap-servers        x86_64        2.4.39-3.el7          rhel7        2.1 M
………………省略部分安装过程………………
Complete!
生成密钥文件（记下生成出的值，后面要用）：

[root@linuxprobe ~]# slappasswd -s linuxprobe -n > /etc/openldap/passwd
[root@linuxprobe ~]# cat /etc/openldap/passwd 
{SSHA}v/GJvGG8SbIuCxhfTDVhkmWEuz2afNIR
写入一条主机与IP地址的解析记录：

[root@linuxprobe ~]# echo "192.168.10.10 instructor.linuxprobe.com" >> /etc/hosts
因为LDAP目录服务是以明文的方式在网络中传输数据的（包括密码），这样真的很不安全，所以我们采用TLS加密机制来解决这个问题，使用openssl工具生成X509格式的证书文件（有效期为365天）：

```shell
[cc lang="bash"]
# req 注册 -new 新的密钥文件 -nodes 自己是一个节点 -out 输出到公钥文件
# -keyout 输出到私钥文件
[root@linuxprobe ~]# openssl req -new -x509 -nodes -out /etc/openldap/certs/cert.pem -keyout /etc/openldap/certs/priv.pem -days 365
Generating a 2048 bit RSA private key
..........................................+++
..............................................................+++
writing new private key to '/etc/openldap/certs/priv.pem'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [XX]:敲击回车
State or Province Name (full name) []:敲击回车
Locality Name (eg, city) [Default City]:敲击回车
Organization Name (eg, company) [Default Company Ltd]:敲击回车
Organizational Unit Name (eg, section) []:敲击回车
Common Name (eg, your name or your server hostname) []:instructor.linuxprobe.com
Email Address []:敲击回车
[/cc]

```

修改证书的所属与权限：

```shell
[root@linuxprobe ~]# cd /etc/openldap/certs/
[root@linuxprobe certs]# chown ldap:ldap *
[root@linuxprobe certs]# chmod 600 priv.pem
[root@linuxprobe certs]# ls -al
total 8
drwxr-xr-x. 2 root root 36 Oct 5 13:41 .
drwxr-xr-x. 5 root root 100 Oct 5 13:39 ..
-rw-r--r--. 1 ldap ldap 1318 Oct 5 13:41 cert.pem
-rw-------. 1 ldap ldap 1704 Oct 5 13:41 priv.pem
```

复制一份LDAP的配置模板：

```shell
[root@linuxprobe ~]# cp /usr/share/openldap-servers/DB_CONFIG.example /var/lib/ldap/DB_CONFIG
```

生成数据库文件（不用担心报错信息）：

```shell
[root@linuxprobe ~]# slaptest 
5610aaa9 hdb_db_open: database "dc=my-domain,dc=com": db_open(/var/lib/ldap/id2entry.bdb) failed: No such file or directory (2).
5610aaa9 backend_startup_one (type=hdb, suffix="dc=my-domain,dc=com"): bi_db_open failed! (2)
slap_startup failed (test would succeed using the -u switch)
```

修改LDAP数据库的所属主与组：

```shell
[root@linuxprobe ~]# chown ldap:ldap /var/lib/ldap/*
```

启动slapd服务程序并设置为开机启动：

```shell
[cc lang="bash"]
[root@linuxprobe ~]# systemctl restart slapd
[root@linuxprobe ~]# systemctl enable slapd
ln -s '/usr/lib/systemd/system/slapd.service' '/etc/systemd/system/multi-user.target.wants/slapd.service'
[/cc]
```

在LDAP目录服务中使用LDIF(LDAP Interchange Format)格式来保存信息，而LDIF是一种标准的文本文件且可以随意的导入导出，所以我们需要有一种“格式”标准化LDIF文件的写法，这中格式叫做“schema”，schema用于指定一个目录中所包含对象的类型，以及每一个类型中的可选属性，我们可以将schema理解为面向对象程序设计中的“类”，通过“类”定义出具体的对象，因此其实LDIF数据条目则都是通过schema数据模型创建出来的具体对象：

ldapadd命令用于将LDIF文件导入到目录服务数据库中，格式为：“ldapadd [参数] LDIF文件”。

参数	作用
-x	进行简单认证。
-D	用于绑定服务器的dn。
-h：	目录服务的地址。
-w：	绑定dn的密码。
-f：	使用LDIF文件进行条目添加的文件。

添加cosine和nis模块：

```shell
[root@linuxprobe ~]# cd /etc/openldap/schema/
[root@linuxprobe schema]# ldapadd -Y EXTERNAL -H ldapi:/// -D "cn=config" -f cosine.ldif
SASL/EXTERNAL authentication started
SASL username: gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth
SASL SSF: 0
adding new entry "cn=cosine,cn=schema,cn=config"
[root@linuxprobe schema]# ldapadd -Y EXTERNAL -H ldapi:/// -D "cn=config" -f nis.ldif
SASL/EXTERNAL authentication started
SASL username: gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth
SASL SSF: 0
adding new entry "cn=nis,cn=schema,cn=config"
```

创建/etc/openldap/changes.ldif文件，并将下面的信息复制进去（注意有一处要修改的地方）：

```shell
[root@linuxprobe ~]# vim /etc/openldap/changes.ldif
dn: olcDatabase={2}hdb,cn=config
changetype: modify
replace: olcSuffix
olcSuffix: dc=linuxprobe,dc=com

dn: olcDatabase={2}hdb,cn=config
changetype: modify
replace: olcRootDN
olcRootDN: cn=Manager,dc=linuxprobe,dc=com

dn: olcDatabase={2}hdb,cn=config
changetype: modify
replace: olcRootPW
olcRootPW: 此处输入之前生成的密码（如{SSHA}v/GJvGG8SbIuCxhfTDVhkmWEuz2afNIR）

dn: cn=config
changetype: modify
replace: olcTLSCertificateFile
olcTLSCertificateFile: /etc/openldap/certs/cert.pem

dn: cn=config
changetype: modify
replace: olcTLSCertificateKeyFile
olcTLSCertificateKeyFile: /etc/openldap/certs/priv.pem

dn: cn=config
changetype: modify
replace: olcLogLevel
olcLogLevel: -1

dn: olcDatabase={1}monitor,cn=config
changetype: modify
replace: olcAccess
olcAccess: {0}to * by dn.base="gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth" read by dn.base="cn=Manager,dc=linuxprobe,dc=com" read by * none
```

将新的配置文件更新到slapd服务程序：

```shell
# ldapmodify 修改
[root@linuxprobe ~]# ldapmodify -Y EXTERNAL -H ldapi:/// -f /etc/openldap/changes.ldif
SASL/EXTERNAL authentication started
SASL username: gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth
SASL SSF: 0
modifying entry "olcDatabase={2}hdb,cn=config"
modifying entry "olcDatabase={2}hdb,cn=config"
modifying entry "olcDatabase={2}hdb,cn=config"
modifying entry "cn=config"
modifying entry "cn=config"
modifying entry "cn=config"
modifying entry "olcDatabase={1}monitor,cn=config"
```

创建/etc/openldap/base.ldif文件，并将下面的信息复制进去：

```shell
[root@linuxprobe ~]# vim /etc/openldap/base.ldif
dn: dc=linuxprobe,dc=com
dc: linuxprobe
objectClass: top
objectClass: domain

dn: ou=People,dc=linuxprobe,dc=com
ou: People
objectClass: top
objectClass: organizationalUnit

dn: ou=Group,dc=linuxprobe,dc=com
ou: Group
objectClass: top
objectClass: organizationalUnit
```

创建目录的结构服务：

```shell
[cc lang="bash"]
[root@linuxprobe ~]# ldapadd -x -w linuxprobe -D cn=Manager,dc=linuxprobe,dc=com -f /etc/openldap/base.ldif
adding new entry "dc=linuxprobe,dc=com"
adding new entry "ou=People,dc=linuxprobe,dc=com"
adding new entry "ou=Group,dc=linuxprobe,dc=com"
[/cc]
```

创建测试用的用户：

```shell
[root@linuxprobe ~]# useradd -d /home/ldap ldapuser
```

设置帐户的迁移（修改第71与74行）：

```shell
[root@linuxprobe ~]# vim /usr/share/migrationtools/migrate_common.ph
$DEFAULT_MAIL_DOMAIN = "linuxprobe.com";
$DEFAULT_BASE = "dc=linuxprobe,dc=com";
```

将当前系统中的用户迁移至目录服务：

```shell
[cc lang="bash"]
[root@linuxprobe ~]# cd /usr/share/migrationtools/
[root@linuxprobe migrationtools]# grep ":10[0-9][0-9]" /etc/passwd > passwd
[root@linuxprobe migrationtools]# ./migrate_passwd.pl passwd users.ldif
[root@linuxprobe migrationtools]# ldapadd -x -w linuxprobe -D cn=Manager,dc=linuxprobe,dc=com -f users.ldif
adding new entry "uid=linuxprobe,ou=People,dc=linuxprobe,dc=com"
adding new entry "uid=ldapuser,ou=People,dc=linuxprobe,dc=com"
[/cc]
```

将当前系统中的用户组迁移至目录服务：

```shell
[cc lang="bash"]
[root@linuxprobe migrationtools]# grep ":10[0-9][0-9]" /etc/group > group
[root@linuxprobe migrationtools]# ./migrate_group.pl group groups.ldif
[root@linuxprobe migrationtools]# ldapadd -x -w linuxprobe -D cn=Manager,dc=linuxprobe,dc=com -f groups.ldif
adding new entry "cn=linuxprobe,ou=Group,dc=linuxprobe,dc=com"
adding new entry "cn=ldapuser,ou=Group,dc=linuxprobe,dc=com"
[/cc]
```

测试linuxprobe用户的配置文件：

[root@linuxprobe ~]# ldapsearch -x cn=ldapuser -b dc=linuxprobe,dc=com
# extended LDIF
#
# LDAPv3
# base <dc=linuxprobe,dc=com> with scope subtree
# filter: cn=ldapuser
# requesting: ALL
#

# ldapuser, People, linuxprobe.com
dn: uid=ldapuser,ou=People,dc=linuxprobe,dc=com
uid: ldapuser
cn: ldapuser
objectClass: account
objectClass: posixAccount
objectClass: top
objectClass: shadowAccount
userPassword:: e2NyeXB0fSQ2JFdtcXFveHFIJFFNaU1pZDAuL01KLnBrR1ZKLkdVSVlWalguTXh
 xLlB5Uk1IeGJseGdkVTBwOUxwcTBJT2huYnkwNFkzdXh1Zi9QaWFpUUtlLk0wUHdQNFpxRXJQV0cv
shadowLastChange: 16713
shadowMin: 0
shadowMax: 99999
shadowWarning: 7
loginShell: /bin/bash
uidNumber: 1001
gidNumber: 1001
homeDirectory: /home/ldapuser

# ldapuser, Group, linuxprobe.com
dn: cn=ldapuser,ou=Group,dc=linuxprobe,dc=com
objectClass: posixGroup
objectClass: top
cn: ldapuser
userPassword:: e2NyeXB0fXg=
gidNumber: 1001

# search result
search: 2
result: 0 Success

# numResponses: 3
# numEntries: 2
安装httpd服务程序：

[root@linuxprobe ~]# yum install httpd
Loaded plugins: langpacks, product-id, subscription-manager
………………省略部分安装过程………………
Installing:
 httpd               x86_64         2.4.6-17.el7            rhel7         1.2 M
Installing for dependencies:
 apr                 x86_64         1.4.8-3.el7             rhel7         103 k
 apr-util            x86_64         1.5.2-6.el7             rhel7          92 k
 httpd-tools         x86_64         2.4.6-17.el7            rhel7          77 k
 mailcap             noarch         2.1.41-2.el7            rhel7          31 k
………………省略部分安装过程………………
Complete!
将密钥文件上传至网站目录：

[root@linuxprobe ~]# cp /etc/openldap/certs/cert.pem /var/www/html
将httpd服务程序重启，并添加到开机启动项：
[cc lang="bash"]
[root@linuxprobe ~]# systemctl restart httpd
[root@linuxprobe ~]# systemctl enable httpd
ln -s '/usr/lib/systemd/system/httpd.service' '/etc/systemd/system/multi-user.target.wants/httpd.service'
[/cc]
清空防火墙的规则并保存状态：

[root@linuxprobe ~]# iptables -F
success
[root@linuxprobe ~]# service iptables save
success
在日志记录服务的配置文件中追加下面语句，并重启日志服务：

[root@linuxprobe ~]# vim /etc/rsyslog.conf
local4.* /var/log/ldap.log
[root@linuxprobe ~]# systemctl restart rsyslog
出现问题?大胆提问!

因读者们硬件不同或操作错误都可能导致实验配置出错，请耐心再仔细看看操作步骤吧，不要气馁~

Linux技术交流请加A群：560843(满)，B群：340829(推荐)，C群：463590（推荐），点此查看全国群。

*本群特色：通过口令验证确保每一个群员都是《Linux就该这么学》的读者，答疑更有针对性，不定期免费领取定制礼品。

23.2.2 配置LDAP客户端
将LDAP服务端主机名与IP地址的解析记录写入：

[root@linuxprobe ~]# echo "192.168.10.10 instructor.linuxprobe.com" >> /etc/hosts
安装相关的软件包：

[root@linuxprobe Desktop]#  yum install openldap-clients nss-pam-ldapd authconfig-gtk pam_krb5
Loaded plugins: langpacks, product-id, subscription-manager
………………省略部分的安装过程………………
Installing:
 authconfig-gtk          x86_64        6.2.8-8.el7            rhel        105 k
 nss-pam-ldapd           x86_64        0.8.13-8.el7           rhel        159 k
 openldap-clients        x86_64        2.4.39-3.el7           rhel        183 k
 pam_krb5                x86_64        2.4.8-4.el7            rhel        158 k
Installing for dependencies:
 nscd                    x86_64        2.17-55.el7            rhel        250 k
………………省略部分的安装过程………………
Complete!
运行系统认证工具，并填写LDAP服务信息：

[root@linuxprobe ~]# system-config-authentication
第23章 使用OpenLDAP部署目录服务。第23章 使用OpenLDAP部署目录服务。
填写证书地址：
第23章 使用OpenLDAP部署目录服务。第23章 使用OpenLDAP部署目录服务。
稍等片刻后，验证本地是否已经有了ldapuser用户：

[root@linuxprobe ~]# id ldapuser
uid=1001(ldapuser) gid=1001(ldapuser) groups=1001(ldapuser)
此时说明已经可以通过LDAP服务端验证了，并且ldapuser用户的帐号信息也不会保存在您本地的/etc/passwd文件中~

23.3 自动挂载用户目录
虽然在客户端已经能够使用LDAP验证帐户了，但是当切换到ldapuser用户时会提示没有该用户的家目录：

[root@linuxprobe ~]# su - ldapuser
su: warning: cannot change directory to /home/ldapuser: No such file or directory
mkdir: cannot create directory '/home/ldapuser': Permission denied
原因是本机并没有该用户的家目录，我们需要配置NFS服务将用户的家目录自动挂载过来：

在LDAP服务端添加共享信息（NFS服务程序已经默认安装，我们之前学过还记得吗？）：

[root@linuxprobe ~]# vim /etc/exports
/home/ldap 192.168.10.20 (rw,sync,root_squash)
重启nfs-server服务程序：

[root@linuxprobe ~]# systemctl restart nfs-server
在LDAP客户端查看共享信息：

[root@linuxprobe ldap]# showmount -e 192.168.10.10
Export list for 192.168.10.10:
/home/ldap 192.168.10.20
将共享目录挂载到本地：

[root@linuxprobe ~]# mkdir /home/ldap
[root@linuxprobe ldap]# mount -t nfs 192.168.10.10:/home/ldap /home/ldap
再次尝试切换到ldapuser用户，这样非常顺利：

[root@linuxprobe ldap]# su - ldapuser
Last login: Tue Oct  6 11:51:25 CST 2015 on pts/3
[ldapuser@linuxprobe ~]$
设置为开机自动挂载：

[root@linuxprobe ~]# vim /etc/fstab
192.168.10.10:/home/ldap /home/ldap nfs defaults 0 0
出现问题?大胆提问!

因读者们硬件不同或操作错误都可能导致实验配置出错，请耐心再仔细看看操作步骤吧，不要气馁~

Linux技术交流请加A群：560843(满)，B群：340829(推荐)，点此查看全国群。

*本群特色：通过口令验证确保每一个群员都是《Linux就该这么学》的读者，答疑更有针对性，不定期免费领取定制礼品。

本章节的复习作业(答案就在问题的下一行哦，用鼠标选中即可看到的~)

1:LDAP目录服务的特点是？

答案:消耗资源少，适合存储较小的信息、具有很好的读性能以及支持TCP/IP协议网络。

2:目录服务的唯一标识符dn的作用是？

答案:用于定义某个条目或属性的唯一性。

3:为什么需要启用TLS加密？

答案:因为openldap服务程序默认使用明文传送数据（包括密码）。

4:ldapadd命令的作用是？

答案:ldapadd命令用于将LDIF文件导入到目录服务数据库中。

5:部署目录服务后配置nfs服务的作用是？

答案:挂载用户的家目录。