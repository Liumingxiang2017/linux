# 使用PXE和Kickstart无人值守安装服务

本章目录结构 [收起]

19.1 无人值守系统
19.2 部署相关服务程序
19.2.1 配置DHCP服务程序
19.2.2 配置TFTP服务程序
19.2.3 配置SYSLinux服务程序
19.2.4 配置VSFtpd服务程序
19.2.5 创建KickStart应答文件
19.3 自动部署客户机

DHCP: 自动分配IP
TFTP：驱动 引导文件
PXE：一种帮助文件，用于获取驱动和引导文件
vsftpd：传输光盘镜像
Kickstart： 应答文件/var/ftp/pub/ks.cfg 

PXE+Kickstart不支持windows

Cobbler（补鞋匠）是一个开源的系统部署软件，基于PXE的二次封装，并集成了DNS,DHCP,软件包更新，电源管理以及配置管理编排等功能；实现快速网络安装操作系统。简单易用且可以用于安装windows。

19.1 无人值守系统
本书在第1章讲解了使用光盘镜像来安装Linux系统的方法，坦白讲，该方法适用于只安装少量Linux系统的情况。如果生产环境中有数百台服务器都需要安装系统，这种方式就不合时宜了。这时，我们就需要使用PXE + TFTP +FTP + DHCP + Kickstart服务搭建出一个无人值守安装系统。这种无人值守安装系统可以自动地为数十台服务器安装系统，这一方面将运维人员从重复性的工作中解救出来，也大大提升了系统安装的效率。

无人值守安装系统的工作流程如图19-1所示。

图19-1  无人值守安装系统的工作流程

PXE（Preboot eXecute Environment，预启动执行环境）是由Intel公司开发的技术，可以让计算机通过网络来启动操作系统（前提是计算机上安装的网卡支持PXE技术），主要用于在无人值守安装系统中引导客户端主机安装Linux操作系统。Kickstart是一种无人值守的安装方式，其工作原理是预先把原本需要运维人员手工填写的参数保存成一个ks.cfg文件，当安装过程中需要填写参数时则自动匹配Kickstart生成的文件。所以只要Kickstart文件包含了安装过程中需要人工填写的所有参数，那么从理论上来讲完全不需要运维人员的干预，就可以自动完成安装工作。TFTP、FTP以及DHCP服务程序的配置与部署已经在第11章和第14章进行了详细讲解，这里不再赘述。

由于当前的客户端主机并没有完整的操作系统，也就不能完成FTP协议的验证了，所以需要使用TFTP协议帮助客户端获取引导及驱动文件。vsftpd服务程序用于将完整的系统安装镜像通过网络传输给客户端。当然，只要能将系统安装镜像成功传输给客户端即可，因此也可以使用httpd来替代vsftpd服务程序。

19.2 部署相关服务程序
19.2.1 配置DHCP服务程序
DHCP服务程序用于为客户端主机分配可用的IP地址，而且这是服务器与客户端主机进行文件传输的基础，因此我们先行配置DHCP服务程序。首先按照表19-1为无人值守系统设置IP地址，然后按照图19-2和图19-3在虚拟机的虚拟网络编辑器中关闭自身的DHCP服务。

表19-1                                          无人值守系统与客户端的设置

主机名称	操作系统	IP地址
无人值守系统	RHEL 7	192.168.10.10
客户端	未安装操作系统	-
第19章 使用PXE+Kickstart无人值守安装服务。第19章 使用PXE+Kickstart无人值守安装服务。

图19-2  打开虚拟机的虚拟网络编辑器

图19-3  关闭虚拟机自带的DHCP服务

当挂载好光盘镜像并把Yum仓库文件配置妥当后，就可以安装DHCP服务程序软件包了。

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

