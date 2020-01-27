# 使用BIND提供域名解析服务

## DNS域名解析服务

相较于由数字构成的IP地址，域名更容易被理解和记忆，所以我们通常更习惯通过域名的方式来访问网络中的资源。但是，网络中的计算机之间只能基于IP地址来相互识别对方的身份，而且要想在互联网中传输数据，也必须基于外网的IP地址来完成。

为了降低用户访问网络资源的门槛，DNS（Domain Name System，域名系统）技术应运而生。这是一项用于管理和解析域名与IP地址对应关系的技术，简单来说，就是能够接受用户输入的域名或IP地址，然后自动查找与之匹配（或者说具有映射关系）的IP地址或域名，即将域名解析为IP地址（正向解析），或将IP地址解析为域名（反向解析）。这样一来，我们只需要在浏览器中输入域名就能打开想要访问的网站了。DNS域名解析技术的正向解析也是我们最常使用的一种工作模式。

鉴于互联网中的域名和IP地址对应关系数据库太过庞大，DNS域名解析服务采用了类似目录树的层次结构来记录域名与IP地址之间的对应关系，从而形成了一个分布式的数据库系统，如图13-1所示。

第13章 使用Bind提供域名解析服务。第13章 使用Bind提供域名解析服务。

图13-1  DNS域名解析服务采用的目录树层次结构

域名后缀一般分为国际域名和国内域名。原则上来讲，域名后缀都有严格的定义，但在实际使用时可以不必严格遵守。目前最常见的域名后缀有.com（商业组织）、.org（非营利组织）、.gov（政府部门）、.net（网络服务商）、.edu（教研机构）、.pub（公共大众）、.cn（中国国家顶级域名）等。

当今世界的信息化程度越来越高，大数据、云计算、物联网、人工智能等新技术不断涌现，全球网民的数量据说也超过了35亿，而且每年还在以10%的速度迅速增长。这些因素导致互联网中的域名数量进一步激增，被访问的频率也进一步加大。假设全球网民每人每天只访问一个网站域名，而且只访问一次，也会产生35亿次的查询请求，如此庞大的请求数量肯定无法被某一台服务器全部处理掉。DNS技术作为互联网基础设施中重要的一环，为了为网民提供不间断、稳定且快速的域名查询服务，保证互联网的正常运转，提供了下面三种类型的服务器。

主服务器：在特定区域内具有唯一性，负责维护该区域内的域名与IP地址之间的对应关系。

从服务器：从主服务器中获得域名与IP地址的对应关系并进行维护，以防主服务器宕机等情况。

缓存服务器：通过向其他域名解析服务器查询获得域名与IP地址的对应关系，并将经常查询的域名信息保存到服务器本地，以此来提高重复查询时的效率。

简单来说，主服务器是用于管理域名和IP地址对应关系的真正服务器，从服务器帮助主服务器“打下手”，分散部署在各个国家、省市或地区，以便让用户就近查询域名，从而减轻主服务器的负载压力。缓存服务器不太常用，一般部署在企业内网的网关位置，用于加速用户的域名查询请求。

DNS域名解析服务采用分布式的数据结构来存放海量的“区域数据”信息，在执行用户发起的域名查询请求时，具有递归查询和迭代查询两种方式。所谓递归查询，是指DNS服务器在收到用户发起的请求时，必须向用户返回一个准确的查询结果。如果DNS服务器本地没有存储与之对应的信息，则该服务器需要询问其他服务器，并将返回的查询结果提交给用户。而迭代查询则是指，DNS服务器在收到用户发起的请求时，并不直接回复查询结果，而是告诉另一台DNS服务器的地址，用户再向这台DNS服务器提交请求，这样依次反复，直到返回查询结果。

由此可见，当用户向就近的一台DNS服务器发起对某个域名的查询请求之后（这里以www.linuxprobe.com为例），其查询流程大致如图13-2所示。

第13章 使用Bind提供域名解析服务。第13章 使用Bind提供域名解析服务。

图13-2  向DNS服务器发起域名查询请求的流程

当用户向网络指定的DNS服务器发起一个域名请求时，通常情况下会有本地由此DNS服务器向上级的DNS服务器发送迭代查询请求；如果该DNS服务器没有要查询的信息，则会进一步向上级DNS服务器发送迭代查询请求，直到获得准确的查询结果为止。其中最高级、最权威的根DNS服务器总共有13台，分布在世界各地，其管理单位、具体的地理位置，以及IP地址如表13-1所示。

表13-1                                        13台根DNS服务器的具体信息

