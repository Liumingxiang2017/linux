# 使用iSCSI服务部署网络存储

17.1 iSCSI技术介绍

iSCSI = internet+SCSI

硬盘是计算机硬件设备中重要的组成部分之一，硬盘存储设备读写速度的快慢也会对服务器的整体性能造成影响。第6章、第7章讲解的硬盘存储结构、RAID磁盘阵列技术以及LVM技术等都是用于存储设备的技术，尽管这些技术有软件层面和硬件层面之分，但是它们都旨在解决硬盘存储设备的读写速度问题，或者竭力保障存储数据的安全。

为了进一步提升硬盘存储设备的读写速度和性能，人们一直在努力改进物理硬盘设备的接口协议。当前的硬盘接口类型主要有IDE、SCSI和SATA这3种。

IDE是一种成熟稳定、价格便宜的并行传输接口。

SATA是一种传输速度更快、数据校验更完整的串行传输接口。

SCSI是一种用于计算机和硬盘、光驱等设备之间系统级接口的通用标准，具有系统资源占用率低、转速高、传输速度快等优点。

不论使用什么类型的硬盘接口，硬盘上的数据总是要通过计算机主板上的总线与CPU、内存设备进行数据交换，这种物理环境上的限制给硬盘资源的共享带来了各种不便。后来，IBM公司开始动手研发基于TCP/IP协议和SCSI接口协议的新型存储技术，这也就是我们目前能看到的互联网小型计算机系统接口（iSCSI，Internet Small Computer System Interface）。这是一种将SCSI接口与以太网技术相结合的新型存储技术，可以用来在网络中传输SCSI接口的命令和数据。这样，不仅克服了传统SCSI接口设备的物理局限性，实现了跨区域的存储资源共享，还可以在不停机的状态下扩展存储容量。

为了让各位读者做到知其然，知其所以然，以便在工作中灵活使用这项技术，下面将讲解一下iSCSI技术在生产环境中的优势和劣势。首先，iSCSI存储技术非常便捷，在访问存储资源的形式上发生了很大变化，摆脱了物理环境的限制，同时还可以把存储资源分给多个服务器共同使用，因此是一种非常推荐使用的存储技术。但是，iSCSI存储技术受到了网速的制约。以往，硬盘设备直接通过主板上的总线进行数据传输，现在则需要让互联网作为数据传输的载体和通道，因此传输速率和稳定性是iSCSI技术的瓶颈。随着网络技术的持续发展，相信iSCSI技术也会随之得以改善。

既然要通过以太网来传输硬盘设备上的数据，那么数据是通过网卡传入到计算机中的么？这就有必要向大家介绍iSCSI-HBA卡了（见图17-1）。与一般的网卡不同（连接网络总线和内存，供计算机上网使用），iSCSI-HBA卡连接的则是SCSI接口或FC（光纤通道）总线和内存，专门用于在主机之间交换存储数据，其使用的协议也与一般网卡有本质的不同。运行Linux系统的服务器会基于iSCSI协议把硬盘设备命令与数据打包成标准的TCP/IP数据包，然后通过以太网传输到目标存储设备，而当目标存储设备接收到这些数据包后，还需要基于iSCSI协议把TCP/IP数据包解压成硬盘设备命令与数据。

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-1  iSCSI-HBA卡实拍图

17.2 创建RAID磁盘阵列
既然要使用iSCSI存储技术为远程用户提供共享存储资源，首先要保障用于存放资源的服务器的稳定性与可用性，否则一旦在使用过程中出现故障，则维护的难度相较于本地硬盘设备要更加复杂、困难。因此推荐各位读者按照本书第7章讲解的知识来部署RAID磁盘阵列组，确保数据的安全性。下面以配置RAID 5磁盘阵列组为例进行讲解。考虑到第7章已经事无巨细地讲解了RAID磁盘阵列技术和配置方法，因此本节不会再重复介绍相关参数的意义以及用途，忘记了的读者可以翻回去看一下。

首先在虚拟机中添加4块新硬盘，用于创建RAID 5磁盘阵列和备份盘，如图17-2所示。

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-2  添加4块用于创建RAID 5级别磁盘阵列的新硬盘

