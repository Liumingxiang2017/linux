# LVM逻辑卷管理器

<!-- TOC -->

1. [LVM逻辑卷管理器](#lvm逻辑卷管理器)
    1. [常用LVM部署命令](#常用lvm部署命令)
    2. [PV管理工具：](#pv管理工具)
    3. [VG管理工具](#vg管理工具)
    4. [lv管理工具](#lv管理工具)
        1. [扩展逻辑卷lv](#扩展逻辑卷lv)
        2. [缩减逻辑卷](#缩减逻辑卷)
        3. [快照卷 snapshot](#快照卷-snapshot)

<!-- /TOC -->

> LVM: Logical Volume Manager, Version 2

主要特性：边界动态扩展和收缩；支持快照

解决问题：动态调整分区大小（扩容）,不再考虑底层硬件设备

相关内核模块dm（device mapper 设备映射）：将一个或多个底层块设备组织成一个逻辑设备的模块。

对应硬件文件
- /dev/dm-#
- /dev/mapper/VG_NAME-LV_NAME (符号链接文件)
- /dev/VG_NAME/LV_NAME (符号链接文件)

PE（Phsical Extent物理弹区）单元：由VG定义，最小为4M。
LE（Logical Extent逻辑弹区）：LV的单元

Note：CentOS 6 以下版本按需使用，CentOS 7开始使用的btrfs文件系统自身具备LVM功能，无需使用。

## 常用LVM部署命令

功能|pv物理卷|vg卷组管理|lv逻辑卷
:-:|:-:|:-:|:-:
扫描|pvscan|vgscan|lvscan
建立|pvcreate|vgcreate|lvcreate
显示|pvdisplay|vgdisplay|lvdisplay
简要显示|pvs|vgs|lvs
删除|pvremove|vgremove|lvremove
扩展|-|vgextend|lvextend
缩小|-|vgreduce|lvreduce

- pv操作：使设备支持LVM技术
- vg操作：合并成卷组
- lv操作：切割成逻辑卷

NOTE: 创建pv前：分区文件系统类型为8e（Linux LVM）

## PV管理工具：
- pvs：简要pv信息显示
- pvdisplay: 显示pv的详细信息
- pvcreate /dev/DEVICE... ：创建pv，可同时创建多个
- pvremove /dev/DEVICE

## VG管理工具
- vgs
- vgdisplay
- vgcreate VG_NAME /PATH/TO/PV
	- -s #: PE大小，默认为4MB
- vgextend VG_NAME /PATH/TO/PV
- vgreduce VG_NAME /PATH/TO/PV
	- 先做pvmove /PATH/TO/PV 移除数据
- vgremove VG_NAME

## lv管理工具
- lvs
- lvdisplay
- lvcreate -n LV_NAME -L #[mMgGtT] VG_NAME
	- -n|--name : 指定名称
	- -L|--size : 指定大小
- lvremove /dev/VG_NAME/LV_NAME
	
### 扩展逻辑卷lv
步骤：先修改lv边界，再修改文件系统边界
1. lvextend -L [+]#[mMgGtT] /dev/VG_NAME/LV_NAME 修改lv边界
	- +表示增加，无+表示至
2. resize2fs /dev/VG_NAME/LV_NAME 只适用于ext系列，修改文件系统边界
	- resize2fs -p /PATH/TO/LV ：-p表示显示百分比

### 缩减逻辑卷

注意：
- 不能在线缩减，得先卸载；
- 确保缩减后的空间大小依然能存储原有的所有数据；
- 在缩减之前应该先强行检查文件，以确保文件系统处于一至性状态；


步骤：

df -lh
1. umount  /dev/VG_NAME/LV_NAME 卸载逻辑卷
2. e2fsck -f /dev/VG_NAME/LV_NAME 文件系统强制检测修复
3. resize2fs /dev/VG_NAME/LV_NAME #[mMgGtT] 指定文件系统缩小后的大小
4. lvreduce -L [-]#[mMgGtT] /dev/VG_NAME/LV_NAME 指定缩减的lv边界
5. mount 重新挂载


### 快照卷 snapshot
访问原卷文件另一条路径，有监视器监视原卷元数据，元数据变化会把对应变化的文件复制一份到快照卷。
- 元数据不变，访问原卷
- 元数据变化，访问快照卷备份

注意：
- 生命周期为整个数据时长；在这段时长内，数据的增长量不能超出快照卷大小；
- 快照卷应该是只读的；
- 必须跟原卷在同一卷组内；


lvcreate -L #[mMgGtT] -p r -s -n snapshot_lv_name original_lv_name
- -s|--snapshot 
- -n|--name：设置名称
- -p r|w：快照卷一般设置只读
	

案例:创建

```sh
# 物理卷可以创建在磁盘、分区、RAID等块设备
# 对于分区，分区文件系统类型为8e（Linux LVM）
# 增加硬盘/dev/sdb /dev/sdc，使支持LVM
pvcreate /dev/sdb /dev/sdc
# 合并并查看
vgcreate vgName /dev/sd[b-c]
vgdisplay
# 切割并查看
# -l 后接PE个数，如果是-L则后接容量
lvcreate -n lvName -l 100 vgName
lvdisplay
# 寻找设备,/dev/卷组名/逻辑卷名
# 格式化并挂载,注意xfs不支持LVM，其本身可以扩容使用命令xfs_growfs
mkdir /mnt/lvm
mkfs.ext4 /dev/vgName/lvName
mount /dev/vgName/lvName /mnt/lvm
df -h
vim /etc/fstab
# /dev/vgName/lvName /mnt/lvm ext4 defaults 0 0
```

案例：扩容

```sh
umount /mnt/lvm
df -h
# 扩容 -L表示扩容到
lvextend -L 800M /dev/vgName/lvName
# 扫描文件系统是否损坏
e2fsck -f /dev/vgName/lvName
# 通知系统内核
resize2fs /dev/vgName/lvName
# 挂载
mount -a
df -h
```

案例：缩小

```sh
umount /mnt/lvm
df -h
# 扫描文件系统是否损坏
e2fsck -f /dev/vgName/lvName
# 通知系统内核，要缩小到300M
resize2fs /dev/vgName/lvName 300M
# 缩小
lvreduce -L 300M /dev/vgName/lvName
# 挂载
mount -a
df -h
```

案例：快照（备份）

```sh
lvcreate -L 300M -s -n snapName /dev/vgName/lvName
# 快照只能还原一次,还原后会删除快照
rm -rf /mnt/lvm/*
umount /mnt/lvm
# 还原
lvconvert --merge /dev/vgName/snapName
mount -a
df -h 
ls /mnt/lvm
```

案例：删除

```sh
# 卸载
umount /mnt/lvm
df -h
vim /etc/fstab
# 删除lv
lvremove /dev/vgName/lvName
# 删除vg
vgremove vgName
# 删除pv
pvremove /dev/sdb
lvdisplay
vgdisplay
pvdisplay

```


练习：创建一个由两个物理卷组成的大小为20G的卷组myvg，要求其PE大小为16M；而后在此卷组中创建一个大小为5G的逻辑卷lv1，此逻辑卷要能在开机后自动挂载至/users目录，且支持ACL功能；

缩减前面创建的逻辑卷lv1的大小至2G；