名称	管理单位	地理位置	IP地址
A	INTERNIC.NET	美国-弗吉尼亚州	198.41.0.4
B	美国信息科学研究所	美国-加利弗尼亚州	128.9.0.107
C	PSINet公司	美国-弗吉尼亚州	192.33.4.12
D	马里兰大学	美国-马里兰州	128.8.10.90
E	美国航空航天管理局	美国加利弗尼亚州	192.203.230.10
F	因特网软件联盟	美国加利弗尼亚州	192.5.5.241
G	美国国防部网络信息中心	美国弗吉尼亚州	192.112.36.4
H	美国陆军研究所	美国-马里兰州	128.63.2.53
I	Autonomica公司	瑞典-斯德哥尔摩	192.36.148.17
J	VeriSign公司	美国-弗吉尼亚州	192.58.128.30
K	RIPE NCC	英国-伦敦	193.0.14.129
L	IANA	美国-弗吉尼亚州	199.7.83.42
M	WIDE Project	日本-东京	202.12.27.33
13.2 安装Bind服务程序
BIND（Berkeley Internet Name Domain，伯克利因特网名称域）服务是全球范围内使用最广泛、最安全可靠且高效的域名解析服务程序。DNS域名解析服务作为互联网基础设施服务，其责任之重可想而知，因此建议大家在生产环境中安装部署bind服务程序时加上chroot（俗称牢笼机制）扩展包，以便有效地限制bind服务程序仅能对自身的配置文件进行操作，以确保整个服务器的安全。

[root@linuxprobe ~]# yum install bind-chroot
Loaded plugins: langpacks, product-id, subscription-manager
………………省略部分输出信息………………
Installing:
 bind-chroot x86_64 32:9.9.4-14.el7 rhel 81 k
Installing for dependencies:
 bind x86_64 32:9.9.4-14.el7 rhel 1.8 M
Transaction Summary
================================================================================
Install 1 Package (+1 Dependent package)
Total download size: 1.8 M
Installed size: 4.3 M
Is this ok [y/d/N]: y
Downloading packages:
--------------------------------------------------------------------------------
Total 28 MB/s | 1.8 MB 00:00 
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
 Installing : 32:bind-9.9.4-14.el7.x86_64 1/2 
 Installing : 32:bind-chroot-9.9.4-14.el7.x86_64 2/2 
 Verifying : 32:bind-9.9.4-14.el7.x86_64 1/2 
 Verifying : 32:bind-chroot-9.9.4-14.el7.x86_64 2/2 
Installed:
 bind-chroot.x86_64 32:9.9.4-14.el7 
Dependency Installed:
 bind.x86_64 32:9.9.4-14.el7 
Complete!
bind服务程序的配置并不简单，因为要想为用户提供健全的DNS查询服务，要在本地保存相关的域名数据库，而如果把所有域名和IP地址的对应关系都写入到某个配置文件中，估计要有上千万条的参数，这样既不利于程序的执行效率，也不方便日后的修改和维护。因此在bind服务程序中有下面这三个比较关键的文件。

主配置文件（/etc/named.conf）：只有58行，而且在去除注释信息和空行之后，实际有效的参数仅有30行左右，这些参数用来定义bind服务程序的运行。

区域配置文件（/etc/named.rfc1912.zones）：用来保存域名和IP地址对应关系的所在位置。类似于图书的目录，对应着每个域和相应IP地址所在的具体位置，当需要查看或修改时，可根据这个位置找到相关文件。

数据配置文件目录（/var/named）：该目录用来保存域名和IP地址真实对应关系的数据配置文件。

在Linux系统中，bind服务程序的名称为named。首先需要在/etc目录中找到该服务程序的主配置文件，然后把第11行和第17行的地址均修改为any，分别表示服务器上的所有IP地址均可提供DNS域名解析服务，以及允许所有人对本服务器发送DNS查询请求。这两个地方一定要修改准确。

 [root@linuxprobe ~]# vim /etc/named.conf
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
 19 /* 
 20 - If you are building an AUTHORITATIVE DNS server, do NOT enable re cursion.
 1,1 Top
 21 - If you are building a RECURSIVE (caching) DNS server, you need to enable 
 22 recursion. 
 23 - If your recursive DNS server has a public IP address, you MUST en able access 
 24 control to limit queries to your legitimate users. Failing to do so will
 25 cause your server to become part of large scale DNS amplification 
 26 attacks. Implementing BCP38 within your network would greatly
 27 reduce such attack surface 
 28 */
 29 recursion yes;
 30 
 31 dnssec-enable yes;
 32 dnssec-validation yes;
 33 dnssec-lookaside auto;
 34 
 35 /* Path to ISC DLV key */
 36 bindkeys-file "/etc/named.iscdlv.key";
 37 
 38 managed-keys-directory "/var/named/dynamic";
 39 
 40 pid-file "/run/named/named.pid";
 41 session-keyfile "/run/named/session.key";
 42 };
 43 
 44 logging {
 45 channel default_debug {
 46 file "data/named.run";
 47 severity dynamic;
 48 };
 49 };
 50 
 51 zone "." IN {
 52 type hint;
 53 file "named.ca";
 54 };
 55 
 56 include "/etc/named.rfc1912.zones";
 57 include "/etc/named.root.key";
 58 
如前所述，bind服务程序的区域配置文件（/etc/named.rfc1912.zones）用来保存域名和IP地址对应关系的所在位置。在这个文件中，定义了域名与IP地址解析规则保存的文件位置以及服务类型等内容，而没有包含具体的域名、IP地址对应关系等信息。服务类型有三种，分别为hint（根区域）、master（主区域）、slave（辅助区域），其中常用的master和slave指的就是主服务器和从服务器。将域名解析为IP地址的正向解析参数和将IP地址解析为域名的反向解析参数分别如图13-3和图13-4所示。

第13章 使用Bind提供域名解析服务。第13章 使用Bind提供域名解析服务。

图13-3 正向解析参数

