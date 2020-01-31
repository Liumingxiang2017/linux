# 使用DHCP动态管理主机

## 动态主机地址管理协议

动态主机配置协议（DHCP）是一种基于UDP协议且仅限于在局域网内部使用的网络协议，主要用于大型的局域网环境或者存在较多移动办公设备的局域网环境中，其主要用途是为局域网内部的设备或网络供应商自动分配IP地址等参数。

简单来说，DHCP协议就是让局域网中的主机自动获得网络参数的服务。在图14-1所示的拓扑图中存在多台主机，如果手动配置每台主机的网络参数会相当麻烦，日后维护起来也让人头大。而且当机房内的主机数量进一步增加时（比如有100台，甚至1000台），这个手动配置以及维护工作的工作量足以让运维人员崩溃。借助于DHCP协议，不仅可以为主机自动分配网络参数，还可以确保主机使用的IP地址是唯一的，更重要的是，还能为特定主机分配固定的IP地址。

图14-1  DHCP协议的拓扑示意图

DHCP协议的应用十分广泛，无论是服务器机房还是家庭、机场、咖啡馆，都会见到它的身影。比如，本书的某位读者开了一家咖啡厅，在为顾客提供咖啡的同时，还为顾客免费提供无线上网服务。这样一来，顾客就可以一边惬意地喝着咖啡，一边连着无线网络刷朋友圈了。但是，作为咖啡厅老板的您，肯定不希望（也没有时间）为每一位造访的顾客手动设置IP地址、子网掩码、网关地址等信息。另外，考虑到咖啡馆使用的内网网段一般为192.168.10.0/24（C类私有地址），最多能容纳的主机数为200多台。而咖啡厅一天的客流量肯定不止200人。如果采用手动方式为他们分配IP地址，则当他们在离开咖啡厅时并不会自动释放这个IP地址，这就可能出现IP地址不够用的情况。这一方面会造成IP地址的浪费，另外一方面也增加的IP地址的管理成本。而使用DHCP协议，这一切都迎刃而解—老板只需安心服务好顾客，为其提供美味的咖啡；顾客通过运行DHCP协议的服务器自动获得上网所需的IP地址，等离开咖啡厅时IP地址将被DHCP服务器收回，以备其他顾客使用。

既然确定在今后的生产环境中肯定离不开DHCP了，那么也就有必要好好地熟悉一下DHCP涉及的常见术语了。

### DHCP涉及的术语

- 作用域
  - 一个完整的IP地址段，DHCP协议根据作用域来管理网络的分布、分配IP地址及其他配置参数。
  - 简单来说就是声明定义一个大网段。

- 超级作用域
  - 用于管理处于同一个物理网络中的多个逻辑子网段。超级作用域中包含了可以统一管理的作用域列表。

- 排除范围
  - 把作用域中的某些IP地址排除，确保这些IP地址不会分配给DHCP客户端。
  - 作用域-地址池

- 地址池
  - 在定义了DHCP的作用域并应用了排除范围后，剩余的用来动态分配给DHCP客户端的IP地址范围。
  - 真正为用户去分配的地址
  - 地址池要小于等于作用域

- 租约
  - DHCP客户端能够使用动态分配的IP地址的时间。
  - 默认时间，之后就等待被回收
  - 最大时间，到达即被回收

- 预约
  - 保证网络中的特定设备总是获取到相同的IP地址。
  - 固定IP地址

## 部署dhcpd服务程序

dhcpd是Linux系统中用于提供DHCP协议的服务程序。尽管DHCP协议的功能十分强大，但是dhcpd服务程序的配置步骤却十分简单，这也在很大程度上降低了在Linux中实现动态主机管理服务的门槛。

在确认Yum软件仓库配置妥当之后，安装dhcpd服务程序：

```shell
[root@linuxprobe ~]# yum install dhcp
Loaded plugins: langpacks, product-id, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
rhel | 4.1 kB 00:00 
Resolving Dependencies
--> Running transaction check
---> Package dhcp.x86_64 12:4.2.5-27.el7 will be installed
--> Finished Dependency Resolution
Dependencies Resolved
================================================================================
 Package Arch Version Repository Size
================================================================================
Installing:
 dhcp x86_64 12:4.2.5-27.el7 rhel 506 k
Transaction Summary
================================================================================
Install 1 Package
Total download size: 506 k
Installed size: 1.4 M
Is this ok [y/d/N]: y
Downloading packages:
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
 Installing : 12:dhcp-4.2.5-27.el7.x86_64 1/1 
 Verifying : 12:dhcp-4.2.5-27.el7.x86_64 1/1 
Installed:
 dhcp.x86_64 12:4.2.5-27.el7 
Complete!
```

