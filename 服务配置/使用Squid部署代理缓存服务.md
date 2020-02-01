# Squid 代理服务

16.1 代理缓存服务
16.2 配置Squid服务程序
16.3 正向代理
16.3.1 标准正向代理
16.3.2 ACL访问控制
16.3.3 透明正向代理
16.4 反向代理
16.1 代理缓存服务

Squid是Linux系统中最为流行的一款高性能代理服务软件，通常用作Web网站的前置缓存服务，能够代替用户向网站服务器请求页面数据并进行缓存。简单来说，Squid服务程序会按照收到的用户请求向网站源服务器请求页面、图片等所需的数据，并将服务器返回的数据存储在运行Squid服务程序的服务器上。当有用户再请求相同的数据时，则可以直接将存储服务器本地的数据交付给用户，这样不仅减少了用户的等待时间，还缓解了网站服务器的负载压力。

Squid服务程序具有配置简单、效率高、功能丰富等特点，它能支持HTTP、FTP、SSL等多种协议的数据缓存，可以基于访问控制列表（ACL）和访问权限列表（ARL）执行内容过滤与权限管理功能，还可以基于多种条件禁止用户访问存在威胁或不适宜的网站资源，因此可以保护企业内网的安全，提升用户的网络体验，帮助节省网络带宽。

由于缓存代理服务不但会消耗服务器较多的CPU计算性能、内存以及硬盘等硬件资源，同时还需要较大的网络带宽来保障数据的传输效率，由此会造成较大的网络带宽开销。因此国内很多IDC或CDN服务提供商会将缓存代理节点服务器放置在二三线城市以降低运营成本。

在使用Squid服务程序为用户提供缓存代理服务时，具有正向代理模式和反向代理模式之分。

所谓正向代理模式，是指让用户通过Squid服务程序获取网站页面等资源，以及基于访问控制列表（ACL）功能对用户访问网站行为进行限制，在具体的服务方式上又分为标准代理模式与透明代理模式。标准正向代理模式是把网站数据缓存到服务器本地，提高数据资源被再次访问时的效率，但是用户在上网时必须在浏览器等软件中填写代理服务器的IP地址与端口号信息，否则默认不使用代理服务。而透明正向代理模式的作用与标准正向代理模式基本相同，区别是用户不需要手动指定代理服务器的IP地址与端口号，所以这种代理服务对于用户来讲是相对透明的。

使用Squid服务程序提供正向代理服务的拓扑如图16-1所示。局域网内的主机如果想要访问外网，则必须要通过Squid服务器提供的代理才行，这样当Squid服务器接收到用户的指令后会向外部发出请求，然后将接收到的数据交还给发出指令的那个用户，从而实现了用户的代理上网需求。另外，从拓扑图中也不难看出，企业中的主机要想上网，就必须要经过公司的网关服务器，既然这是一条流量的必经之路，因此企业一般还会把Squid服务程序部署到公司服务器位置，并通过稍后讲到的ACL（访问控制列表）功能对企业内员工进行上网审计及限制。

第16章 使用Squid部署代理缓存服务。第16章 使用Squid部署代理缓存服务。

图16-1  Squid服务程序提供正向代理服务

反向代理模式是指让多台节点主机反向缓存网站数据，从而加快用户访问速度。因为一般来讲，网站中会普遍加载大量的文字、图片等静态资源，而且它们相对来说都是比较稳定的数据信息，当用户发起网站页面中这些静态资源的访问请求时，我们可以使用Squid服务程序提供的反向代理模式来进行响应。而且，如果反向代理服务器中恰巧已经有了用户要访问的静态资源，则直接将缓存的这些静态资源发送给用户，这不仅可以加快用户的网站访问速度，还在一定程度上降低了网站服务器的负载压力。

使用Squid服务程序提供反向代理服务的拓扑如图16-2所示。当外网用户尝试访问某个网站时，实际请求是被Squid服务器所处理的。反向代理服务器会将缓存好的静态资源更快地交付给外网用户，从而加快了网站页面被用户访问的速度。并且由于网站页面数据中的静态资源请求已被Squid服务器处理，因此网站服务器负责动态数据查询就可以了，也进而降低了服务器机房中网站服务器的负载压力。

图16-2  Squid服务程序提供的反向代理模式

总结来说，正向代理模式一般用于企业局域网之中，让企业用户统一地通过Squid服务访问互联网资源，这样不仅可以在一定程度上减少公网带宽的开销，而且还能对用户访问的网站内容进行监管限制，一旦内网用户访问的网站内容与禁止规则相匹配，就会自动屏蔽网站。反向代理模式一般是为大中型网站提供缓存服务的，它把网站中的静态资源保存在国内多个节点机房中，当有用户发起静态资源的访问请求时，可以就近为用户分配节点并传输资源，因此在大中型网站中得到了普遍应用。

