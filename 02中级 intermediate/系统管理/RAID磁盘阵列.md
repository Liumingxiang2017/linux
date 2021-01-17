# RAID磁盘阵列

伯克利大学1988年提出。

RAID解决的问题

- 合并
- 速度
- 损坏

## RAID方案

级别：仅代表磁盘组织方式不同，没有上下之分；

### RAID0：条带

- 性能提升: 读，写
- 冗余能力（容错能力）: 无
- 空间利用率：nS
- 至少2块盘
- 数据安全性降低
- 成本低

### RAID1：镜像

- 性能表现：写性能下降，读性能提升
- 冗余能力：有
- 空间利用率：1/2
- 至少2块盘
- 数据安全性提高
- 成本高

2
3
4

### RAID5

保存奇偶校验和，用于节省空间，恢复数据。

妥协方案：为了成本，对数据安全性进行妥协

- 性能表现：读，写提升
- 冗余能力：有
- 空间利用率：(n-1)/n
- 至少需要3块
- 数据安全性提高

### RAID10

最推荐的RAID方案，并且增加热备盘（平时不工作，故障时会自动顶替）。另外还需要运维工程师常常备份。

此外还有异地备份的容灾技术。

- 性能表现：读、写提升
- 冗余能力：有
- 空间利用率：1/2
- 至少需要4块

#### 案例：创建RAID10

```shell
# 首先由四块硬盘,用mdadm创建
# mdadm -Cv /dev/md0 -n 4 -l 10 /dev/sdb /dev/sdc/ dev/sdd/ /dev/sde
mdadm -Cv /dev/md0 -n 4 -l 10 /dev/sd[b-e]
# 查看基本信息
mdadm -Q /dev/md0
# mdadm -D /dev/md0 查看详细信息details，看是否同步好

```

01:
	性能表现：读、写提升
	冗余能力：有
	空间利用率：1/2
	至少需要4块
50:
	性能表现：读、写提升
	冗余能力：有
	空间利用率：(n-2)/n
    至少需要6块
jbod:
	性能表现：无提升
	冗余能力：无
	空间利用率：100%
	至少需要2块

逻辑RIAD：
/dev/md0
/dev/md1

## mdadm 管理磁盘阵列

md adminstration，将任何块设备做成RAID

模式化的命令：

### 创建模式

-C 创建阵列卡

专用选项：

- -v 过程可视
- -n #: 设备个数为#
- -l #: 级别为#
- -x #: 指定空闲盘(热备盘)个数为#
- -c: CHUNK大小, 2^n，默认为64K
- -a {yes|no}: 是否自动为其创建设备文件

### 管理模式

- -f --fail 使失效
- -r --remove 
- -a --add

替换热备盘
```shell
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

### 停止阵列

mdadm -S /dev/md#

	--stop

创建一个空间大小为10G的RAID5设备；其chuck大小为32k；要求此设备开机时可以自动挂载至/backup目录；

RAID0
	2G:
		4: 512MB
		2: 1G

RAID1
	2G
		2：2G
		

		
watch: 周期性地执行指定命令，并以全屏方式显示结果
	-n #：指定周期长度，单位为秒，默认为2
格式： watch -n # 'COMMAND'
	
将当前RAID信息保存至配置文件，以便以后进行装配：
mdamd -D --scan > /etc/mdadm.conf


RAID5: 
	2G: 3, 1G

归档
--xattrs