查看dhcpd服务程序的配置文件内容。

```shell
[root@linuxprobe ~]# cat /etc/dhcp/dhcpd.conf
# DHCP Server Configuration file.
# see /usr/share/doc/dhcp*/dhcpd.conf.example
# see dhcpd.conf(5) man page
```

是的，您没有看错！dhcp的服务程序的配置文件中只有3行注释语句，这意味着我们需要自行编写这个文件。如果读者不知道怎么编写，可以看一下配置文件中第2行的参考示例文件，其组成架构如图14-2所示。

图14-2  dhcpd服务程序配置文件的架构

一个标准的配置文件应该包括全局配置参数、子网网段声明、地址配置选项以及地址配置参数。其中，全局配置参数用于定义dhcpd服务程序的整体运行参数；子网网段声明用于配置整个子网段的地址属性。

考虑到dhcpd服务程序配置文件的可用参数比较多，刘遄老师挑选了最常用的参数（见表14-1），并逐一进行了简单介绍，以便为接下来的实验打好基础。

表14-1  dhcpd服务程序配置文件中使用的常见参数以及作用

参数	作用
ddns-update-style 类型	定义DNS服务动态更新的类型，类型包括：
none（不支持动态更新）、interim（互动更新模式）与ad-hoc（特殊更新模式）
allow/ignore client-updates	允许/忽略客户端更新DNS记录
default-lease-time 21600	默认超时时间
max-lease-time 43200	最大超时时间
option domain-name-servers 8.8.8.8	定义DNS服务器地址
option domain-name "domain.org"	定义DNS域名
range	定义用于分配的IP地址池
option subnet-mask	定义客户端的子网掩码
option routers	定义客户端的网关地址
broadcast-address 广播地址	定义客户端的广播地址
ntp-server IP地址	定义客户端的网络时间服务器（NTP）
nis-servers IP地址	定义客户端的NIS域服务器的地址
hardware 硬件类型 MAC地址	指定网卡接口的类型与MAC地址
server-name 主机名	向DHCP客户端通知DHCP服务器的主机名
fixed-address IP地址	将某个固定的IP地址分配给指定主机
time-offset 偏移差	指定客户端与格林尼治时间的偏移差

## 自动管理IP地址

DHCP协议的设计初衷是为了更高效地集中管理局域网内的IP地址资源。DHCP服务器会自动把IP地址、子网掩码、网关、DNS地址等网络信息分配给有需要的客户端，而且当客户端的租约时间到期后还可以自动回收所分配的IP地址，以便交给新加入的客户端。

为了让实验更有挑战性，刘遄老师来模拟一个真实生产环境的需求：

“机房运营部门：明天会有100名学员自带笔记本电脑来我司培训学习，请保证他们能够使用机房的本地DHCP服务器自动获取IP地址并正常上网”。

机房所用的网络地址及参数信息如表14-2所示。

表14-2   机房所用的网络地址以及参数信息

参数名称	值
默认租约时间	21600秒
最大租约时间	43200秒
IP地址范围	192.168.10.50~192.168.10.150
子网掩码	255.255.255.0
网关地址	192.168.10.1
DNS服务器地址	192.168.10.1
搜索域	linuxprobe.com
在了解了真实需求以及机房网络中的配置参数之后，我们按照表14-3来配置DHCP服务器以及客户端。

表14-3  DHCP服务器以及客户端的配置信息

主机类型	操作系统	IP地址
DHCP服务器	RHEL 7	192.168.10.1
DHCP客户机	RHEL 7	DHCP自动获取地址
前文讲到，作用域一般是个完整的IP地址段，而地址池中的IP地址才是真正供客户端使用的，因此地址池应该小于或等于作用域的IP地址范围。另外，由于VMware Workstation虚拟机软件自带DHCP服务，为了避免与自己配置的dhcpd服务程序产生冲突，应该先按照图14-3和图14-4所示将虚拟机软件自带的DHCP功能关闭。

图14-3  单击虚拟机软件的“虚拟网络编辑器”菜单

图14-4  关闭虚拟机自带的DHCP功能

可随意开启几台客户端，准备进行验证。但是一定要注意，DHCP客户端与服务器需要处于同一种网络模式—仅主机模式（Hostonly），否则就会产生物理隔离，从而无法获取IP地址。刘遄老师建议开启1～3台客户端虚拟机验证一下效果就好，以免物理主机的CPU和内存的负载太高。