启动虚拟机系统，使用mdadm命令创建RAID磁盘阵列。其中，-Cv参数为创建阵列并显示过程，/dev/md0为生成的阵列组名称，-n 3参数为创建RAID 5磁盘阵列所需的硬盘个数，-l 5参数为RAID磁盘阵列的级别，-x 1参数为磁盘阵列的备份盘个数。在命令后面要逐一写上使用的硬盘名称。另外，还可以使用第3章讲解的通配符来指定硬盘设备的名称，有兴趣的读者可以试一下。

[root@linuxprobe ~]# mdadm -Cv /dev/md0 -n 3 -l 5 -x 1 /dev/sdb /dev/sdc /dev/sdd /dev/sde
mdadm: layout defaults to left-symmetric
mdadm: layout defaults to left-symmetric
mdadm: chunk size defaults to 512K
mdadm: size set to 20954624K
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md0 started.
在上述命令成功执行之后，得到一块名称为/dev/md0的新设备，这是一块RAID 5级别的磁盘阵列，并且还有一块备份盘为硬盘数据保驾护航。大家可使用mdadm -D命令来查看设备的详细信息。另外，由于在使用远程设备时极有可能出现设备识别顺序发生变化的情况，因此，如果直接在fstab挂载配置文件中写入/dev/sdb、/dev/sdc等设备名称的话，就有可能在下一次挂载了错误的存储设备。而UUID值是设备的唯一标识符，可以用于精确地区分本地或远程设备。于是我们可以把这个值记录下来，一会儿准备填写到挂载配置文件中。

[root@linuxprobe ~]# mdadm -D /dev/md0
/dev/md0:
        Version : 1.2
  Creation Time : Thu Sep 24 21:59:57 2017
     Raid Level : raid5
     Array Size : 41909248 (39.97 GiB 42.92 GB)
  Used Dev Size : 20954624 (19.98 GiB 21.46 GB)
   Raid Devices : 3
  Total Devices : 4
    Persistence : Superblock is persistent
    Update Time : Thu Sep 24 22:02:23 2017
          State : clean 
 Active Devices : 3
Working Devices : 4
 Failed Devices : 0
  Spare Devices : 1
         Layout : left-symmetric
     Chunk Size : 512K
           Name : linuxprobe.com:0  (local to host linuxprobe.com)
           UUID : 3370f643:c10efd6a:44e91f2a:20c71f3e
         Events : 26
    Number   Major   Minor   RaidDevice State
       0       8       16        0      active sync   /dev/sdb
       1       8       32        1      active sync   /dev/sdc
       4       8       48        2      active sync   /dev/sdd
       3       8       64        -      spare   /dev/sde
17.3 配置iSCSI服务端
iSCSI技术在工作形式上分为服务端（target）与客户端（initiator）。iSCSI服务端即用于存放硬盘存储资源的服务器，它作为前面创建的RAID磁盘阵列的存储端，能够为用户提供可用的存储资源。iSCSI客户端则是用户使用的软件，用于访问远程服务端的存储资源。下面按照表17-1来配置iSCSI服务端和客户端所用的IP地址。

表17-1                             iSCSI服务端和客户端的操作系统以及IP地址

主机名称	操作系统	IP地址
iSCSI服务端	RHEL 7	192.168.10.10
iSCSI客户端	RHEL 7	192.168.10.20
第1步：配置好Yum软件仓库后安装iSCSI服务端程序以及配置命令工具。通过在yum命令的后面添加-y参数，在安装过程中就不需要再进行手动确认了：

[root@linuxprobe ~]# yum -y install targetd targetcli
Loaded plugins: langpacks, product-id, subscription-manager
………………省略部分输出信息………………
Installing:
 targetcli noarch 2.1.fb34-1.el7 rhel 55 k
 targetd noarch 0.7.1-1.el7 rhel 48 k
Installing for dependencies:
 PyYAML x86_64 3.10-11.el7 rhel 153 k
 libyaml x86_64 0.1.4-10.el7 rhel 55 k
 lvm2-python-libs x86_64 7:2.02.105-14.el7 rhel 153 k
 pyparsing noarch 1.5.6-9.el7 rhel 94 k
 python-configshell noarch 1:1.1.fb11-3.el7 rhel 64 k
 python-kmod x86_64 0.9-4.el7 rhel 57 k
 python-rtslib noarch 2.1.fb46-1.el7 rhel 75 k
 python-setproctitle x86_64 1.1.6-5.el7 rhel 15 k
 python-urwid x86_64 1.1.1-3.el7 rhel 654 k
………………省略部分输出信息………………
Installed:
 targetcli.noarch 0:2.1.fb34-1.el7 targetd.noarch 0:0.7.1-1.el7 