16.2 配置Squid服务程序
Squid服务程序的配置步骤虽然十分简单，但依然需要为大家交代一下实验所需的设备以及相应的设置。首先需要准备两台虚拟机，一台用作Squid服务器，另外一台用作Squid客户端，后者无论是Windows系统还是Linux系统皆可（本实验中使用的是Windows 7操作系统）。为了能够相互通信，需要将这两台虚拟机都设置为仅主机模式（Hostonly），然后关闭其中一台虚拟机的电源，在添加一块新的网卡后开启电源，如图16-3所示。
第16章 使用Squid部署代理缓存服务。第16章 使用Squid部署代理缓存服务。

图16-3  在其中一台虚拟机中添加一块新网卡

需要注意的是，这块新添加的网卡设备必须选择为桥接模式，否则这两台虚拟机都无法访问外网。按照表16-1配置这两台虚拟机的IP地址。

表16-1                           Squid服务器和客户端的操作系统和IP地址信息

主机名称	操作系统	IP地址
Squid服务器	RHEL 7	外网卡：桥接DHCP模式
内网卡：192.168.10.10
Squid客户端	Windows 7	192.168.10.20
这样一来，我们就有了一台既能访问内网，又能访问外网的虚拟机了。一会儿需要把Squid服务程序部署在这台虚拟机上，然后让另外一台原本只能访问内网的虚拟机（即Squid客户端）通过Squid服务器进行代理上网，从而使得Squid客户端也能访问外部   网站。

另外，我们还需要检查Squid服务器是否已经可以成功访问外部网络。可以ping一个外网域名进行测试（手动按下Ctrl+c键停止）。

[root@linuxprobe ~]# ping www.linuxprobe.com
PING www.linuxprobe.com (162.159.211.33) 56(84) bytes of data.
64 bytes from 162.159.211.33: icmp_seq=1 ttl=45 time=166 ms
64 bytes from 162.159.211.33: icmp_seq=2 ttl=45 time=168 ms
64 bytes from 162.159.211.33: icmp_seq=3 ttl=45 time=167 ms
64 bytes from 162.159.211.33: icmp_seq=4 ttl=45 time=166 ms
^C
--- www.linuxprobe.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3006ms
rtt min/avg/max/mdev = 166.361/167.039/168.109/0.836 ms
当配置好Yum软件仓库并挂载好设备镜像后，就可以安装Squid服务程序了。考虑到本书中大部分服务程序都是通过Yum软件仓库安装的，读者应该对此十分熟悉，因此这里不再赘述。当然，大家也不必担心自己过于依赖Yum软件仓库来管理软件程序包，第20章会讲解如何通过源码包的方式来安装服务程序。

[root@linuxprobe ~]# yum install squid
Loaded plugins: langpacks, product-id, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
rhel | 4.1 kB 00:00 
Resolving Dependencies
--> Running transaction check
---> Package squid.x86_64 7:3.3.8-11.el7 will be installed
--> Processing Dependency: perl(DBI) for package: 7:squid-3.3.8-11.el7.x86_64
--> Processing Dependency: perl(Data::Dumper) for package: 7:squid-3.3.8-11.el7.x86_64
--> Processing Dependency: perl(Digest::MD5) for package: 7:squid-3.3.8-11.el7.x86_64
--> Processing Dependency: libecap.so.2()(64bit) for package: 7:squid-3.3.8-11.el7.x86_64
--> Running transaction check
………………省略部分输出信息………………
Installed:
 squid.x86_64 7:3.3.8-11.el7 
Dependency Installed:
 libecap.x86_64 0:0.2.0-8.el7 
 perl-Compress-Raw-Bzip2.x86_64 0:2.061-3.el7 
 perl-Compress-Raw-Zlib.x86_64 1:2.061-4.el7 
 perl-DBI.x86_64 0:1.627-4.el7 
 perl-Data-Dumper.x86_64 0:2.145-3.el7 
 perl-Digest.noarch 0:1.17-245.el7 
 perl-Digest-MD5.x86_64 0:2.52-3.el7 
 perl-IO-Compress.noarch 0:2.061-2.el7 
 perl-Net-Daemon.noarch 0:0.48-5.el7 
 perl-PlRPC.noarch 0:0.2020-14.el7 