第14章已经详细讲解了DHCP服务程序的配置以及部署方法，相信各位读者对相关的配置参数还有一些印象。但是，我们在这里使用的配置文件与第14章中的配置文件有两个主要区别：允许了BOOTP引导程序协议，旨在让局域网内暂时没有操作系统的主机也能获取静态IP地址；在配置文件的最下面加载了引导驱动文件pxelinux.0（这个文件会在下面的步骤中创建），其目的是让客户端主机获取到IP地址后主动获取引导驱动文件，自行进入下一步的安装过程。

```shell
[root@linuxprobe ~]# vim /etc/dhcp/dhcpd.conf
# 允许booting（能够开机分配IP地址的协议）
allow booting;
allow bootp;
# 动态DDNS更新 内部（这句没用）
ddns-update-style interim;
ignore client-updates;
subnet 192.168.10.0 netmask 255.255.255.0 {
        option subnet-mask      255.255.255.0;
        #dns也不需要，只是说有这个功能
        option domain-name-servers  192.168.10.10; 
        # 动态bootp 支持没有系统分配IP地址（下例支持100台）
        range dynamic-bootp 192.168.10.100 192.168.10.200;
        # 默认租约时间
        default-lease-time      21600;
        max-lease-time          43200;
        # 网关地址，也不需要，但有这个功能
        next-server             192.168.10.10;
        # 当分配好地址网卡信息以后自动加载该文件
        filename                "pxelinux.0";
}
```

在确认DHCP服务程序的参数都填写正确后，重新启动该服务程序，并将其添加到开机启动项中。这样在设备下一次重启之后，在无须人工干预的情况下，自动为客户端主机安装系统。

[root@linuxprobe ~]# systemctl restart dhcpd
[root@linuxprobe ~]# systemctl enable dhcpd
ln -s '/usr/lib/systemd/system/dhcpd.service' '/etc/systemd/system/multi-user.target.wants/dhcpd.service'
19.2.2 配置TFTP服务程序
我们曾经在第11章中学习过vsftpd服务与TFTP服务。vsftpd是一款功能丰富的文件传输服务程序，允许用户以匿名开放模式、本地用户模式、虚拟用户模式来进行访问认证。但是，当前的客户端主机还没有安装操作系统，该如何进行登录认证呢？而TFTP作为一种基于UDP协议的简单文件传输协议，不需要进行用户认证即可获取到所需的文件资源。因此接下来配置TFTP服务程序，为客户端主机提供引导及驱动文件。当客户端主机有了基本的驱动程序之后，再通过vsftpd服务程序将完整的光盘镜像文件传输过去。

```shell
[root@linuxprobe ~]# yum install tftp-server
Loaded plugins: langpacks, product-id, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
Resolving Dependencies
--> Running transaction check
---> Package tftp-server.x86_64 0:5.2-11.el7 will be installed
--> Processing Dependency: xinetd for package: tftp-server-5.2-11.el7.x86_64
--> Running transaction check
---> Package xinetd.x86_64 2:2.3.15-12.el7 will be installed
--> Finished Dependency Resolution
Dependencies Resolved
================================================================================
 Package Arch Version Repository Size
================================================================================
Installing:
 tftp-server x86_64 5.2-11.el7 rhel 44 k
Installing for dependencies:
 xinetd x86_64 2:2.3.15-12.el7 rhel 128 k
Transaction Summary
================================================================================
Install 1 Package (+1 Dependent package)
Total download size: 172 k
Installed size: 325 k
Is this ok [y/d/N]: y
Downloading packages:
--------------------------------------------------------------------------------
Total 1.7 MB/s | 172 kB 00:00 
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
 Installing : 2:xinetd-2.3.15-12.el7.x86_64 1/2 
 Installing : tftp-server-5.2-11.el7.x86_64 2/2 
 Verifying : 2:xinetd-2.3.15-12.el7.x86_64 1/2 
 Verifying : tftp-server-5.2-11.el7.x86_64 2/2 
Installed:
 tftp-server.x86_64 0:5.2-11.el7 
Dependency Installed:
 xinetd.x86_64 2:2.3.15-12.el7 
Complete!
```