Dependency Installed:
 PyYAML.x86_64 0:3.10-11.el7 
 libyaml.x86_64 0:0.1.4-10.el7 
 lvm2-python-libs.x86_64 7:2.02.105-14.el7 
 pyparsing.noarch 0:1.5.6-9.el7 
 python-configshell.noarch 1:1.1.fb11-3.el7 
 python-kmod.x86_64 0:0.9-4.el7 
 python-rtslib.noarch 0:2.1.fb46-1.el7 
 python-setproctitle.x86_64 0:1.1.6-5.el7 
 python-urwid.x86_64 0:1.1.1-3.el7 
Complete!
安装完成后启动iSCSI的服务端程序targetd，然后把这个服务程序加入到开机启动项中，以便下次在服务器重启后依然能够为用户提供iSCSI共享存储资源服务：

[root@linuxprobe ~]# systemctl start targetd
[root@linuxprobe ~]# systemctl enable targetd
 ln -s '/usr/lib/systemd/system/targetd.service' '/etc/systemd/system/multi-user.target.wants/targetd.service'
第2步：配置iSCSI服务端共享资源。targetcli是用于管理iSCSI服务端存储资源的专用配置命令，它能够提供类似于fdisk命令的交互式配置功能，将iSCSI共享资源的配置内容抽象成“目录”的形式，我们只需将各类配置信息填入到相应的“目录”中即可。这里的难点主要在于认识每个“参数目录”的作用。当把配置参数正确地填写到“目录”中后，iSCSI服务端也可以提供共享资源服务了。

在执行targetcli命令后就能看到交互式的配置界面了。在该界面中可以使用很多Linux命令，比如利用ls查看目录参数的结构，使用cd切换到不同的目录中。/backstores/block是iSCSI服务端配置共享设备的位置。我们需要把刚刚创建的RAID 5磁盘阵列md0文件加入到配置共享设备的“资源池”中，并将该文件重新命名为disk0，这样用户就不会知道是由服务器中的哪块硬盘来提供共享存储资源，而只会看到一个名为disk0的存储设备。

