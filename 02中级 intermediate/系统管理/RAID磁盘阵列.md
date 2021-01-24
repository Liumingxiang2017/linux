# RAID磁盘阵列

<!-- TOC -->

1. [RAID磁盘阵列](#raid磁盘阵列)
    1. [RAID级别](#raid级别)
        1. [RAID0：条带](#raid0条带)
        2. [RAID1：镜像](#raid1镜像)
        3. [RAID4](#raid4)
        4. [RAID5](#raid5)
        5. [RAID6](#raid6)
        6. [RAID-10 最常用](#raid-10-最常用)
        7. [RAID-01:](#raid-01)
        8. [RAID-50:](#raid-50)
        9. [JBOD:](#jbod)
    2. [mdadm 管理磁盘阵列](#mdadm-管理磁盘阵列)
        1. [创建模式](#创建模式)
        2. [管理模式](#管理模式)
        3. [监控模式](#监控模式)
        4. [增长模式](#增长模式)
        5. [装配模式](#装配模式)
        6. [查看RAID阵列的详细信息](#查看raid阵列的详细信息)
        7. [停止阵列](#停止阵列)

<!-- /TOC -->

> 旧时名称：Redundant Arrays of Inexpensive Disks 廉价冗余磁盘阵列
> 现在名称：Redundant Arrays of Independent Disks 独立冗余磁盘阵列

伯克利Berkeley大学1988年提出 A case for Redundant Arrays of Inexpensive Disks RAID。

提供IO能力：通过磁盘并行读写，部分卡添加RAID内存（提供额外电源）
提高耐用性：通过磁盘冗余来实现

RAID实现方式：
- 硬件实现方式
	- 外接式磁盘阵列：通过扩展卡提供适配能力，控制器Controller接PCI或者PCIE
	- 内接式RAID：主板集成RAID控制器
- 软件实现方式
	- Software RAID：了解即可，不建议使用


RAID解决的问题；

- 合并
- 速度
- 损坏

## RAID级别

级别level：仅代表磁盘组织方式不同，没有上下之分；

常用级别：
- RAID-0：0，条带卷，strip
- RAID-1：1，镜像卷，mirror
- RAID-5
- RAID10
- RAID50
- JBOD



### RAID0：条带

耐用性降低，适合非关键性数据

- 读写性能提升
- 空间利用率：nS（同大小）、n*min(S1,S2...)不同大小
- 冗余能力（容错能力）: 无
- 至少2块盘
- 数据安全性降低
- 成本低

### RAID1：镜像

- 性能表现：写性能略微下降（有快慢，取决于慢的），读性能提升
- 空间利用率：1/2（同大小），1*min（S1,S2...）
- 冗余能力：有
- 至少2块盘
- 数据安全性提高
- 成本高

2
3
### RAID4

允许坏一块盘。

一个盘做集中校验盘，有性能瓶颈。

### RAID5

轮流做校验盘

保存奇偶校验和，用于节省空间，恢复数据。

妥协方案：为了成本，对数据安全性进行妥协

- 性能表现：读，写提升
- 冗余能力：有
- 空间利用率：(n-1)/n
- 至少需要3块
- 数据安全性提高

### RAID6

- 读写性能提升
- 可用空间：（N-2）*min(S1,S2...)
- 有容错能力
- 最少需要4块

### RAID-10 最常用

先做RAID1再做RAID0，两个一组每一组是镜像卷，再做RAID0

最推荐的RAID方案，并且增加热备盘（平时不工作，故障时会自动顶替）。另外还需要运维工程师常常备份。

此外还有异地备份的容灾技术。

- 性能表现：读、写提升
- 冗余能力：有, 每组镜像最多坏一块
- 空间利用率：1/2
- 至少需要4块

案例：创建RAID10

```shell
# 首先由四块硬盘,用mdadm创建
# mdadm -Cv /dev/md0 -n 4 -l 10 /dev/sdb /dev/sdc/ dev/sdd/ /dev/sde
mdadm -Cv /dev/md0 -n 4 -l 10 /dev/sd[b-e]
# 查看基本信息
mdadm -Q /dev/md0
# mdadm -D /dev/md0 查看详细信息details，看是否同步好

```

### RAID-01:

先分为两组，每组做成条带0，再做镜像1。

- 性能表现：读、写提升
- 冗余能力：有
- 空间利用率：1/2
- 至少需要4块

### RAID-50:

先RAID5再做RAID0

- 性能表现：读、写提升
- 冗余能力：有
- 空间利用率：(n-2)/n
- 至少需要6块

### JBOD:
> Just a Bunch Of Disk2
> 将多块磁盘的空间合并为一个大的连续空间使用

- 性能表现：无提升
- 冗余能力：无
- 空间利用率：100%
- 可用空间：sum(S1,S2...)
- 至少需要2块

逻辑RIAD：
/dev/md0
/dev/md1

## mdadm 管理磁盘阵列

> CentOS 6上的软RAID实现，结合内核中的md模块 (multi devices 多设备)，将多个硬盘设备组成一个设备，并通过软件实现。

> 模式化工具

md adminstration，将任何块设备做成RAID

mdadm [mode] raiddevice [options] component-devices
- raiddevice: /dev/md#
- component-device: 任意块设备

支持的RAID级别：LINEAR(JBOD)，RAID0, RAID1, RAID5, RAID10

模式：
- 创建模式：-C
- 装配模式：-A
- 监控模式：-F
- 管理模式：-f, -r, -a

### 创建模式

-C: 创建模式 create

专用选项：

- -v 过程可视
- -n #: 设备个数为#
- -l #: 级别为#
- -x #: 指定空闲盘(热备盘)个数为#
- -c CHUNK_SIZE: CHUNK大小, 2^n，默认为64K
- -a {yes|no}: 是否自动为其创建设备文件

### 管理模式

- -f --fail 标记指定磁盘为损坏
- -r --remove 移除磁盘
- -a --add 添加磁盘

替换热备盘
```sh
# 使失效
mdadm -f /dev/md0 /dev/sdc
# 查看，等待热备盘同步完成
mdadm -D /dev/md0
# 移除
mdadm -r /dev/md0 /dev/sdc
# 查看
mdadm -D /dev/md0
# 添加硬盘，卸载原来RAID组，并查看
umount /dev/md0
df -h
# 添加热备盘
mdadm /dev/md0 -a /dev/sdc
# 挂载,并查看
mouont -a
df -h
```

### 监控模式

-F

### 增长模式

-G

### 装配模式

-A

### 查看RAID阵列的详细信息

mdadm -D /dev/md#

	--detail

cat /proc/mdstat

watch -n1 'mdadm -D /dev/md#'


### 停止阵列

mdadm -S /dev/md#

	--stop


创建一个空间大小为10G的RAID5设备；其chuck大小为32k；要求此设备开机时可以自动挂载至/backup目录；
```sh
# 准备分区，分区类型设为fd
# 创建
mdadm -C /dev/md0 -a yes -n 3 -x 1 -l 5 /dev/sda{7,8,9,10}
# 格式化
mke2fs -t ext4 /dev/md0
# 挂载
mount /dev/md0 /mydata
# 查看挂载
mount
# 自动挂载（使用UUID挂载，应为/dev/md0重启会变化）
vim /etc/fstab
```




RAID0
	2G:
		4: 512MB
		2: 1G

RAID1
	2G
		2：2G
		

将当前RAID信息保存至配置文件，以便以后进行装配：
mdamd -D --scan > /etc/mdadm.conf


RAID5: 
	2G: 3, 1G

归档
--xattrs