第13章 使用Bind提供域名解析服务。第13章 使用Bind提供域名解析服务。

图13-4 反向解析参数

下面的实验中会分别修改bind服务程序的主配置文件、区域配置文件与数据配置文件。如果在实验中遇到了bind服务程序启动失败的情况，而您认为这是由于参数写错而导致的，则可以执行named-checkconf命令和named-checkzone命令，分别检查主配置文件与数据配置文件中语法或参数的错误。

出现问题?大胆提问!

因读者们硬件不同或操作错误都可能导致实验配置出错，请耐心再仔细看看操作步骤吧，不要气馁~

Linux技术交流请加A群：560843(满)，B群：340829(推荐)，C群：463590（推荐），点此查看全国群。

*本群特色：通过口令验证确保每一个群员都是《Linux就该这么学》的读者，答疑更有针对性，不定期免费领取定制礼品。

13.2.1 正向解析实验
在DNS域名解析服务中，正向解析是指根据域名（主机名）查找到对应的IP地址。也就是说，当用户输入了一个域名后，bind服务程序会自动进行查找，并将匹配到的IP地址返给用户。这也是最常用的DNS工作模式。

第1步：编辑区域配置文件。该文件中默认已经有了一些无关紧要的解析参数，旨在让用户有一个参考。我们可以将下面的参数添加到区域配置文件的最下面，当然，也可以将该文件中的原有信息全部清空，而只保留自己的域名解析信息：

[root@linuxprobe ~]# vim /etc/named.rfc1912.zones
zone "linuxprobe.com" IN {
type master;
file "linuxprobe.com.zone";
allow-update {none;};
};
第2步：编辑数据配置文件。我们可以从/var/named目录中复制一份正向解析的模板文件（named.localhost），然后把域名和IP地址的对应数据填写数据配置文件中并保存。在复制时记得加上-a参数，这可以保留原始文件的所有者、所属组、权限属性等信息，以便让bind服务程序顺利读取文件内容：

[root@linuxprobe ~]# cd /var/named/
[root@linuxprobe named]# ls -al named.localhost
-rw-r-----. 1 root named 152 Jun 21 2007 named.localhost
[root@linuxprobe named]# cp -a named.localhost linuxprobe.com.zone
编辑数据配置文件。在保存并退出后文件后记得重启named服务程序，让新的解析数据生效。考虑到正向解析文件中的参数较多，而且相对都比较重要，刘遄老师在每个参数后面都作了简要的说明。

[root@linuxprobe named]# vim linuxprobe.com.zone
[root@linuxprobe named]# systemctl restart named
$TTL 1D	#生存周期为1天				
@	IN SOA	linuxprobe.com.	root.linuxprobe.com.	(	
#授权信息开始:	#DNS区域的地址	#域名管理员的邮箱(不要用@符号)	
0;serial	#更新序列号
1D;refresh	#更新时间
1H;retry	#重试延时
1W;expire	#失效时间
3H;)minimum	#无效解析记录的缓存时间
NS	ns.linuxprobe.com.	#域名服务器记录
ns	IN A	192.168.10.10	#地址记录(ns.linuxprobe.com.)
IN MX 10	mail.linuxprobe.com.	#邮箱交换记录
mail	IN A	192.168.10.10	#地址记录(mail.linuxprobe.com.)
www	IN A	192.168.10.10	#地址记录(www.linuxprobe.com.)
bbs	IN A	192.168.10.20	#地址记录(bbs.linuxprobe.com.)
第3步：检验解析结果。为了检验解析结果，一定要先把Linux系统网卡中的DNS地址参数修改成本机IP地址，这样就可以使用由本机提供的DNS查询服务了。nslookup命令用于检测能否从DNS服务器中查询到域名与IP地址的解析记录，进而更准确地检验DNS服务器是否已经能够为用户提供服务。

[root@linuxprobe ~]# systemctl restart network
[root@linuxprobe ~]# nslookup
> www.linuxprobe.com
Server: 127.0.0.1
Address: 127.0.0.1#53
Name: www.linuxprobe.com
Address: 192.168.10.10
> bbs.linuxprobe.com
Server: 127.0.0.1
Address: 127.0.0.1#53
Name: bbs.linuxprobe.com
Address: 192.168.10.20
13.2.2 反向解析实验
在DNS域名解析服务中，反向解析的作用是将用户提交的IP地址解析为对应的域名信息，它一般用于对某个IP地址上绑定的所有域名进行整体屏蔽，屏蔽由某些域名发送的垃圾邮件。它也可以针对某个IP地址进行反向解析，大致判断出有多少个网站运行在上面。当购买虚拟主机时，可以使用这一功能验证虚拟主机提供商是否有严重的超售问题。

第1步：编辑区域配置文件。在编辑该文件时，除了不要写错格式之外，还需要记住此处定义的数据配置文件名称，因为一会儿还需要在/var/named目录中建立与其对应的同名文件。反向解析是把IP地址解析成域名格式，因此在定义zone（区域）时应该要把IP地址反写，比如原来是192.168.10.0，反写后应该就是10.168.192，而且只需写出IP地址的网络位即可。把下列参数添加至正向解析参数的后面。