[root@linuxprobe ~]# targetcli
Warning: Could not load preferences file /root/.targetcli/prefs.bin.
targetcli shell version 2.1.fb34
Copyright 2011-2013 by Datera, Inc and others.
For help on commands, type 'help'.
/> ls
o- / ..................................................................... [...]
o- backstores .......................................................... [...]
| o- block .............................................. [Storage Objects: 0]
| o- fileio ............................................. [Storage Objects: 0]
| o- pscsi .............................................. [Storage Objects: 0]
| o- ramdisk ............................................ [Storage Objects: 0]
o- iscsi ........................................................ [Targets: 0]
o- loopback ..................................................... [Targets: 0
/> cd /backstores/block
/backstores/block> create disk0 /dev/md0
Created block storage object disk0 using /dev/md0.
/backstores/block> cd /
/> ls
o- / ..................................................................... [...]
  o- backstores .......................................................... [...]
  | o- block .............................................. [Storage Objects: 1]
  | | o- disk0 ..................... [/dev/md0 (40.0GiB) write-thru deactivated]
  | o- fileio ............................................. [Storage Objects: 0]
  | o- pscsi .............................................. [Storage Objects: 0]
  | o- ramdisk ............................................ [Storage Objects: 0]
  o- iscsi ........................................................ [Targets: 0]
  o- loopback ..................................................... [Targets: 0]
第3步：创建iSCSI target名称及配置共享资源。iSCSI target名称是由系统自动生成的，这是一串用于描述共享资源的唯一字符串。稍后用户在扫描iSCSI服务端时即可看到这个字符串，因此我们不需要记住它。系统在生成这个target名称后，还会在/iscsi参数目录中创建一个与其字符串同名的新“目录”用来存放共享资源。我们需要把前面加入到iSCSI共享资源池中的硬盘设备添加到这个新目录中，这样用户在登录iSCSI服务端后，即可默认使用这硬盘设备提供的共享存储资源了。

/> cd iscsi
/iscsi> 
/iscsi> create
Created target iqn.2003-01.org.linux-iscsi.linuxprobe.x8664:sn.d497c356ad80.
Created TPG 1.
/iscsi> cd iqn.2003-01.org.linux-iscsi.linuxprobe.x8664:sn.d497c356ad80/
/iscsi/iqn.20....d497c356ad80> ls
o- iqn.2003-01.org.linux-iscsi.linuxprobe.x8664:sn.d497c356ad80 ...... [TPGs: 1]
  o- tpg1 ............................................... [no-gen-acls, no-auth]
    允许用户访问列表的名称
    o- acls .......................................................... [ACLs: 0]
    用户访问设备名称
    o- luns .......................................................... [LUNs: 0]
    由哪个地址端口号提供iscsi
    o- portals .................................................... [Portals: 0]
/iscsi/iqn.20....d497c356ad80> cd tpg1/luns
/iscsi/iqn.20...d80/tpg1/luns> create /backstores/block/disk0 
Created LUN 0.
第4步：设置访问控制列表（ACL）。iSCSI协议是通过客户端名称进行验证的，也就是说，用户在访问存储共享资源时不需要输入密码，只要iSCSI客户端的名称与服务端中设置的访问控制列表中某一名称条目一致即可，因此需要在iSCSI服务端的配置文件中写入一串能够验证用户信息的名称。acls参数目录用于存放能够访问iSCSI服务端共享存储资源的客户端名称。刘遄老师推荐在刚刚系统生成的iSCSI target后面追加上类似于:client的参数，这样既能保证客户端的名称具有唯一性，又非常便于管理和阅读：

/iscsi/iqn.20...d80/tpg1/luns> cd ..
/iscsi/iqn.20...c356ad80/tpg1> cd acls 
/iscsi/iqn.20...d80/tpg1/acls> create iqn.2003-01.org.linux-iscsi.linuxprobe.x8664:sn.d497c356ad80:client
Created Node ACL for iqn.2003-01.org.linux-iscsi.linuxprobe.x8664:sn.d497c356ad80:client
Created mapped LUN 0.
第5步：设置iSCSI服务端的监听IP地址和端口号。位于生产环境中的服务器上可能有多块网卡，那么到底是由哪个网卡或IP地址对外提供共享存储资源呢？这就需要我们在配置文件中手动定义iSCSI服务端的信息，即在portals参数目录中写上服务器的IP地址。接下来将由系统自动开启服务器192.168.10.10的3260端口将向外提供iSCSI共享存储资源服务：

/iscsi/iqn.20...d80/tpg1/acls> cd ..
/iscsi/iqn.20...c356ad80/tpg1> cd portals 
/iscsi/iqn.20.../tpg1/portals> create 192.168.10.10
Using default IP port 3260
Created network portal 192.168.10.10:3260.
第6步：配置妥当后检查配置信息，重启iSCSI服务端程序并配置防火墙策略。在参数文件配置妥当后，可以浏览刚刚配置的信息，确保与下面的信息基本一致。在确认信息无误后输入exit命令来退出配置。注意，千万不要习惯性地按Ctrl + C组合键结束进程，这样不会保存配置文件，我们的工作也就白费了。最后重启iSCSI服务端程序，再设置firewalld防火墙策略，使其放行3260/tcp端口号的流量。

/iscsi/iqn.20.../tpg1/portals> ls /
o- / ........................... [...]
  o- backstores................. [...]
  | o- block ................... [Storage Objects: 1]
  | | o- disk0 ................. [/dev/md0 (40.0GiB) write-thru activated]
  | o- fileio .................. [Storage Objects: 0]
  | o- pscsi ................... [Storage Objects: 0]
  | o- ramdisk ................. [Storage Objects: 0]
  o- iscsi ..................... [Targets: 1]
  | o- iqn.2003-01.org.linux-iscsi.linuxprobe.x8664:sn.d497c356ad80 .... [TPGs: 1]
  |   o- tpg1 .................. [no-gen-acls, no-auth]
  |     o- acls ........................................................ [ACLs: 1]
  |     | o- iqn.2003-01.org.linux-iscsi.linuxprobe.x8664:sn.d497c356ad80:client [Mapped LUNs: 1]
  |     |   o- mapped_lun0 ............................................. [lun0 block/disk0 (rw)]  
    o- luns .................... [LUNs: 1]
  |     | o- lun0 .............. [block/disk0 (/dev/md0)]
  |     o- portals ............. [Portals: 1]
  |       o- 192.168.10.10:3260  [OK]
  o- loopback .................. [Targets: 0]
/> exit
Global pref auto_save_on_exit=true
Last 10 configs saved in /etc/target/backup.
Configuration saved to /etc/target/saveconfig.json
[root@linuxprobe ~]# systemctl restart targetd
[root@linuxprobe ~]# firewall-cmd --permanent --add-port=3260/tcp 
success 
[root@linuxprobe ~]# firewall-cmd --reload 
success
17.4 配置Linux客户端
我们在前面的章节中已经配置了很多Linux服务，基本上可以说，无论是什么服务，客户端的配置步骤都要比服务端的配置步骤简单一些。在RHEL 7系统中，已经默认安装了iSCSI客户端服务程序initiator。如果您的系统没有安装的话，可以使用Yum软件仓库手动安装。

[root@linuxprobe ~]# yum install iscsi-initiator-utils 
Loaded plugins: langpacks, product-id, subscription-manager 
Package iscsi-initiator-utils-6.2.0.873-21.el7.x86_64 already installed and latest version 
Nothing to do
前面讲到，iSCSI协议是通过客户端的名称来进行验证，而该名称也是iSCSI客户端的唯一标识，而且必须与服务端配置文件中访问控制列表中的信息一致，否则客户端在尝试访问存储共享设备时，系统会弹出验证失败的保存信息。

下面我们编辑iSCSI客户端中的initiator名称文件，把服务端的访问控制列表名称填写进来，然后重启客户端iscsid服务程序并将其加入到开机启动项中：

[root@linuxprobe ~]# vim /etc/iscsi/initiatorname.iscsi
InitiatorName=iqn.2003-01.org.linux-iscsi.linuxprobe.x8664:sn.d497c356ad80:client
[root@linuxprobe ~]# systemctl restart iscsid
[root@linuxprobe ~]# systemctl enable iscsid
 ln -s '/usr/lib/systemd/system/iscsid.service' '/etc/systemd/system/multi-user.target.wants/iscsid.service'
iSCSI客户端访问并使用共享存储资源的步骤很简单，只需要记住刘遄老师的一个小口诀“先发现，再登录，最后挂载并使用”。iscsiadm是用于管理、查询、插入、更新或删除iSCSI数据库配置文件的命令行工具，用户需要先使用这个工具扫描发现远程iSCSI服务端，然后查看找到的服务端上有哪些可用的共享存储资源。其中，-m discovery参数的目的是扫描并发现可用的存储资源，-t st参数为执行扫描操作的类型，-p 192.168.10.10参数为iSCSI服务端的IP地址：

[root@linuxprobe ~]# iscsiadm -m discovery -t st -p 192.168.10.10
192.168.10.10:3260,1 iqn.2003-01.org.linux-iscsi.linuxprobe.x8664:sn.d497c356ad80
在使用iscsiadm命令发现了远程服务器上可用的存储资源后，接下来准备登录iSCSI服务端。其中，-m node参数为将客户端所在主机作为一台节点服务器，-T  iqn.2003-01. org.linux-iscsi.linuxprobe.x8664:sn.d497c356ad80参数为要使用的存储资源（大家可以直接复制前面命令中扫描发现的结果，以免录入错误），-p 192.168.10.10参数依然为对方iSCSI服务端的IP地址。最后使用--login或-l参数进行登录验证。

[root@linuxprobe ~]# iscsiadm -m node -T iqn.2003-01.org.linux-iscsi.linuxprobe.x8664:sn.d497c356ad80 -p 192.168.10.10 --login
Logging in to [iface: default, target: iqn.2003-01.org.linux-iscsi.linuxprobe.x8664:sn.d497c356ad80, portal: 192.168.10.10,3260] (multiple)
Login to [iface: default, target: iqn.2003-01.org.linux-iscsi.linuxprobe.x8664:sn.d497c356ad80, portal: 192.168.10.10,3260] successful.
在iSCSI客户端成功登录之后，会在客户端主机上多出一块名为/dev/sdb的设备文件。第6章曾经讲过，udev服务在命名硬盘名称时，与硬盘插槽是没有关系的。接下来可以像使用本地主机上的硬盘那样来操作这个设备文件了。

[root@linuxprobe ~]# file /dev/sdb 
/dev/sdb: block special
下面进入标准的磁盘操作流程。考虑到大家已经在第6章学习了这部分内容，外加这个设备文件本身只有40GB的容量，因此我们不再进行分区，而是直接格式化并挂载使用。

[root@linuxprobe ~]# mkfs.xfs /dev/sdb
log stripe unit (524288 bytes) is too large (maximum is 256KiB)
log stripe unit adjusted to 32KiB
meta-data=/dev/sdb               isize=256    agcount=16, agsize=654720 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=0
data     =                       bsize=4096   blocks=10475520, imaxpct=25
         =                       sunit=128    swidth=256 blks
naming   =version 2              bsize=4096   ascii-ci=0 ftype=0
log      =internal log           bsize=4096   blocks=5120, version=2
         =                       sectsz=512   sunit=8 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
[root@linuxprobe ~]# mkdir /iscsi
[root@linuxprobe ~]# mount /dev/sdb /iscsi
[root@linuxprobe ~]# df -h
Filesystem             Size  Used Avail Use% Mounted on
/dev/mapper/rhel-root   18G  3.4G   15G  20% /
devtmpfs               734M     0  734M   0% /dev
tmpfs                  742M  176K  742M   1% /dev/shm
tmpfs                  742M  8.8M  734M   2% /run
tmpfs                  742M     0  742M   0% /sys/fs/cgroup
/dev/sr0               3.5G  3.5G     0 100% /media/cdrom
/dev/sda1              497M  119M  379M  24% /boot
/dev/sdb                40G   33M   40G   1% /iscsi
从此以后，这个设备文件就如同是客户端本机主机上的硬盘那样工作。需要提醒大家的是，由于udev服务是按照系统识别硬盘设备的顺序来命名硬盘设备的，当客户端主机同时使用多个远程存储资源时，如果下一次识别远程设备的顺序发生了变化，则客户端挂载目录中的文件也将随之混乱。为了防止发生这样的问题，我们应该在/etc/fstab配置文件中使用设备的UUID唯一标识符进行挂载，这样，不论远程设备资源的识别顺序再怎么变化，系统也能正确找到设备所对应的目录。

blkid命令用于查看设备的名称、文件系统及UUID。可以使用管道符（详见第3章）进行过滤，只显示与/dev/sdb设备相关的信息：

[root@linuxprobe ~]# blkid | grep /dev/sdb
/dev/sdb: UUID="eb9cbf2f-fce8-413a-b770-8b0f243e8ad6" TYPE="xfs" 
刘遄老师还要再啰嗦一句，由于/dev/sdb是一块网络存储设备，而iSCSI协议是基于TCP/IP网络传输数据的，因此必须在/etc/fstab配置文件中添加上_netdev参数，表示当系统联网后再进行挂载操作，以免系统开机时间过长或开机失败：

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
UUID=eb9cbf2f-fce8-413a-b770-8b0f243e8ad6 /iscsi xfs defaults,_netdev 0 0
如果我们不再需要使用iSCSI共享设备资源了，可以用iscsiadm命令的-u参数将其设备卸载：

[root@linuxprobe ~]# iscsiadm -m node -T iqn.2003-01.org.linux-iscsi.linuxprobe.x8664:sn.d497c356ad80 -u

Logging out of session [sid: 7, target : iqn.2003-01.org.linux-iscsi.linuxprobe.x8664:sn.d497c356ad80, portal: 192.168.10.10,3260]

Logout of [sid: 7, target: iqn.2003-01.org.linux-iscsi.linuxprobe.x8664:sn.d497c356ad80,portal:192.168.10.10,3260] successful.

17.5 配置Windows客户端
使用Windows系统的客户端也可以正常访问iSCSI服务器上的共享存储资源，而且操作原理及步骤与Linux系统的客户端基本相同。在进行下面的实验之前，请先关闭Linux系统客户端，以免这两台客户端主机同时使用iSCSI共享存储资源而产生潜在问题。下面按照表17-2来配置iSCSI服务器和Windows客户端所用的IP地址。

表17-2    iSCSI服务器和客户端的操作系统以及IP地址

主机名称	操作系统	IP地址
iSCSI服务端	RHEL 7	192.168.10.10
Windows系统客户端	Windows 7	192.168.10.30
第1步：运行iSCSI发起程序。在Windows 7操作系统中已经默认安装了iSCSI客户端程序，我们只需在控制面板中找到“系统和安全”标签，然后单击“管理工具”（见图17-3），进入到“管理工具”页面后即可看到“iSCSI发起程序”图标。双击该图标。在第一次运行iSCSI发起程序时，系统会提示“Microsoft iSCSI服务端未运行”，单击“是”按钮即可自动启动并运行iSCSI发起程序，如图17-4所示。

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-3  在控制面板中单击“管理工具”

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-4  双击“iSCSI发起程序”图标

第2步：扫描发现iSCSI服务端上可用的存储资源。不论是Windows系统还是Linux系统，要想使用iSCSI共享存储资源都必须先进行扫描发现操作。运行iSCSI发起程序后在“目标”选项卡的“目标”文本框中写入iSCSI服务端的IP地址，然后单击“快速连接”按钮，如图17-5所示。

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-5  填写iSCSI服务端的IP地址

在弹出的“快速连接”提示框中可看到共享的硬盘存储资源，单击“完成”按钮即可，如图17-6所示。

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-6  在“快速连接”提示框中看到的共享的硬盘存储资源

回到“目标”选项卡页面，可以看到共享存储资源的名称已经出现，如图17-7所示。

第3步：准备连接iSCSI服务端的共享存储资源。由于在iSCSI服务端程序上设置了ACL，使得只有客户端名称与ACL策略中的名称保持一致时才能使用远程存储资源，因此需要在“配置”选项卡中单击“更改”按钮，把iSCSI发起程序的名称修改为服务端

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-7  在“目标”选项卡中看到了共享存储资源

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-8  修改iSCSI发起程序的名称

在确认客户端发起程序的名称修改正确后即可返回到“目标”选项卡页面中，然后单击“连接”按钮进行连接请求，成功连接到远程共享存储资源的页面如图17-9所示。

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-9  成功连接到远程共享存储资源

第4步：访问iSCSI远程共享存储资源。右键单击桌面上的“计算机”图标，打开计算机管理程序，如图17-10所示。

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-10  计算机管理程序的界面

开始对磁盘进行初始化操作，如图17-11所示。Windows系统用来初始化磁盘设备的步骤十分简单，各位读者都可以玩得转Linux系统，相信Windows系统就更不在话下了。Windows系统的初始化过程步骤如图17-12至图17-18所示。

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-11  对磁盘设备进行初始化操作

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-12  开始使用“新建简单卷向导”

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-13  对磁盘设备进行分区操作

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-14  设置系统中显示的盘符

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-15  设置磁盘设备的格式以及卷标

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-16   检查磁盘初始化信息是否正确

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-17   等待磁盘设备初始化过程结束

第17章 使用iSCSI服务部署网络存储。第17章 使用iSCSI服务部署网络存储。

图17-18  磁盘初始化完毕后弹出设备图标

出现问题?大胆提问!

因读者们硬件不同或操作错误都可能导致实验配置出错，请耐心再仔细看看操作步骤吧，不要气馁~

Linux技术交流请加A群：560843(满)，B群：340829(推荐)，C群：463590（推荐），点此查看全国群。

*本群特色：通过口令验证确保每一个群员都是《Linux就该这么学》的读者，答疑更有针对性，不定期免费领取定制礼品。

本章节的复习作业(答案就在问题的下一行哦，用鼠标选中即可看到的~)

1．简述iSCSI存储技术在生产环境中的作用。

答：iSCSI存储技术通过把硬件存储设备与TCP/IP网络协议相互结合，使得用户可以通过互联网方便的访问远程机房提供的共享存储资源。

2．在Linux系统中，iSCSI服务端和iSCSI客户端所使用的服务程序分别叫什么？

答：iSCSI服务端程序为targetd，iSCSI客户端程序为initiator。

3．在使用targetcli命令配置iSCSI服务端配置文件时，acls与portals参数目录中分别存放什么内容？

答：acls参数目录用于存放能够访问iSCSI服务端共享存储资源的客户端名称，portals参数目录用于定义由服务器的哪个IP地址对外提供共享存储资源服务。

4．iSCSI协议占用了服务器哪个协议和端口号？

答：iSCSI协议占用了服务器TCP协议的3260端口号。

5．用户在填写fstab设备挂载配置文件时，一般会把远程存储资源的UUID（而非设备的名称）填写到配置文件中。这是为什么？

答：在Linux系统中，设备名称是由udev服务进行管理的，而udev服务的设备命名规则是由设备类型及系统识别顺序等信息共同组成的。考虑到网络存储设备具有识别顺序不稳定的特点，所以为了避免识别顺序混乱造成的挂载错误问题，故使用UUID进行挂载操作。

6．在使用Windows系统来访问iSCSI共享存储资源时，它有两个步骤与Linux系统一样。请说明是哪两个步骤。

答：扫描并发现服务端上可用的iSCSI共享存储资源；验证登录。