Complete!
与之前配置过的服务程序大致类似，Squid服务程序的配置文件也是存放在/etc目录下一个以服务名称命名的目录中。表16-2罗列了一些常用的Squid服务程序配置参数，大家可以预先浏览一下。

表16-2                                 常用的Squid服务程序配置参数以及作用

参数	作用
http_port 3128	监听的端口号
cache_mem 64M	内存缓冲区的大小
cache_dir ufs /var/spool/squid 2000 16 256	硬盘缓冲区的大小
cache_effective_user squid	设置缓存的有效用户
cache_effective_group squid	设置缓存的有效用户组
dns_nameservers IP地址	一般不设置，而是用服务器默认的DNS地址
cache_access_log /var/log/squid/access.log	访问日志文件的保存路径
cache_log /var/log/squid/cache.log	缓存日志文件的保存路径
visible_hostname linuxprobe.com	设置Squid服务器的名称
16.3 正向代理
16.3.1 标准正向代理
Squid服务程序软件包在正确安装并启动后，默认就已经可以为用户提供标准正向代理模式服务了，而不再需要单独修改配置文件或者进行其他操作。接下来在运行Windows 7系统的客户端上面打开任意一款浏览器，然后单击“Internet选项”命令，如图16-4所示。

[root@linuxprobe ~]# systemctl restart squid
[root@linuxprobe ~]# systemctl enable squid
ln -s '/usr/lib/systemd/system/squid.service' '/etc/systemd/system/multi-user.target.wants/squid.service'
第16章 使用Squid部署代理缓存服务。第16章 使用Squid部署代理缓存服务。

图16-4  单击浏览器中的“Internet选项”命令

要想使用Squid服务程序提供的标准正向代理模式服务，就必须在浏览器中填写服务器的IP地址以及端口号信息。因此还需要在“连接”选项卡下单击“局域网设置”按钮（见图16-5），并按照图16-6所示填写代理服务器的信息，然后保存并退出配置向导。

第16章 使用Squid部署代理缓存服务。第16章 使用Squid部署代理缓存服务。

图16-5  在“连接”选项卡中单击“局域网设置”按钮

第16章 使用Squid部署代理缓存服务。第16章 使用Squid部署代理缓存服务。

图16-6  填写代理服务器的IP地址与端口号

现在，用户可以使用Squid服务程序提供的代理服务了。托代理服务器转发的福，网卡被设置为仅主机模式（Hostonly）的虚拟机也能奇迹般地上网浏览了，如图16-7所示。

第16章 使用Squid部署代理缓存服务。第16章 使用Squid部署代理缓存服务。

图16-7  虚拟机可以正常网络外网

如此公开而没有密码验证的代理服务终归让人觉得不放心，万一有人也来“蹭网”该怎么办呢？Squid服务程序默认使用3128、3401与4827等端口号，因此可以把默认使用的端口号修改为其他值，以便起到一定的保护作用。现在大家应该都知道，在Linux系统配置服务程序其实就是修改该服务的配置文件，因此直接在/etc目录下的Squid服务程序同名目录中找到配置文件，把http_port参数后面原有的3128修改为10000，即把Squid服务程序的代理服务端口修改成了新值。最后一定不要忘记重启服务程序。

[root@linuxprobe ~]# vim /etc/squid/squid.conf
………………省略部分输出信息………………
45 #
46 # INSERT YOUR OWN RULE(S) HERE TO ALLOW ACCESS FROM YOUR CLIENTS
47 #
48 
49 # Example rule allowing access from your local networks.
50 # Adapt localnet in the ACL section to list your (internal) IP networks
51 # from where browsing should be allowed
52 http_access allow localnet
53 http_access allow localhost
54 
55 # And finally deny all other access to this proxy
56 http_access deny all
57 
58 # Squid normally listens to port 3128
59 http_port 10000
60 
http_port 10000
………………省略部分输出信息………………
[root@linuxprobe ~]# systemctl restart squid 
[root@linuxprobe ~]# systemctl enable squid 
 ln -s '/usr/lib/systemd/system/squid.service' '/etc/systemd/system/multi-user.target.wants/squid.service'
有没有突然觉得这一幕似曾相识？在10.5.3节讲解基于端口号来部署httpd服务程序的虚拟主机功能时，我们在编辑完httpd服务程序的配置文件并重启服务程序后，被系统提示报错。尽管现在重启Squid服务程序后系统没有报错，但是用户还不能使用代理服务。SElinux安全子系统认为Squid服务程序使用3128端口号是理所当然的，因此在默认策略规则中也是允许的，但是现在Squid服务程序却尝试使用新的10000端口号，而该端口原本并不属于Squid服务程序应该使用的系统资源，因此还需要手动把新的端口号添加到Squid服务程序在SElinux域的允许列表中。