[root@linuxprobe ~]# vim /etc/named.rfc1912.zones
zone "linuxprobe.com" IN {
type master;
file "linuxprobe.com.zone";
allow-update {none;};
};
zone "10.168.192.in-addr.arpa" IN {
type master;
file "192.168.10.arpa";
};
第2步：编辑数据配置文件。首先从/var/named目录中复制一份反向解析的模板文件（named.loopback），然后把下面的参数填写到文件中。其中，IP地址仅需要写主机位，如图13-5所示。

第13章 使用Bind提供域名解析服务。第13章 使用Bind提供域名解析服务。

图13-5  反向解析文件中IP地址参数规范

[root@linuxprobe named]# cp -a named.loopback 192.168.10.arpa
[root@linuxprobe named]# vim 192.168.10.arpa
[root@linuxprobe named]# systemctl restart named
$TTL 1D				
@	IN SOA	linuxprobe.com.	root.linuxprobe.com.	(
0;serial
1D;refresh
1H;retry
1W;expire
3H);minimum
NS	ns.linuxprobe.com.	
ns	A	192.168.10.10	
10	PTR	ns.linuxprobe.com.	#PTR为指针记录，仅用于反向解析中。
10	PTR	mail.linuxprobe.com.	
10	PTR	www.linuxprobe.com.	
20	PTR	bbs.linuxprobe.com.	
第3步：检验解析结果。在前面的正向解析实验中，已经把系统网卡中的DNS地址参数修改成了本机IP地址，因此可以直接使用nslookup命令来检验解析结果，仅需输入IP地址即可查询到对应的域名信息。

[root@linuxprobe ~]# nslookup
> 192.168.10.10
Server: 127.0.0.1
Address: 127.0.0.1#53
10.10.168.192.in-addr.arpa name = ns.linuxprobe.com.
10.10.168.192.in-addr.arpa name = www.linuxprobe.com.
10.10.168.192.in-addr.arpa name = mail.linuxprobe.com.
> 192.168.10.20
Server: 127.0.0.1
Address: 127.0.0.1#53
20.10.168.192.in-addr.arpa name = bbs.linuxprobe.com.
13.3 部署从服务器
作为重要的互联网基础设施服务，保证DNS域名解析服务的正常运转至关重要，只有这样才能提供稳定、快速且不间断的域名查询服务。在DNS域名解析服务中，从服务器可以从主服务器上获取指定的区域数据文件，从而起到备份解析记录与负载均衡的作用，因此通过部署从服务器可以减轻主服务器的负载压力，还可以提升用户的查询效率。

在本实验中，主服务器与从服务器分别使用的操作系统和IP地址如表13-2所示。

表13-2                     主服务器与从服务器分别使用的操作系统与IP地址信息

主机名称	操作系统	IP地址
主服务器	RHEL 7	192.168.10.10
从服务器	RHEL 7	192.168.10.20
第1步：在主服务器的区域配置文件中允许该从服务器的更新请求，即修改allow-update {允许更新区域信息的主机地址;};参数，然后重启主服务器的DNS服务程序。

[root@linuxprobe ~]# vim /etc/named.rfc1912.zones
zone "linuxprobe.com" IN {
type master;
file "linuxprobe.com.zone";
allow-update { 192.168.10.20; };
};
zone "10.168.192.in-addr.arpa" IN {
type master;
file "192.168.10.arpa";
allow-update { 192.168.10.20; };
};
[root@linuxprobe ~]# systemctl restart named
第2步：在从服务器中填写主服务器的IP地址与要抓取的区域信息，然后重启服务。注意此时的服务类型应该是slave（从），而不再是master（主）。masters参数后面应该为主服务器的IP地址，而且file参数后面定义的是同步数据配置文件后要保存到的位置，稍后可以在该目录内看到同步的文件。

[root@linuxprobe ~]# vim /etc/named.rfc1912.zones
zone "linuxprobe.com" IN {
type slave;
masters { 192.168.10.10; };
file "slaves/linuxprobe.com.zone";
};
zone "10.168.192.in-addr.arpa" IN {
type slave;
masters { 192.168.10.10; };
file "slaves/192.168.10.arpa";
};
[root@linuxprobe ~]# systemctl restart named
第3步：检验解析结果。当从服务器的DNS服务程序在重启后，一般就已经自动从主服务器上同步了数据配置文件，而且该文件默认会放置在区域配置文件中所定义的目录位置中。随后修改从服务器的网络参数，把DNS地址参数修改成192.168.10.20，这样即可使用从服务器自身提供的DNS域名解析服务。最后就可以使用nslookup命令顺利看到解析结果了。

[root@linuxprobe ~]# cd /var/named/slaves
[root@linuxprobe slaves]# ls 
192.168.10.arpa linuxprobe.com.zone
[root@linuxprobe slaves]# nslookup
> www.linuxprobe.com
Server: 192.168.10.20
Address: 192.168.10.20#53
Name: www.linuxprobe.com
Address: 192.168.10.10
> 192.168.10.10
Server: 192.168.10.20
Address: 192.168.10.20#53
10.10.168.192.in-addr.arpa name = www.linuxprobe.com.
10.10.168.192.in-addr.arpa name = ns.linuxprobe.com.
10.10.168.192.in-addr.arpa name = mail.linuxprobe.com.
13.4 安全的加密传输
前文反复提及，域名解析服务是互联网基础设施中重要的一环，几乎所有的网络应用都依赖于DNS才能正常运行。如果DNS服务发生故障，那么即便Web网站或电子邮件系统服务等都正常运行，用户也无法找到并使用它们了。