在确认DHCP服务器的IP地址等网络信息配置妥当后就可以配置dhcpd服务程序了。请注意，在配置dhcpd服务程序时，配置文件中的每行参数后面都需要以分号（;）结尾，这是规定。另外，dhcpd服务程序配置文件内的参数都十分重要，因此刘遄老师在表14-4中罗列出了每一行参数，并对其用途进行了简单介绍。

```shell
[root@linuxprobe ~]# vim /etc/dhcp/dhcpd.conf
# 动态DNS更新协议 功能不需要
ddns-update-style none;
# 忽略掉客户端更新
ignore client-updates;
# 定义作用域网段
subnet 192.168.10.0 netmask 255.255.255.0 {
range 192.168.10.50 192.168.10.150;
option subnet-mask 255.255.255.0;
# 为用户分配的网关地址
option routers 192.168.10.1;
option domain-name "linuxprobe.com";
# dns地址
option domain-name-servers 192.168.10.1;
# 默认租约时间
default-lease-time 21600;
# 最大租约时间
max-lease-time 43200;
}
```

表14-4    dhcpd服务程序配置文件中使用的参数以及作用

参数	作用
ddns-update-style none;	设置DNS服务不自动进行动态更新
ignore client-updates;	忽略客户端更新DNS记录
subnet 192.168.10.0 netmask 255.255.255.0 {	作用域为192.168.10.0/24网段
range 192.168.10.50 192.168.10.150;	IP地址池为192.168.10.50-150（约100个IP地址）
option subnet-mask 255.255.255.0;	定义客户端默认的子网掩码
option routers 192.168.10.1;	定义客户端的网关地址
option domain-name "linuxprobe.com";	定义默认的搜索域
option domain-name-servers 192.168.10.1;	定义客户端的DNS地址
default-lease-time 21600;	定义默认租约时间（单位：秒）
max-lease-time 43200;	定义最大预约时间（单位：秒）
}	结束符

在红帽认证考试以及生产环境中，都需要把配置过的dhcpd服务加入到开机启动项中，以确保当服务器下次开机后dhcpd服务依然能自动启动，并顺利地为客户端分配IP地址等信息。刘遄老师真心建议大家能养成“配置好服务程序，顺手加入开机启动项”的好习惯：

```shell
[root@linuxprobe ~]# systemctl start dhcpd
[root@linuxprobe ~]# systemctl enable dhcpd
 ln -s '/usr/lib/systemd/system/dhcpd.service' '/etc/systemd/system/multi-user.target.wants/dhcpd.service'
```

把dhcpd服务程序配置妥当之后就可以开启客户端来检验IP分配效果了。重启客户端的网卡服务后即可看到自动分配到的IP地址，如图14-5所示。

图14-5  客户端自动获取的IP地址

如果有兴趣，大家还可以再开启一台运行Windows系统的客户端进行尝试，其效果都是一样的。

## 分配固定IP地址

在DHCP协议中有个术语是“预约”，它用来确保局域网中特定的设备总是获取到固定的IP地址。换句话说，就是dhcpd服务程序会把某个IP地址私藏下来，只将其用于相匹配的特定设备。

要想把某个IP地址与某台主机进行绑定，就需要用到这台主机的MAC地址。MAC地址是网卡上面的一串独立的标识符，具备唯一性，因此不会存在冲突的情况，如图14-6所示。
第14章 使用DHCP动态管理主机地址。第14章 使用DHCP动态管理主机地址。

图14-6  查看运行Linux系统的主机MAC地址

在Linux系统或Windows系统中，都可以通过查看网卡的状态来获知主机的MAC地址。在dhcpd服务程序的配置文件中，按照如下格式将IP地址与MAC地址进行绑定。

host 主机名称 {				
hardware	ethernet	该主机的MAC地址;	
fixed-address	欲指定的IP地址;		
}				
如果不方便查看主机的MAC地址，该怎么办呢？比如，要给老板使用的主机绑定IP地址，总不能随便就去查看老板的主机信息吧。针对这种情况，刘遄老师告诉大家一个很好的办法。我们首先启动dhcpd服务程序，为老板的主机分配一个IP地址，这样就会在DHCP服务器本地的日志文件中保存这次的IP地址分配记录。然后查看日志文件，就可以获悉主机的MAC地址了（即下面加粗的内容）。

