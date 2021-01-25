# btrfs文件系统
技术预览版

Btrfs （B-tree，Butter FS，Better FS）
- 基于GPL
- 开发者Oracle, 2007
- 目的是取代ext3/ext4（事实上的标准）
- 支持大文件


## 核心特性：
- 多物理卷支持，brtfs可由多个物理卷组成，可挂载后直接使用，也可以在内部创建子卷。
- 支持RAID，条带，mirror等功能，以联机添加、移除、修改
- 支持写时复制更新机制（CoW）:复制、更新及替换指针，而非就地更新
- 数据及元数据校验码
- 子卷：sub_volume
- 支持快照，支持累积快照，单文件快照，增量备份效果
- 透明压缩

## 文件系统管理命令

mkfs.btrfs 

CentOS 7 或更新版本debian ubuntu才有此功能。

- -L|--label Name：指定卷标
- -m|--metadata TYPE：指定元数据组成方式 raid0,raid1,raid5,raid6,raid10,single,dup, 默认single
- -d|--data TYPE：指定数据组成方式 raid0,raid1,raid5,raid6,raid10,single,dup
- -O FEATURE : 指定特性
    - -O list all ：列出支持的所有feature


子命令：
- filesystem
- device
- balance
- subvolume

btrfs filesystem show 属性查看

mount -t btrfs /dev/sdb MOUNT_POINT  挂载文件系统，挂载时选择一个设备即可

mount -o compress={lzo|zlib} DEVICE MOUNT_POINT 透明压缩机制

btrfs filesystem resize +10G /mydata 调整大小

btrfs filesystem resize max /mydata 调整大小至最大

btrfs filesystem df /mydata 查看大小

df -lh

btrfs device add /dev/sdd /mydata 增加硬盘

btrfs balance start /mydata 启用balance

btrfs balance status /mydata 在balance的过程中查看

btrfs device delete /dev/sdb 移除设备，无需先移动数据，系统自动进行。

btrfs balance start -mconvert=raid5 /mydata 修改数据或者元数据raid级别

btrfs subvolume list /mydata 查看子卷

btrfs subvolume create /mydata/logs 创建子卷

mount -o subvol=logs /dev/sdb /mnt 只挂载子卷,先卸载父卷umount /mydata

btrfs subvolume show /mnt 查看子卷信息

btrfs subvolume delete /mydata/logs 删除子卷

btrfs subvolume snapshot /mydata/logs /mydata/logs_snapshot 创建快照卷

btrfs subvolume delete /mydata/logs_snapshot 删除快照卷

cp --reflink grub2.cfg  grub2.cfg_snapshot 对单个文件创建快照（写时复制特性）


btrfs-convert /dev/sdd1 将ext转换为btrfs，需要先卸载umount /mnt并进行检查fsck -f /dev/sdd1

btrfs-convert -r /dev/sdd1 转化为原格式


systemctl set-default multi-user.target 关闭图形界面

```sh
# 创建
mkfs.btrfs -L mydata /dev/sdb /dev/sdc
# 查看
btrfs filesystem show
btrfs filesystem show --mounted
btrfs filesystem show --all-devices
btrfs filesystem show /dev/sdb
btrfs filesystem show /dev/sdc # 任何一个设备都代表全局
btrfs filesystem show /mydata
man btrfs-filesystem # 查看btrfs filesytem 帮助
# 或查看
blkid /dev/sdb
blkid /dev/sdc
# 挂载
mount -t btrfs /dev/sdb /mydata # blkid识别就不需要-t btrfs，任何一个设备都代表全局
```