互联网中的绝大多数DNS服务器（超过95%）都是基于BIND域名解析服务搭建的，而bind服务程序为了提供安全的解析服务，已经对TSIG（RFC 2845）加密机制提供了支持。TSIG主要是利用了密码编码的方式来保护区域信息的传输（Zone Transfer），即TSIG加密机制保证了DNS服务器之间传输域名区域信息的安全性。

接下来的实验依然使用了表13-2中的两台服务器。

书接上回。前面在从服务器上配妥bind服务程序并重启后，即可看到从主服务器中获取到的数据配置文件。

主机名称	操作系统	IP地址
主服务器	RHEL 7	192.168.10.10
从服务器	RHEL 7	192.168.10.20
[root@linuxprobe ~]# ls -al /var/named/slaves/
total 12
drwxrwx---. 2 named named 54 Jun 7 16:02 .
drwxr-x---. 6 root named 4096 Jun 7 15:58 ..
-rw-r--r--. 1 named named 432 Jun 7 16:02 192.168.10.arpa
-rw-r--r--. 1 named named 439 Jun 7 16:02 linuxprobe.com.zone
[root@linuxprobe ~]# rm -rf /var/named/slaves/*
第1步：在主服务器中生成密钥。dnssec-keygen命令用于生成安全的DNS服务密钥，其格式为“dnssec-keygen [参数]”，常用的参数以及作用如表13-3所示。

表13-3                                        dnssec-keygen命令的常用参数

参数	作用
-a	指定加密算法，包括RSAMD5（RSA）、RSASHA1、DSA、NSEC3RSASHA1、NSEC3DSA等
-b	密钥长度（HMAC-MD5的密钥长度在1~512位之间）
-n	密钥的类型（HOST表示与主机相关）
使用下述命令生成一个主机名称为master-slave的128位HMAC-MD5算法的密钥文件。在执行该命令后默认会在当前目录中生成公钥和私钥文件，我们需要把私钥文件中Key参数后面的值记录下来，一会儿要将其写入传输配置文件中。

[root@linuxprobe ~]# dnssec-keygen -a HMAC-MD5 -b 128 -n HOST master-slave
Kmaster-slave.+157+46845
[root@linuxprobe ~]# ls -al Kmaster-slave.+157+46845.*
-rw-------. 1 root root 56 Jun 7 16:06 Kmaster-slave.+157+46845.key
-rw-------. 1 root root 165 Jun 7 16:06 Kmaster-slave.+157+46845.private
[root@linuxprobe ~]# cat Kmaster-slave.+157+46845.private
Private-key-format: v1.3
Algorithm: 157 (HMAC_MD5)
Key: 1XEEL3tG5DNLOw+1WHfE3Q==
Bits: AAA=
Created: 20170607080621
Publish: 20170607080621
Activate: 20170607080621
第2步：在主服务器中创建密钥验证文件。进入bind服务程序用于保存配置文件的目录，把刚刚生成的密钥名称、加密算法和私钥加密字符串按照下面格式写入到tansfer.key传输配置文件中。为了安全起见，我们需要将文件的所属组修改成named，并将文件权限设置得要小一点，然后把该文件做一个硬链接到/etc目录中。

[root@linuxprobe ~]# cd /var/named/chroot/etc/
[root@linuxprobe etc]# vim transfer.key
key "master-slave" {
algorithm hmac-md5;
secret "1XEEL3tG5DNLOw+1WHfE3Q==";
};
[root@linuxprobe etc]# chown root:named transfer.key
[root@linuxprobe etc]# chmod 640 transfer.key
[root@linuxprobe etc]# ln transfer.key /etc/transfer.key
第3步：开启并加载Bind服务的密钥验证功能。首先需要在主服务器的主配置文件中加载密钥验证文件，然后进行设置，使得只允许带有master-slave密钥认证的DNS服务器同步数据配置文件：