TFTP是一种非常精简的文件传输服务程序，它的运行和关闭是由xinetd网络守护进程服务来管理的。xinetd服务程序会同时监听系统的多个端口，然后根据用户请求的端口号调取相应的服务程序来响应用户的请求。需要开启TFTP服务程序，只需在xinetd服务程序的配置文件中把disable参数改成no就可以了。保存配置文件并退出，然后重启xinetd服务程序，并将其加入到开机启动项中（在RHEL 7系统中，已经默认启用了xinetd服务程序，因此在将其添加到开机启动项中的时候没有输出信息属于正常情况）。

```shell
[root@linuxprobe ~.d]# vim /etc/xinetd.d/tftp
service tftp
{
        socket_type             = dgram
        protocol                = udp
        wait                    = yes
        user                    = root
        server                  = /usr/sbin/in.tftpd
        server_args             = -s /var/lib/tftpboot
        disable                 = no
        per_source              = 11
        cps                     = 100 2
        flags                   = IPv4
[root@linuxprobe xinetd.d]# systemctl restart xinetd
[root@linuxprobe xinetd.d]# systemctl enable xinetd
```

TFTP服务程序默认使用的是UDP协议，占用的端口号为69，所以在生产环境中还需要在firewalld防火墙管理工具中写入使其永久生效的允许策略，以便让客户端主机顺利获取到引导文件。

[root@linuxprobe ~]# firewall-cmd --permanent --add-port=69/udp
success
[root@linuxprobe ~]# firewall-cmd --reload 
success
19.2.3 配置SYSLinux服务程序
SYSLinux是一个用于提供引导加载的服务程序。与其说SYSLinux是一个服务程序，不如说更需要里面的引导文件，在安装好SYSLinux服务程序软件包后，/usr/share/syslinux目录中会出现很多引导文件。

```shell
[root@linuxprobe ~]# yum install syslinux
Loaded plugins: langpacks, product-id, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
Resolving Dependencies
--> Running transaction check
---> Package syslinux.x86_64 0:4.05-8.el7 will be installed
--> Finished Dependency Resolution
Dependencies Resolved
================================================================================
 Package Arch Version Repository Size
================================================================================
Installing:
 syslinux x86_64 4.05-8.el7 rhel 1.0 M
Transaction Summary
================================================================================
Install 1 Package
Total download size: 1.0 M
Installed size: 2.3 M
Is this ok [y/d/N]: y
Downloading packages:
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
 Installing : syslinux-4.05-8.el7.x86_64 1/1 
 Verifying : syslinux-4.05-8.el7.x86_64 1/1 
Installed:
 syslinux.x86_64 0:4.05-8.el7 
Complete!
```

我们首先需要把SYSLinux提供的引导文件复制到TFTP服务程序的默认目录中，也就是前文提到的文件pxelinux.0，这样客户端主机就能够顺利地获取到引导文件了。另外在RHEL 7系统光盘镜像中也有一些我们需要调取的引导文件。确认光盘镜像已经被挂载到/media/cdrom目录后，使用复制命令将光盘镜像中自带的一些引导文件也复制到TFTP服务程序的默认目录中。

```shell
# 进入tftp默认目录
[root@linuxprobe ~]# cd /var/lib/tftpboot
# 复制引导文件
[root@linuxprobe tftpboot]# cp /usr/share/syslinux/pxelinux.0 .
# 复制引导文件
[root@linuxprobe tftpboot]# cp /media/cdrom/images/pxeboot/{vmlinuz,initrd.img} .
[root@linuxprobe tftpboot]# cp /media/cdrom/isolinux/{vesamenu.c32,boot.msg} .
```