[root@linuxprobe ~]# semanage port -l | grep squid_port_t
squid_port_t                   tcp      3128, 3401, 4827
squid_port_t                   udp      3401, 4827
[root@linuxprobe ~]# semanage port -a -t squid_port_t -p tcp 10000
[root@linuxprobe ~]# semanage port -l | grep squid_port_t
squid_port_t                   tcp      10000, 3128, 3401, 4827
squid_port_t                   udp      3401, 4827
出现问题?大胆提问!

因读者们硬件不同或操作错误都可能导致实验配置出错，请耐心再仔细看看操作步骤吧，不要气馁~

Linux技术交流请加A群：560843(满)，B群：340829(推荐)，C群：463590（推荐），点此查看全国群。

*本群特色：通过口令验证确保每一个群员都是《Linux就该这么学》的读者，答疑更有针对性，不定期免费领取定制礼品。

16.3.2 ACL访问控制
在日常工作中，企业员工一般是通过公司内部的网关服务器来访问互联网，当将Squid服务程序部署为公司网络的网关服务器后，Squid服务程序的访问控制列表（ACL）功能将发挥它的用武之地。它可以根据指定的策略条件来缓存数据或限制用户的访问。比如很多公司会分时段地禁止员工逛淘宝、打网页游戏，这些禁止行为都可以通过Squid服务程序的ACL功能来实现。大家如果日后在人员流动较大的公司中从事运维工作，可以牢记本节内容，在公司网关服务器上部署的Squid服务程序中添加某些策略条件，禁止员工访问某些招聘网站或竞争对手的网站，没准还能有效降低员工的流失率。

Squid服务程序的ACL是由多个策略规则组成的，它可以根据指定的策略规则来允许或限制访问请求，而且策略规则的匹配顺序与防火墙策略规则一样都是由上至下；在一旦形成匹配之后，则立即执行相应操作并结束匹配过程。为了避免ACL将所有流量全部禁止或全部放行，起不到预期的访问控制效果，运维人员通常会在ACL的最下面写上deny all或者allow all语句，以避免安全隐患。

刘遄老师将通过下面的4个实验向大家演示Squid服务程序的ACL功能有多么强大。

实验1：只允许IP地址为192.168.10.20的客户端使用服务器上的Squid服务程序提供的代理服务，禁止其余所有的主机代理请求。

下面的配置文件依然是Squid服务程序的配置文件，但是需要留心配置参数的填写位置。如果写的太靠前，则有些Squid服务程序自身的语句都没有加载完，也会导致策略无效。当然也不用太靠后，大约在26~32行的位置就可以，而且采用分行填写的方式也便于日后的修改。

[root@linuxprobe ~]# vim /etc/squid/squid.conf
 1 #
 2 # Recommended minimum configuration:
 3 #
 4 
 5 # Example rule allowing access from your local networks.
 6 # Adapt to list your (internal) IP networks from where browsing
 7 # should be allowed
 8 acl localnet src 10.0.0.0/8 # RFC1918 possible internal network
 9 acl localnet src 172.16.0.0/12 # RFC1918 possible internal network
 10 acl localnet src 192.168.0.0/16 # RFC1918 possible internal network
 11 acl localnet src fc00::/7 # RFC 4193 local private network range
 12 acl localnet src fe80::/10 # RFC 4291 link-local (directly plugged) mac hines
 13 
 14 acl SSL_ports port 443
 15 acl Safe_ports port 80 # http
 16 acl Safe_ports port 21 # ftp
 17 acl Safe_ports port 443 # https
 18 acl Safe_ports port 70 # gopher
 19 acl Safe_ports port 210 # wais
 20 acl Safe_ports port 1025-65535 # unregistered ports
 21 acl Safe_ports port 280 # http-mgmt
 22 acl Safe_ports port 488 # gss-http
 23 acl Safe_ports port 591 # filemaker
 24 acl Safe_ports port 777 # multiling http
 25 acl CONNECT method CONNECT
 26 acl client src 192.168.10.20
 27 #
 28 # Recommended minimum Access Permission configuration:
 29 #
 30 # Deny requests to certain unsafe ports
 31 http_access allow client
 32 http_access deny all
 33 http_access deny !Safe_ports
 34