```shell
[root@linuxprobe ~]# tail -f /var/log/messages 
Mar 30 05:33:17 localhost dhcpd: Copyright 2004-2013 Internet Systems Consortium.
Mar 30 05:33:17 localhost dhcpd: All rights reserved.
Mar 30 05:33:17 localhost dhcpd: For info, please visit https://www.isc.org/software/dhcp/
Mar 30 05:33:17 localhost dhcpd: Not searching LDAP since ldap-server, ldap-port and ldap-base-dn were not specified in the config file
Mar 30 05:33:17 localhost dhcpd: Wrote 0 leases to leases file.
Mar 30 05:33:17 localhost dhcpd: Listening on LPF/eno16777728/00:0c:29:c4:a4:09/192.168.10.0/24
Mar 30 05:33:17 localhost dhcpd: Sending on LPF/eno16777728/00:0c:29:c4:a4:09/192.168.10.0/24
Mar 30 05:33:17 localhost dhcpd: Sending on Socket/fallback/fallback-net
Mar 30 05:33:26 localhost dhcpd: DHCPDISCOVER from 00:0c:29:27:c6:12 via eno16777728
Mar 30 05:33:27 localhost dhcpd: DHCPOFFER on 192.168.10.50 to 00:0c:29:27:c6:12 (WIN-APSS1EANKLR) via eno16777728
Mar 30 05:33:29 localhost dhcpd: DHCPDISCOVER from 00:0c:29:27:c6:12 (WIN-APSS1EANKLR) via eno16777728
Mar 30 05:33:29 localhost dhcpd: DHCPOFFER on 192.168.10.50 to 00:0c:29:27:c6:12 (WIN-APSS1EANKLR) via eno16777728
Mar 30 05:33:29 localhost dhcpd: DHCPREQUEST for 192.168.10.50 (192.168.10.10) from 00:0c:29:27:c6:12 (WIN-APSS1EANKLR) via eno16777728
Mar 30 05:33:29 localhost dhcpd: DHCPACK on 192.168.10.50 to 00:0c:29:27:c6:12 (WIN-APSS1EANKLR) via eno16777728
```

之前我在线下讲课时，讲完DHCP服务后总是看到有些学员在挠头。起初我很不理解，毕竟dhcpd服务程序是Linux系统中一个很简单的实验，总共就那么十几行的配置参数还能写错？后来发现了原因—有些学员是以Windows系统为对象做的IP与MAC地址的绑定实验。而在Windows系统中看到的MAC地址，其格式类似于00-0c-29-27-c6-12，间隔符为减号（-）。但是在Linux系统中，MAC地址的间隔符则变成了冒号（:）。

```shell
[root@linuxprobe ~]# vim /etc/dhcp/dhcpd.conf 
ddns-update-style none;
ignore client-updates;
subnet 192.168.10.0 netmask 255.255.255.0 {
range 192.168.10.50 192.168.10.150;
option subnet-mask 255.255.255.0;
option routers 192.168.10.1;
option domain-name "linuxprobe.com";
option domain-name-servers 192.168.10.1;
default-lease-time 21600;
max-lease-time 43200;
host linuxprobe {
hardware ethernet 00:0c:29:27:c6:12;
fixed-address 192.168.10.88;
}
}
```

确认参数填写正确后就可以保存退出配置文件，然后就可以重启dhcpd服务程序了。

```shell
[root@linuxprobe ~]# systemctl restart dhcpd
```

需要说明的是，如果您刚刚为这台主机分配了IP地址，则它的IP地址租约时间还没有到期，因此不会立即换成新绑定的IP地址。要想立即查看绑定效果，则需要重启一下客户端的网络服务，如图14-7所示。

图14-7  重启客户端的网络服务，查看绑定效果

本章节的复习作业(答案就在问题的下一行哦，用鼠标选中即可看到的~)

1．简述DHCP协议的主要用途。

答：为局域网内部的设备或网络供应商自动分配IP地址等参数。

2．DHCP协议能够为客户端分配什么网卡资源？

答：可为客户端分配IP地址、子网掩码、网关地址以及DNS地址等信息。

3．真正供用户使用的IP地址范围是作用域还是地址池？

答：地址池，因为作用域内还会包含要排除掉的IP地址。

4．简述DHCP协议中“租约”的作用。

答：租约分为默认租约时间和最大租约时间，用于在租约时间到期后自动回收主机的IP地址，以免造成IP地址的浪费。

5．把IP地址与主机的什么信息绑定，就可以保证该主机一直获取到固定的IP地址？

答：主机网卡的MAC地址。