然后在TFTP服务程序的目录中新建pxelinux.cfg目录，虽然该目录的名字带有后缀，但依然也是目录，而非文件！将系统光盘中的开机选项菜单复制到该目录中，并命名为default。这个default文件就是开机时的选项菜单，如图19-4所示。

图19-4  Linux系统的引导菜单界面

```shell
[root@linuxprobe tftpboot]# mkdir pxelinux.cfg
[root@linuxprobe tftpboot]# cp /media/cdrom/isolinux/isolinux.cfg pxelinux.cfg/default
```

默认的开机菜单中有两个选项，要么是安装系统，要么是对安装介质进行检验。既然我们已经确定采用无人值守的方式安装系统，还需要为每台主机手动选择相应的选项，未免与我们的主旨（无人值守安装）相悖。现在我们编辑这个default文件，把第1行的default参数修改为linux，这样系统在开机时就会默认执行那个名称为linux的选项了。对应的linux选项大约在64行，我们将默认的光盘镜像安装方式修改成FTP文件传输方式，并指定好光盘镜像的获取网址以及Kickstart应答文件的获取路径：

```shell
[root@linuxprobe tftpboot]# vim pxelinux.cfg/default
# 第一行修改为default linux
 1 default linux
 2 timeout 600
 3
 4 display boot.msg
 5
 6 # Clear the screen when exiting the menu, instead of leaving the menu displa yed.
 7 # For vesamenu, this means the graphical background is still displayed witho ut
 8 # the menu itself for as long as the screen remains in graphics mode.
 9 menu clear
 10 menu background splash.png
 11 menu title Red Hat Enterprise Linux 7.0
 12 menu vshift 8
 13 menu rows 18
 14 menu margin 8
 15 #menu hidden
 16 menu helpmsgrow 15
 17 menu tabmsgrow 13
 18
 19 # Border Area
 20 menu color border * #00000000 #00000000 none
 21
 22 # Selected item
 23 menu color sel 0 #ffffffff #00000000 none
 24
 25 # Title bar
 26 menu color title 0 #ff7ba3d0 #00000000 none
 27
 28 # Press [Tab] message
 29 menu color tabmsg 0 #ff3a6496 #00000000 none
 30
 31 # Unselected menu item
 32 menu color unsel 0 #84b8ffff #00000000 none
 33
 34 # Selected hotkey
 35 menu color hotsel 0 #84b8ffff #00000000 none
 36
 37 # Unselected hotkey
 38 menu color hotkey 0 #ffffffff #00000000 none
 39
 40 # Help text
 41 menu color help 0 #ffffffff #00000000 none
 42 
 43 # A scrollbar of some type? Not sure.
 44 menu color scrollbar 0 #ffffffff #ff355594 none
 45 
 46 # Timeout msg
 47 menu color timeout 0 #ffffffff #00000000 none
 48 menu color timeout_msg 0 #ffffffff #00000000 none
 49 
 50 # Command prompt text
 51 menu color cmdmark 0 #84b8ffff #00000000 none
 52 menu color cmdline 0 #ffffffff #00000000 none
 53 
 54 # Do not display the actual menu unless the user presses a key. All that is displayed is a timeout message.
 55 
 56 menu tabmsg Press Tab for full configuration options on menu items.
 57 
 58 menu separator # insert an empty line
 59 menu separator # insert an empty line
 59 menu separator # insert an empty line
 60 
 # 标签为linux
 61 label linux
 62 menu label ^Install Red Hat Enterprise Linux 7.0
 63 kernel vmlinuz
 # 安装路径改成网络安装，欠下ftp，kickstart
 64 append initrd=initrd.img inst.stage2=ftp://192.168.10.10 ks=ftp://192.168.10.10/pub/ks.cfg quiet
 65
………………省略部分输出信息………………
```