[root@linuxprobe ~]# systemctl restart squid
上面的配置参数其实很容易理解。首先定义了一个名为client的别名。这其实类似于13.6节讲解的DNS分离解析技术，当时我们分别定义了两个名为china与american的别名变量，这样当再遇到这个别名时也就意味着与之定义的IP地址了。保存配置文件后重启Squid服务程序，这时由于客户端主机的IP地址不符合我们的允许策略而被禁止使用代理服务，如图16-8所示。

图16-8  使用代理服务浏览网页失败

实验2：禁止所有客户端访问网址中包含linux关键词的网站。

Squid服务程序的这种ACL功能模式是比较粗犷暴力的，客户端访问的任何网址中只要包含了某个关键词就会被立即禁止访问，但是这并不影响访问其他网站。

[root@linuxprobe ~]# vim /etc/squid/squid.conf
 1 #
 2 # Recommended minimum configuration:
 3 #
 4 
 5 # Example rule allowing access from your local networks.
 6 # Adapt to list your (internal) IP networks from where browsing
 7 # should be allowed
 8 acl localnet src 10.0.0.0/8 # RFC1918 possible internal network
 9 acl localnet src 172.16.0.0/12 # RFC1918 possible internal network
 10 acl localnet src 192.168.0.0/16 # RFC1918 possible internal network
 11 acl localnet src fc00::/7 # RFC 4193 local private network range
 12 acl localnet src fe80::/10 # RFC 4291 link-local (directly plugged) mac hines
 13 
 14 acl SSL_ports port 443
 15 acl Safe_ports port 80 # http
 16 acl Safe_ports port 21 # ftp
 17 acl Safe_ports port 443 # https
 18 acl Safe_ports port 70 # gopher
 19 acl Safe_ports port 210 # wais
 20 acl Safe_ports port 1025-65535 # unregistered ports
 21 acl Safe_ports port 280 # http-mgmt
 22 acl Safe_ports port 488 # gss-http
 23 acl Safe_ports port 591 # filemaker
 24 acl Safe_ports port 777 # multiling http
 25 acl CONNECT method CONNECT
 26 acl deny_keyword url_regex -i linux
 27 #
 28 # Recommended minimum Access Permission configuration:
 29 #
 30 # Deny requests to certain unsafe ports
 31 http_access deny deny_keyword
 33 http_access deny !Safe_ports
 34
[root@linuxprobe ~]# systemctl restart squid
刘遄老师建议大家在进行实验之前，一定要先把前面实验中的代码清理干净，以免不同的实验之间产生冲突。在当前的实验中，我们直接定义了一个名为deny_keyword的别名，然后把所有网址带有linux关键词的网站请求统统拒绝掉。当客户端分别访问带有linux关键词和不带有linux关键词的网站时，其结果如图16-9所示。

第16章 使用Squid部署代理缓存服务。第16章 使用Squid部署代理缓存服务。

图16-9  当客户端分别访问带有linux关键词和不带linux关键词的网站时，所呈现的结果

实验3：禁止所有客户端访问某个特定的网站。

在实验2中，由于我们禁止所有客户端访问网址中包含linux关键词的网站，这将造成一大批网站被误封，从而影响同事们的正常工作。其实通过禁止客户端访问某个特定的网址，也就避免了误封的行为。下面按照如下所示的参数配置Squid服务程序并重启，然后进行测试，其测试结果如图16-10所示。

[root@linuxprobe ~]# vim /etc/squid/squid.conf
 24 acl Safe_ports port 777 # multiling http
 25 acl CONNECT method CONNECT
 26 acl deny_url url_regex http://www.linuxcool.com
 27 #
 28 # Recommended minimum Access Permission configuration:
 29 #
 30 # Deny requests to certain unsafe ports
 31 http_access deny deny_url
 33 http_access deny !Safe_ports
 34
[root@linuxprobe ~]# systemctl restart squid
第16章 使用Squid部署代理缓存服务。第16章 使用Squid部署代理缓存服务。

图16-10  无法使用代理服务访问这个特定的网站

实验4：禁止员工在企业网内部下载带有某些后缀的文件。

在企业网络中，总会有一小部分人利用企业网络的高速带宽私自下载资源（比如游戏安装文件、电影文件等），从而对其他同事的工作效率造成影响。通过禁止所有用户访问.rar或.avi等后缀文件的请求，可以防止他们继续下载资源，让他们知难而退。下面按照如下所示的参数配置Squid服务程序并重启，然后进行测试，其测试结果如图16-11所示。

如果这些员工是使用迅雷等P2P下载软件来下载资源的话，就只能使用专业级的应用防火墙来禁止了。