[root@linuxprobe ~]# vim /etc/named.conf
 1 //
 2 // named.conf
 3 //
 4 // Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
 5 // server as a caching only nameserver (as a localhost DNS resolver only).
 6 //
 7 // See /usr/share/doc/bind*/sample/ for example named configuration files.
 8 //
 9 include "/etc/transfer.key";
 10 options {
 11 listen-on port 53 { any; };
 12 listen-on-v6 port 53 { ::1; };
 13 directory "/var/named";
 14 dump-file "/var/named/data/cache_dump.db";
 15 statistics-file "/var/named/data/named_stats.txt";
 16 memstatistics-file "/var/named/data/named_mem_stats.txt";
 17 allow-query { any; };
 18 allow-transfer { key master-slave; };
………………省略部分输出信息………………
[root@linuxprobe ~]# systemctl restart named
至此，DNS主服务器的TSIG密钥加密传输功能就已经配置完成。此时清空DNS从服务器同步目录中所有的数据配置文件，然后再次重启bind服务程序，这时就已经不能像刚才那样自动获取到数据配置文件了。

[root@linuxprobe ~]# rm -rf /var/named/slaves/*
[root@linuxprobe ~]# systemctl restart named
[root@linuxprobe ~]# ls  /var/named/slaves/
第4步：配置从服务器，使其支持密钥验证。配置DNS从服务器和主服务器的方法大致相同，都需要在bind服务程序的配置文件目录中创建密钥认证文件，并设置相应的权限，然后把该文件做一个硬链接到/etc目录中。

[root@linuxprobe ~]# cd /var/named/chroot/etc
[root@linuxprobe etc]# vim transfer.key
key "master-slave" {
algorithm hmac-md5;
secret "1XEEL3tG5DNLOw+1WHfE3Q==";
};
[root@linuxprobe etc]# chown root:named transfer.key
[root@linuxprobe etc]# chmod 640 transfer.key
[root@linuxprobe etc]# ln transfer.key /etc/transfer.key
第5步：开启并加载从服务器的密钥验证功能。这一步的操作步骤也同样是在主配置文件中加载密钥认证文件，然后按照指定格式写上主服务器的IP地址和密钥名称。注意，密钥名称等参数位置不要太靠前，大约在第43行比较合适，否则bind服务程序会因为没有加载完预设参数而报错：

[root@linuxprobe etc]# vim /etc/named.conf
 1 //
 2 // named.conf
 3 //
 4 // Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
 5 // server as a caching only nameserver (as a localhost DNS resolver only).
 6 //
 7 // See /usr/share/doc/bind*/sample/ for example named configuration files.
 8 //
 9 include "/etc/transfer.key";
 10 options {
 11 listen-on port 53 { 127.0.0.1; };
 12 listen-on-v6 port 53 { ::1; };
 13 directory "/var/named";
 14 dump-file "/var/named/data/cache_dump.db";
 15 statistics-file "/var/named/data/named_stats.txt";
 16 memstatistics-file "/var/named/data/named_mem_stats.txt";
 17 allow-query { localhost; };
 18 
 19 /* 
 20 - If you are building an AUTHORITATIVE DNS server, do NOT enable recursion.
 21 - If you are building a RECURSIVE (caching) DNS server, you need to enable 
 22 recursion. 
 23 - If your recursive DNS server has a public IP address, you MUST enable access 
 24 control to limit queries to your legitimate users. Failing to do so will
 25 cause your server to become part of large scale DNS amplification 
 26 attacks. Implementing BCP38 within your network would greatly
 27 reduce such attack surface 
 28 */
 29 recursion yes;
 30 
 31 dnssec-enable yes;
 32 dnssec-validation yes;
 33 dnssec-lookaside auto;
 34 
 35 /* Path to ISC DLV key */
 36 bindkeys-file "/etc/named.iscdlv.key";
 37 
 38 managed-keys-directory "/var/named/dynamic";
 39 
 40 pid-file "/run/named/named.pid";
 41 session-keyfile "/run/named/session.key";
 42 };
 43 server 192.168.10.10
 44 {
 45 keys { master-slave; };
 46 }; 
 47 logging {
 48 channel default_debug {
 49 file "data/named.run";
 50 severity dynamic;
 51 };
 52 };
 53 
 54 zone "." IN {
 55 type hint;
 56 file "named.ca";
 57 };
 58 
 59 include "/etc/named.rfc1912.zones";
 60 include "/etc/named.root.key";
 61
第6步：DNS从服务器同步域名区域数据。现在，两台服务器的bind服务程序都已经配置妥当，并匹配到了相同的密钥认证文件。接下来在从服务器上重启bind服务程序，可以发现又能顺利地同步到数据配置文件了。

[root@linuxprobe ~]# systemctl restart named
[root@linuxprobe ~]# ls /var/named/slaves/
 192.168.10.arpa  linuxprobe.com.zone
出现问题?大胆提问!

因读者们硬件不同或操作错误都可能导致实验配置出错，请耐心再仔细看看操作步骤吧，不要气馁~

Linux技术交流请加A群：560843(满)，B群：340829(推荐)，C群：463590（推荐），点此查看全国群。

*本群特色：通过口令验证确保每一个群员都是《Linux就该这么学》的读者，答疑更有针对性，不定期免费领取定制礼品。

13.5 部署缓存服务器
DNS缓存服务器（Caching DNS Server）是一种不负责域名数据维护的DNS服务器。简单来说，缓存服务器就是把用户经常使用到的域名与IP地址的解析记录保存在主机本地，从而提升下次解析的效率。DNS缓存服务器一般用于经常访问某些固定站点而且对这些网站的访问速度有较高要求的企业内网中，但实际的应用并不广泛。而且，缓存服务器是否可以成功解析还与指定的上级DNS服务器的允许策略有关，因此当前仅需了解即可。

第1步：配置系统的双网卡参数。前面讲到，缓存服务器一般用于企业内网，旨在降低内网用户查询DNS的时间消耗。因此，为了更加贴近真实的网络环境，实现外网查询功能，我们需要在缓存服务器中再添加一块网卡，并按照表13-4所示的信息来配置出两台Linux虚拟机系统。而且，还需要在虚拟机软件中将新添加的网卡设置为“桥接模式”，然后设置成与物理设备相同的网络参数（此处需要大家按照物理设备真实的网络参数来配置，图13-6所示为以DHCP方式获取IP地址与网关等信息，重启网络服务后的效果如图13-7所示）。

表13-4                               用于配置Linux虚拟机系统所需的参数信息

主机名称	操作系统	IP地址
缓存服务器	RHEL 7	网卡（外网）：根据物理设备的网络参数进行配置（通过DHCP或手动方式指定IP地址与网关等信息）
网卡（内网）：192.168.10.10
客户端	RHEL 7	192.168.10.20
第13章 使用Bind提供域名解析服务。第13章 使用Bind提供域名解析服务。

图13-6  以DHCP方式获取网络参数

第13章 使用Bind提供域名解析服务。第13章 使用Bind提供域名解析服务。

图13-7  查看网卡的工作状态

第2步：在bind服务程序的主配置文件中添加缓存转发参数。在大约第17行处添加一行参数“forwarders { 上级DNS服务器地址; };”，上级DNS服务器地址指的是获取数据配置文件的服务器。考虑到查询速度、稳定性、安全性等因素，刘遄老师在这里使用的是北京市公共DNS服务器的地址210.73.64.1。如果大家也使用该地址，请先测试是否可以ping通，以免导致DNS域名解析失败。

[root@linuxprobe ~]# vim /etc/named.conf
1 //
2 // named.conf
3 //
4 // Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
5 // server as a caching only nameserver (as a localhost DNS resolver only).
6 //
7 // See /usr/share/doc/bind*/sample/ for example named configuration files.
8 //
9 options {
10 listen-on port 53 { any; };
11 listen-on-v6 port 53 { ::1; };
12 directory "/var/named";
13 dump-file "/var/named/data/cache_dump.db";
14 statistics-file "/var/named/data/named_stats.txt";
15 memstatistics-file "/var/named/data/named_mem_stats.txt";
16 allow-query { any; };
17 forwarders { 210.73.64.1; };
………………省略部分输出信息………………
[root@linuxprobe ~]# systemctl restart named
第3步：重启DNS服务，验证成果。把客户端主机的DNS服务器地址参数修改为DNS缓存服务器的IP地址192.168.10.10，如图13-8所示。这样即可让客户端使用本地DNS缓存服务器提供的域名查询解析服务。

第13章 使用Bind提供域名解析服务。第13章 使用Bind提供域名解析服务。

图13-8  设置客户端主机的DNS服务器地址参数

在将客户端主机的网络参数设置妥当后重启网络服务，即可使用nslookup命令来验证实验结果（如果解析失败，请读者留意是否是上级DNS服务器选择的问题）。其中，Server参数为域名解析记录提供的服务器地址，因此可见是由本地DNS缓存服务器提供的解析内容。

[root@linuxprobe ~]# nslookup
> www.linuxprobe.com
Server: 192.168.10.10
Address: 192.168.10.10#53

Non-authoritative answer:
Name: www.linuxprobe.com
Address: 113.207.76.73
Name: www.linuxprobe.com
Address: 116.211.121.154
> 8.8.8.8
Server: 192.168.10.10
Address: 192.168.10.10#53

Non-authoritative answer:
8.8.8.8.in-addr.arpa name = google-public-dns-a.google.com.
Authoritative answers can be found from:
in-addr.arpa nameserver = f.in-addr-servers.arpa.
in-addr.arpa nameserver = b.in-addr-servers.arpa.
in-addr.arpa nameserver = a.in-addr-servers.arpa.
in-addr.arpa nameserver = e.in-addr-servers.arpa.
in-addr.arpa nameserver = d.in-addr-servers.arpa.
in-addr.arpa nameserver = c.in-addr-servers.arpa.
a.in-addr-servers.arpa internet address = 199.212.0.73
a.in-addr-servers.arpa has AAAA address 2001:500:13::73
b.in-addr-servers.arpa internet address = 199.253.183.183
b.in-addr-servers.arpa has AAAA address 2001:500:87::87
c.in-addr-servers.arpa internet address = 196.216.169.10
c.in-addr-servers.arpa has AAAA address 2001:43f8:110::10
d.in-addr-servers.arpa internet address = 200.10.60.53
d.in-addr-servers.arpa has AAAA address 2001:13c7:7010::53
e.in-addr-servers.arpa internet address = 203.119.86.101
e.in-addr-servers.arpa has AAAA address 2001:dd8:6::101
f.in-addr-servers.arpa internet address = 193.0.9.1
f.in-addr-servers.arpa has AAAA address 2001:67c:e0::1
13.6 分离解析技术
现在，喜欢看我们这本《Linux就该这么学》的海外读者越来越多，如果继续把本书配套的网站服务器（https://www.linuxprobe.com）架设在北京市的机房内，则海外读者的访问速度势必会很慢。可如果把服务器架设在美国那边的机房，也将增大国内读者的访问难度。

为了满足海内外读者的需求，外加刘遄老师不差钱，于是可以购买多台服务器并分别部署在全球各地，然后再使用DNS服务的分离解析功能，即可让位于不同地理范围内的读者通过访问相同的网址，而从不同的服务器获取到相同的数据。例如，我们可以按照表13-5所示，分别为处于北京的DNS服务器和处于美国的DNS服务器分配不同的IP地址，然后让国内读者在访问时自动匹配到北京的服务器，而让海外读者自动匹配到美国的服务器，如图13-9所示。

表13-5                                      不同主机的操作系统与IP地址情况

主机名称	操作系统	IP地址
DNS服务器	RHEL 7	北京网络：122.71.115.10
美国网络：106.185.25.10
北京用户	Windows 7	122.71.115.1
海外用户	Windows 7	106.185.25.1
第13章 使用Bind提供域名解析服务。第13章 使用Bind提供域名解析服务。

图13-9  DNS分离解析技术

为了解决海外读者访问https://www.linuxprobe.com时的速度问题，刘遄老师已经在美国机房购买并架设好了相应的网站服务器，接下来需要手动部署DNS服务器并实现分离解析功能，以便让不同地理区域的读者在访问相同的域名时，能解析出不同的IP地址。

建议大家将虚拟机还原到初始状态，并重新安装bind服务程序，以免多个实验之间相互产生冲突。

第1步：修改bind服务程序的主配置文件，把第11行的监听端口与第17行的允许查询主机修改为any。由于配置的DNS分离解析功能与DNS根服务器配置参数有冲突，所以需要把第51~54行的根域信息删除。

[root@linuxprobe ~]# vim /etc/named.conf
………………省略部分输出信息………………
 44 logging {
 45 channel default_debug {
 46 file "data/named.run";
 47 severity dynamic;
 48 };
 49 };
 50 
 51 zone "." IN {
 52 type hint;
 53 file "named.ca";
 54 };
 55 
 56 include "/etc/named.rfc1912.zones";
 57 include "/etc/named.root.key";
 58
………………省略部分输出信息………………
第2步：编辑区域配置文件。把区域配置文件中原有的数据清空，然后按照以下格式写入参数。首先使用acl参数分别定义两个变量名称（china与american），当下面需要匹配IP地址时只需写入变量名称即可，这样不仅容易阅读识别，而且也利于修改维护。这里的难点是理解view参数的作用。它的作用是通过判断用户的IP地址是中国的还是美国的，然后去分别加载不同的数据配置文件（linuxprobe.com.china或linuxprobe.com.american）。这样，当把相应的IP地址分别写入到数据配置文件后，即可实现DNS的分离解析功能。这样一来，当中国的用户访问linuxprobe.com域名时，便会按照linuxprobe.com.china数据配置文件内的IP地址找到对应的服务器。

[root@linuxprobe ~]# vim /etc/named.rfc1912.zones
1 acl "china" { 122.71.115.0/24; };
2 acl "american" { 106.185.25.0/24;};
3 view "china"{
4 match-clients { "china"; };
5 zone "linuxprobe.com" {
6 type master;
7 file "linuxprobe.com.china";
8 };
9 };
10 view "american" {
11 match-clients { "american"; };
12 zone "linuxprobe.com" {
13 type master;
14 file "linuxprobe.com.american";
15 };
16 };
第3步：建立数据配置文件。分别通过模板文件创建出两份不同名称的区域数据文件，其名称应与上面区域配置文件中的参数相对应。

[root@linuxprobe ~]# cd /var/named
[root@linuxprobe named]# cp -a named.localhost linuxprobe.com.china
[root@linuxprobe named]# cp -a named.localhost linuxprobe.com.american
[root@linuxprobe named]# vim linuxprobe.com.china
$TTL 1D	#生存周期为1天				
@	IN SOA	linuxprobe.com.	root.linuxprobe.com.	(	
#授权信息开始:	#DNS区域的地址	#域名管理员的邮箱(不要用@符号)	
0;serial	#更新序列号
1D;refresh	#更新时间
1H;retry	#重试延时
1W;expire	#失效时间
3H;)minimum	#无效解析记录的缓存时间
NS	ns.linuxprobe.com.	#域名服务器记录
ns	IN A	122.71.115.10	#地址记录(ns.linuxprobe.com.)
www	IN A	122.71.115.15	#地址记录(www.linuxprobe.com.)
[root@linuxprobe named]# vim linuxprobe.com.american
$TTL 1D	#生存周期为1天				
@	IN SOA	linuxprobe.com.	root.linuxprobe.com.	(	
#授权信息开始:	#DNS区域的地址	#域名管理员的邮箱(不要用@符号)	
0;serial	#更新序列号
1D;refresh	#更新时间
1H;retry	#重试延时
1W;expire	#失效时间
3H;)minimum	#无效解析记录的缓存时间
NS	ns.linuxprobe.com.	#域名服务器记录
ns	IN A	106.185.25.10	#地址记录(ns.linuxprobe.com.)
www	IN A	106.185.25.15	#地址记录(www.linuxprobe.com.)
第4步：重新启动named服务程序，验证结果。将客户端主机（Windows系统或Linux系统均可）的IP地址分别设置为122.71.115.1与106.185.25.1，将DNS地址分别设置为服务器主机的两个IP地址。这样，当尝试使用nslookup命令解析域名时就能清晰地看到解析结果，分别如图13-10与图13-11所示。

第13章 使用Bind提供域名解析服务。第13章 使用Bind提供域名解析服务。

图13-10   模拟中国用户的域名解析操作

第13章 使用Bind提供域名解析服务。第13章 使用Bind提供域名解析服务。

图13-11  模拟美国用户的域名解析