19.2.4 配置VSFtpd服务程序
在我们这套无人值守安装系统的服务中，光盘镜像是通过FTP协议传输的，因此势必要用到vsftpd服务程序。当然，也可以使用httpd服务程序来提供Web网站访问的方式，只要能确保将光盘镜像顺利传输给客户端主机即可。如果打算使用Web网站服务来提供光盘镜像，一定记得将上面配置文件中的光盘镜像获取网址和Kickstart应答文件获取网址修改一下。

```shell
[root@linuxprobe ~]# yum install vsftpd
Loaded plugins: langpacks, product-id, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
Resolving Dependencies
--> Running transaction check
---> Package vsftpd.x86_64 0:3.0.2-9.el7 will be installed
--> Finished Dependency Resolution
Dependencies Resolved
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

刘遄老师再啰嗦一句，在配置文件修改正确之后，一定将相应的服务程序添加到开机启动项中，这样无论是在生产环境中还是在红帽认证考试中，都可以在设备重启之后依然能提供相应的服务。希望各位读者一定养成这个好习惯。

```shell
[root@linuxprobe ~]# systemctl restart vsftpd
[root@linuxprobe ~]# systemctl enable vsftpd
ln -s '/usr/lib/systemd/system/vsftpd.service' '/etc/systemd/system/multi-user.target.wants/vsftpd.service'
```

在确认系统光盘镜像已经正常挂载到/media/cdrom目录后，把目录中的光盘镜像文件全部复制到vsftpd服务程序的工作目录中。

```shell
[root@linuxprobe ~]# cp -r /media/cdrom/* /var/ftp
```

这个过程大约需要3～5分钟。在此期间，我们也别闲着，在firewalld防火墙管理工具中写入使FTP协议永久生效的允许策略，然后在SELinux中放行FTP传输：

```shell
[root@linuxprobe ~]# firewall-cmd --permanent --add-service=ftp
success
[root@linuxprobe ~]# firewall-cmd --reload 
success
[root@linuxprobe ~]# setsebool -P ftpd_connect_all_unreserved=on
```

19.2.5 创建KickStart应答文件
毕竟，我们使用PXE + Kickstart部署的是一套“无人值守安装系统服务”，而不是“无人值守传输系统光盘镜像服务”，因此还需要让客户端主机能够一边获取光盘镜像，还能够一边自动帮我们填写好安装过程中出现的选项。简单来说，如果生产环境中有100台服务器，它们需要安装相同的系统环境，那么在安装过程中单击的按钮和填写的信息也应该都是相同的。那么，为什么不创建一个类似于备忘录的需求清单呢？这样，在无人值守安装系统时，可以从这个需求清单中找到相应的选项值，从而免去了手动输入之苦，更重要的是，也彻底解放了人的干预，彻底实现无人值守自动安装系统，而不是单纯地传输系统光盘镜像。

有了上文做铺垫，相信大家现在应该可以猜到Kickstart其实并不是一个服务程序，而是一个应答文件了。是的！Kickstart应答文件中包含了系统安装过程中需要使用的选项和参数信息，系统可以自动调取这个应答文件的内容，从而彻底实现了无人值守安装系统。那么，既然这个文件如此重要，该去哪里找呢？其实在root管理员的家目录中有一个名为anaconda-ks.cfg的文件，它就是应答文件。下面将这个文件复制到vsftpd服务程序的工作目录中（在开机选项菜单的配置文件中已经定义了该文件的获取路径，也就是vsftpd服务程序数据目录中的pub子目录中）。使用chmod命令设置该文件的权限，确保所有人都有可读的权限，以保证客户端主机可以顺利获取到应答文件及里面的内容：

```shell
[root@linuxprobe ~]# cp ~/anaconda-ks.cfg /var/ftp/pub/ks.cfg
[root@linuxprobe ~]# chmod +r /var/ftp/pub/ks.cfg
```

Kickstart应答文件并没有想象中的那么复杂，它总共只有46行左右的参数和注释内容，大家完全可以通过参数的名称及介绍来快速了解每个参数的作用。刘遄老师在这里挑选几个比较有代表性的参数进行讲解，其他参数建议大家自行修改测试。

首先把第6行的光盘镜像安装方式修改成FTP协议，仔细填写好FTP服务器的IP地址，并用本地浏览器尝试打开下检查有没有报错。然后把第21行的时区修改成上海(Asia/Shanghai)，最后再把29行的磁盘选项设置为清空所有磁盘内容并初始化磁盘：

```shell
[root@linuxprobe ~]# vim /var/ftp/pub/ks.cfg
 1 #version=RHEL7
 2 # System authorization information
 3 auth --enableshadow --passalgo=sha512
 4 
 5 # Use CDROM installation media
 # 光盘镜像安装方式修改成FTP协议
 6 url --url=ftp://192.168.10.10
 7 # Run the Setup Agent on first boot
 8 firstboot --enable
 9 ignoredisk --only-use=sda
 10 # Keyboard layouts
 11 keyboard --vckeymap=us --xlayouts='us'
 12 # System language
 13 lang en_US.UTF-8
 14 
 15 # Network information
 16 network --bootproto=dhcp --device=eno16777728 --onboot=off --ipv6=auto
 17 network --hostname=localhost.localdomain
 18 # Root password
 19 rootpw --iscrypted $6$pDjJf42g8C6pL069$iI.PX/yFaqpo0ENw2pa7MomkjLyoae2zjMz2UZJ7b H3UO4oWtR1.Wk/hxZ3XIGmzGJPcs/MgpYssoi8hPCt8b/
 20 # System timezone
 # 时区修改成上海(Asia/Shanghai)
 21 timezone Asia/Shanghai --isUtc
 22 user --name=linuxprobe --password=$6$a9v3InSTNbweIR7D$JegfYWbCdoOokj9sodEccdO.zL F4oSH2AZ2ss2R05B6Lz2A0v2K.RjwsBALL2FeKQVgf640oa/tok6J.7GUtO/ --iscrypted --gecos ="linuxprobe"
 23 # X Window System configuration information
 24 xconfig --startxonboot
 25 # System bootloader configuration
 26 bootloader --location=mbr --boot-drive=sda
 27 autopart --type=lvm
 28 # Partition clearing information
 # 磁盘选项设置为清空所有磁盘内容并初始化磁盘
 29 clearpart --all --initlabel
 30 
 31 %packages
 32 @base
 33 @core
 34 @desktop-debugging
 35 @dial-up
 36 @fonts
 37 @gnome-desktop
 38 @guest-agents
 39 @guest-desktop-agents
 40 @input-methods
 41 @internet-browser
 42 @multimedia
 43 @print-client
 44 @x11
 45 
 46 %end
 ```

如果觉得系统默认自带的应答文件参数较少，不能满足生产环境的需求，则可以通过Yum软件仓库来安装system-config-kickstart软件包。这是一款图形化的Kickstart应答文件生成工具，可以根据自己的需求生成自定义的应答文件，然后将生成的文件放到/var/ftp/pub目录中并将名字修改为ks.cfg即可。

19.3 自动部署客户机
在按照上文讲解的方法成功部署各个相关的服务程序后，就可以使用PXE + Kickstart无人值守安装系统了。在采用下面的步骤建立虚拟主机时，一定要把客户端的网卡模式设定成与服务端一致的“仅主机模式”，否则两台设备无法进行通信，也就更别提自动安装系统了。其余硬件配置选项并没有强制性要求，大家可参考这里的配置选项来设定。

第1步：打开“新建虚拟机向导”程序，选择“典型（推荐） ”配置类型，然后单击“下一步”按钮，如图19-5所示。

图19-5  选择虚拟机的配置类型

第2步：将虚拟机操作系统的安装来源设置为“稍后安装操作系统”。这样做的目的是让虚拟机真正从网络中获取系统安装镜像，同时也可避免VMware Workstation虚拟机软件按照内设的方法自行安装系统。单击“下一步”按钮，如图19-6所示。

图19-6  设置虚拟机操作系统的安装来源

第3步：将“客户机操作系统”设置为“Red Hat Enterprise Linux 7 64位”，然后单击“下一步”按钮，如图19-7所示。

图19-7  选择客户端主机的操作系统

第4步：对虚拟机进行命名并设置安装位置。大家可自行定义虚拟机的名称，而安装位置则尽量选择磁盘空间较大的分区。然后单击“下一步”按钮，如图19-8所示。

图19-8  命名虚拟机并设置虚拟机的安装位置

第5步：指定磁盘容量。这里将“最大磁盘大小”设置为20GB，指的是虚拟机系统能够使用的最大上限，而不是会被立即占满，因此设置得稍微大一些也没有关系。然后单击“下一步”按钮，如图19-9所示。

图19-9  将磁盘容量指定为20GB

第6步：结束“新建虚拟机向导程序”后，先不要着急打开虚拟机系统。大家还需要单击图19-10中的“自定义硬件”按钮，在弹出的如图19-11所示的界面中，把“网络适配器”设备同样也设置为“仅主机模式”（这个步骤非常重要），然后单击“确定”按钮。

图19-10  单击虚拟机的“自定义硬件”按钮

图19-11  设置虚拟机网络适配器设备为仅主机模式

现在，我们就同时准备好了PXE + Kickstart无人值守安装系统与虚拟主机。在生产环境中，大家只需要将配置妥当的服务器上架，接通服务器和客户端主机之间的网线，然后启动客户端主机即可。接下来就会按照图19-12和图19-13那样，开始传输光盘镜像文件并进行自动安装了—期间完全无须人工干预，直到安装完毕时才需要运维人员进行简单的初始化工作。

图19-12  自动传输光盘镜像文件并安装系统

图19-13  自动安装系统，无须人工干预

由此可见，当生产环境工作中有数百台服务器需要批量安装系统时，使用无人值守安装系统的便捷性是不言而喻的。

出现问题?大胆提问!

因读者们硬件不同或操作错误都可能导致实验配置出错，请耐心再仔细看看操作步骤吧，不要气馁~

Linux技术交流请加A群：560843(满)，B群：340829(推荐)，C群：463590（推荐），点此查看全国群。

*本群特色：通过口令验证确保每一个群员都是《Linux就该这么学》的读者，答疑更有针对性，不定期免费领取定制礼品。

本章节的复习作业(答案就在问题的下一行哦，用鼠标选中即可看到的~)

1．部署无人值守安装系统，需要用到哪些服务程序？

答：需要用到SYSLinux引导服务、DHCP服务、vsftpd文件传输服务（或httpd网站服务）、TFTP服务以及KickStart应答文件。

2．在Vmware Workstation虚拟机软件中，DHCP服务总是分配错误IP地址的原因可能是什么？

答：虚拟机的虚拟网络编辑器中自带的DHCP服务可能没有关闭，由此产生了错误分配IP地址的情况。

3．如何启用TFTP服务？

答：需要在xinetd服务程序的配置文件中把disable参数改成no。

4．成功安装SYSLinux服务程序后，可以在哪个目录中找到引导文件？

答：在安装好SYSLinux服务程序软件包后，在/usr/share/syslinux目录中会出现很多引导文件。

5．在开机选项菜单文件中，把default参数设置成linux的作用是什么？

答：目的是让系统自动开始安装过程，而不需要运维人员再去选择是安装系统还是校验镜像文件。

6．安装vsftpd文件传输服务或httpd网站服务的作用是什么？

答：把光盘镜像文件完整、顺利地传送到客户端主机。

7．Kickstart应答文件的作用是什么？

答：Kickstart应答文件中包含了系统安装过程中需要使用的选项和参数信息，客户端主机在安装系统的过程中可以自动调取这个应答