```shell
[root@linuxprobe ~]# vim /etc/squid/squid.conf
 24 acl Safe_ports port 777 # multiling http
 25 acl CONNECT method CONNECT
 # -i 关键词 url_regex不加i 后接网址
 # acl deny_keyword url_regex -i linux
 # http_access deny deny_keyword
 # \表示转义
 26 acl badfile urlpath_regex -i \.mp3$ \.rar$
 27 #
 28 # Recommended minimum Access Permission configuration:
 29 #
 30 # Deny requests to certain unsafe ports
 31 http_access deny badfile
 33 http_access deny !Safe_ports
 34
[root@linuxprobe ~]# systemctl restart squid
```

图16-11  无法使用代理服务下载具有指定后缀的文件

16.3.3 透明正向代理

如果是firewall只需要勾选MASQURADE这一步。

正向代理服务一般是针对企业内部的所有员工设置的，鉴于每位员工所掌握的计算机知识不尽相同，如果您所在的公司不是IT行业的公司，想教会大家如何使用代理服务也不是一件容易的事情。再者，无论是什么行业的公司，公司领导都希望能采取某些措施限制员工在公司内的上网行为，这时就需要用到透明的正向代理模式了。

“透明”二字指的是让用户在没有感知的情况下使用代理服务，这样的好处是一方面不需要用户手动配置代理服务器的信息，进而降低了代理服务的使用门槛；另一方面也可以更隐秘地监督员工的上网行为。

在透明代理模式中，用户无须在浏览器或其他软件中配置代理服务器地址、端口号等信息，而是由DHCP服务器将网络配置信息分配给客户端主机。这样只要用户打开浏览器便会自动使用代理服务了。如果大家此时并没有配置DHCP服务器，可以像如图16-12所示来手动配置客户端主机的网卡参数。

第16章 使用Squid部署代理缓存服务。第16章 使用Squid部署代理缓存服务。

图16-12  配置Windows客户端的网络信息

为了避免实验之间互相影响，更好地体验透明代理技术的效果，我们需要把客户端浏览器的代理信息删除（即图16-6的操作），然后再刷新页面，就会看到访问任何网站都失败了，如图16-13所示。第16章 使用Squid部署代理缓存服务。第16章 使用Squid部署代理缓存服务。

图16-13  停止使用代理服务后无法成功访问网站

有些时候会因为Windows系统的缓存原因导致依然能看到网页内容，这时可以换个网站尝试一下访问效果。

 

既然要让用户在无需过多配置系统的情况下就能使用代理服务，作为运维人员就必须提前将网络配置信息与数据转发功能配置好。前面已经配置好的网络参数，接下来要使用8.3.2节介绍的SNAT技术完成数据的转发，让客户端主机将数据交给Squid代理服务器，再由后者转发到外网中。简单来说，就是让Squid服务器作为一个中间人，实现内网客户端主机与外部网络之间的数据传输。

由于当前还没有部署SNAT功能，因此当前内网中的客户端主机是不能访问外网的：

C:\Users\linuxprobe>ping www.linuxprobe.com
Ping 请求找不到主机 www.linuxprobe.com。请检查该名称，然后重试。
第8章已经介绍了iptables与firewalld防火墙理论知识以及策略规则的配置方法，大家可以任选其中一款完成接下来的实验。刘遄老师觉得firewalld防火墙实在太简单了，因此决定使用纯命令行的iptables防火墙管理工具来演示部署方法。

要想让内网中的客户端主机能够访问外网，客户端主机首先要能获取到DNS地址解析服务的数据，这样才能在互联网中找到对应网站的IP地址。下面通过iptables命令实现DNS地址解析服务53端口的数据转发功能，并且允许Squid服务器转发IPv4数据包。sysctl -p命令的作用是让转发参数立即生效：

```shell
[root@linuxprobe ~]# iptables -F
# -t nat 表示配置的是SNAT
# -A POSTROUTING路由后转发
# -p udp 协议udp
# -o 从对外网卡转发出去
# -j MASQUERADE每次换网卡后，自动找到最新网卡并设置它
[root@linuxprobe ~]# iptables -t nat -A POSTROUTING -p udp --dport 53 -o eno33554968 -j MASQUERADE
# 支持ipv4转发
[root@linuxprobe ~]# echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
# 当前生效
[root@linuxprobe ~]# sysctl -p 
net.ipv4.ip_forward = 1
```

现在回到客户端主机，再次ping某个外网地址。此时可以发现，虽然不能连通网站，但是此时已经能够获取到外网DNS服务的域名解析数据。这个步骤非常重要，为接下来的SNAT技术打下了扎实的基础。

