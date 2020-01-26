# LVM逻辑卷管理器

:| 解决问题：动态调整分区大小（扩容）,不再考虑底层硬件设备

## 常用LVM部署命令

功能|物理卷|卷组管理|逻辑卷
:-:|:-:|:-:|:-:
扫描|pvscan|vgscan|lvscan
建立|pvcreate|vgcreate|lvcreate
显示|pvdisplay|vgdisplay|lvdisplay
删除|pvremove|vgremove|lvremove
扩展|-|vgextend|lvextend
缩小|-|vgreduce|lvreduce

- pv操作：使设备支持LVM技术
- vg操作：合并成卷组
- lv操作：切割成逻辑卷

案例:创建

```shell
# 增加硬盘/dev/sdb /dev/sdc
# 使支持LVM
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

```shell
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

```shell
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

```shell
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

```shell
umount /mnt/lvm
df -h
vim /etc/fstab
lvremove /dev/vgName/lvName
vgremove vgName
pvremove /dev/sdb
lvdisplay
vgdisplay
pvdisplay
```


PE 单元，最小为4M。

LVM：
	扩展
	逻辑卷的缩减
	快照卷

10G, VG

vgcreate VG_NAME /PATH/TO/PV
	-s #: PE大小，默认为4MB

lvcreate -n LV_NAME -L #G VG_NAME


练习：创建一个由两个物理卷组成的大小为20G的卷组myvg，要求其PE大小为16M；而后在此卷组中创建一个大小为5G的逻辑卷lv1，此逻辑卷要能在开机后自动挂载至/users目录，且支持ACL功能；

缩减前面创建的逻辑卷lv1的大小至2G；

一、扩展逻辑卷；
lvextend
	-L [+]# /PATH/TO/LV

2G, +3G
5G	
	
resize2fs
	resize2fs -p /PATH/TO/LV


二、缩减逻辑卷；
注意：1、不能在线缩减，得先卸载；
	  2、确保缩减后的空间大小依然能存储原有的所有数据；
	  3、在缩减之前应该先强行检查文件，以确保文件系统处于一至性状态；
df -lh
umount 
e2fsck -f
	  	  
resize2fs 
	resize2fs /PATH/TO/PV 3G

lvreduce -L [-]# /PATH/TO/LV

重新挂载


三、快照卷
1、生命周期为整个数据时长；在这段时长内，数据的增长量不能超出快照卷大小；
2、快照卷应该是只读的；
3、跟原卷在同一卷组内；


lvcreate 
	-s
	-p r|w
	
lvcreate -L # -n SLV_NAME -p r /PATH/TO/LV