C:\Users\linuxprobe>ping www.linuxprobe.com
正在 Ping www.linuxprobe.com [116.31.127.233] 具有 32 字节的数据:
请求超时。
请求超时。
请求超时。
请求超时。
116.31.127.233 的 Ping 统计信息:
    数据包: 已发送 = 4，已接收 = 0，丢失 = 4 (100% 丢失)，
与配置DNS和SNAT技术转发相比，Squid服务程序透明代理模式的配置过程就十分简单了，只需要在主配置文件中服务器端口号后面追加上transparent单词（意思为“透明的”），然后把第62行的井号（#）注释符删除，设置缓存的保存路径就可以了。保存主配置文件并退出后再使用squid -k parse命令检查主配置文件是否有错误，以及使用squid -z命令对Squid服务程序的透明代理技术进行初始化。

```shell
[root@linuxprobe ~]# vim /etc/squid/squid.conf
………………省略部分输出信息………………
58 # Squid normally listens to port 3128
# 开启透明代理模式
59 http_port 3128 transparent
60
61 # Uncomment and adjust the following to add a disk cache directory.
# 缓存目录技术，提高二次访问速度
62 cache_dir ufs /var/spool/squid 100 16 256
63 
………………省略部分输出信息………………
# 检查是否出错
[root@linuxprobe ~]# squid -k parse
2017/04/13 06:40:44| Startup: Initializing Authentication Schemes ...
2017/04/13 06:40:44| Startup: Initialized Authentication Scheme 'basic'
2017/04/13 06:40:44| Startup: Initialized Authentication Scheme 'digest'
2017/04/13 06:40:44| Startup: Initialized Authentication Scheme 'negotiate'
2017/04/13 06:40:44| Startup: Initialized Authentication Scheme 'ntlm'
2017/04/13 06:40:44| Startup: Initialized Authentication.
………………省略部分输出信息………………
# 生成默认共享目录
[root@linuxprobe ~]# squid -z
2017/04/13 06:41:26 kid1| Creating missing swap directories
2017/04/13 06:41:26 kid1| /var/spool/squid exists
2017/04/13 06:41:26 kid1| Making directories in /var/spool/squid/00
2017/04/13 06:41:26 kid1| Making directories in /var/spool/squid/01
2017/04/13 06:41:26 kid1| Making directories in /var/spool/squid/02
2017/04/13 06:41:26 kid1| Making directories in /var/spool/squid/03
2017/04/13 06:41:26 kid1| Making directories in /var/spool/squid/04
2017/04/13 06:41:26 kid1| Making directories in /var/spool/squid/05
2017/04/13 06:41:26 kid1| Making directories in /var/spool/squid/06
2017/04/13 06:41:26 kid1| Making directories in /var/spool/squid/07
2017/04/13 06:41:26 kid1| Making directories in /var/spool/squid/08
2017/04/13 06:41:26 kid1| Making directories in /var/spool/squid/09
2017/04/13 06:41:26 kid1| Making directories in /var/spool/squid/0A
2017/04/13 06:41:26 kid1| Making directories in /var/spool/squid/0B
2017/04/13 06:41:26 kid1| Making directories in /var/spool/squid/0C
2017/04/13 06:41:26 kid1| Making directories in /var/spool/squid/0D
2017/04/13 06:41:26 kid1| Making directories in /var/spool/squid/0E
2017/04/13 06:41:26 kid1| Making directories in /var/spool/squid/0F
[root@linuxprobe ~]# systemctl restart squid
```

在配置妥当并重启Squid服务程序且系统没有提示报错信息后，接下来就可以完成SNAT数据转发功能了。它的原理其实很简单，就是使用iptables防火墙管理命令把所有客户端主机对网站80端口的请求转发至Squid服务器本地的3128端口上。SNAT数据转发功能的具体配置参数如下。

[root@linuxprobe ~]# iptables -t nat -A PREROUTING  -p tcp -m tcp --dport 80 -j REDIRECT --to-ports 3128
[root@linuxprobe ~]# iptables -t nat -A POSTROUTING -s 192.168.10.0/24 -o eno33554968 -j SNAT --to 您的桥接网卡IP地址
[root@linuxprobe ~]# service iptables save
iptables: Saving firewall rules to /etc/sysconfig/iptables:[ OK ]
这时客户端主机再刷新一下浏览器，就又能访问网络了，如图16-14所示。

图16-14  客户端主机借助于透明代理技术成功访问网络

现在肯定有读者在想，如果开启了SNAT功能，数据不就直接被转发到外网了么？内网中的客户端主机是否还依然使用Squid服务程序提供的代理服务呢？其实，只要仔细看一下iptables防火墙命令就会发现，刘遄老师刚才并不是单纯地开启了SNAT功能，而是通过把客户端主机访问外网80端口的请求转发到Squid服务器的3128端口号上，从而还是强制客户端主机必须通过Squid服务程序来上网。为了验证这个说法，我们编辑Squid服务程序的配置文件，单独禁止本书的配套站点（https://www.linuxprobe.com/），然后再次刷新客户端主机的浏览器，发现网页又被禁止显示了，如图16-15所示。

图16-15  客户端主机再次无法访问网络

16.4 反向代理
网站页面是由静态资源和动态资源一起组成的，其中静态资源包括网站架构CSS文件、大量的图片、视频等数据，这些数据相对于动态资源来说更加稳定，一般不会经常发生改变。但是，随着建站技术的更新换代，外加人们不断提升的审美能力，这些静态资源占据的网站空间越来越多。如果能够把这些静态资源从网站页面中抽离出去，然后在全国各地部署静态资源的缓存节点，这样不仅可以提升用户访问网站的速度，而且网站源服务器也会因为这些缓存节点的存在而降低负载。

反向代理是Squid服务程序的一种重要模式，其原理是把一部分原本向网站源服务器发起的用户请求交给Squid服务器缓存节点来处理。但是这种技术的弊端也很明显，如果有心怀不轨之徒将自己的域名和服务器反向代理到某个知名的网站上面，从理论上来讲，当用户访问到这个域名时，也会看到与那个知名网站一样的内容（有些诈骗网站就是这样骗取用户信任的）。因此，当前许多网站都默认禁止了反向代理功能。开启了CDN（内容分发网络）服务的网站也可以避免这种窃取行为。如果访问开启了防护功能的网站，一般会看到如图16-16所示的报错信息。

第16章 使用Squid部署代理缓存服务。第16章 使用Squid部署代理缓存服务。

图16-16  访问网站时提示报错信息

刘遄老师为了实验需要而临时关闭了本书配套站点的CDN服务及防护插件，请大家尽量选择用自己的网站或博客进行该实验操作，避免影响到其他网站的正常运转，给他人造成麻烦。

使用Squid服务程序来配置反向代理服务非常简单。首先找到一个网站源服务器的IP地址，然后编辑Squid服务程序的主配置文件，把端口号3128修改为网站源服务器的地址和端口号，此时正向解析服务会被暂停（它不能与反向代理服务同时使用）。然后按照下面的参数形式写入需要反向代理的网站源服务器的IP地址信息，保存退出后重启Squid服务程序。正常网站使用反向代理服务的效果如图16-17所示。

```shell
[root@linuxprobe ~]# vim /etc/squid/squid.conf
………………省略部分输出信息………………
57 
58 # Squid normally listens to port 3128
# vhost 虚拟主机
59 http_port 您的桥接网卡IP地址:80 vhost
60 cache_peer 网站源服务器IP地址 parent 80 0 originserver
61 
………………省略部分输出信息………………
[root@linuxprobe ~]# systemctl restart squid
```

图16-17  使用反向代理模式访问网站

本章节的复习作业(答案就在问题的下一行哦，用鼠标选中即可看到的~)

1．简述Squid服务程序提供的正向代理服务的主要作用。

答：实现代理上网、隐藏用户的真实访问信息以及对控制用户访问网站行为的访问控制列表（ACL）进行限制。

2．简述Squid服务程序提供的反向代理服务的主要作用。

答：加快用户访问网站的速度，降低网站源服务器的负载压力。

3．Squid服务程序能够提供的代理模式有哪些？

答：正向代理模式与反向代理模式，其中正向代理模式又分为标准正向代理模式与透明正向代理模式。

4．标准正向代理模式与透明正向代理模式的区别是什么？

答：区别在于用户是否需要配置代理服务器的信息。若使用透明代理模式，则用户感知不到代理服务的存在。

5．使用Squid服务程序提供的标准正向代理模式时，需要在浏览器中配置哪些信息？

答：需要填写Squid服务器的IP地址及端口号信息。

6．若需要通过ACL功能限制用户不能使用代理服务访问指定网站，参数该怎么写？

答：以本书的配套学习站点（www.linuxprobe.com）为例，可使用参数“acl deny_url url_regex https://www.linuxprobe.com”和“http_access deny deny_url”来禁止用户访问这个指定的网站。

7．若让客户端主机使用透明正向代理模式，则需要用DHCP服务器为客户端主机分配什么信息？

答：需要为客户端主机分配IP地址、子网掩码、网关地址以及外部DNS服务