# DOS
## 创建目录md命令
chdir 简写为cd (chage directory)

cd .. 切换到上一层目录 
同linux下的cd

cd \ 切换到根目录

mkdir 简写为md （make directory）

md /?可以查看md命令的相关帮助

md \directory1\directory2

## Ctrl+c 中断命令

## 删除目录rd命令
rd (remove directory)
类似linux下的 rmdir

功能：删除空子目录

## 列出目录dir命令 
dir /a 列出当前目录所有文件（包含隐藏文件及系统文件）
类似linux下的 ls

## 复制文件cp 
copy 文件 目录
copy 文件 目录 /y   不会提示是否覆盖
copy 原文件名 新文件名    对当前文件下的文件进行复制并重命名
copy 原文件名 目录\新文件名

## 删除文件del
del 文件    删除文件
del 文件夹    删除指定目录下所有文件（不包含目录）
类似linux下的rm

## 重命名ren
ren （rename） ren [drive:][path]filename1 filename2

## 移动文件并重命名文件和目录move
move [/Y | /-Y][dirve:][path]dirname1 dirname2

## type 查看文本文件内容 
查看使用方法 type /?
TYPE [drive:][path]filename

## attrib 显示或更改文件属性
查看使用方法 attrib /?

## ipconfig 查看网络信息
ipconfig    显示信息
ipconfig /all    显示详细信息
ipconfig /renew     更新所有适配器
类似 linux 下的 ifconfig 命令

## msconfig 调出系统配置窗口

## netstat 查看端口
端口分为: 
物理端口，比如 ADSL、Modem、 集线器、 交换机、 路由器用于连接其他网络设备的接口，如RJ-45端口、SC端口等等 
逻辑端基，一般指TCPIP端口

端口作用：
一台拥有IP地址的主机可以提供许多服务，比如Web服务、FTP服务、SMTP服务等，这些服务完全可以通过1个IP地址来实现。那么，主机是怎样区分不同的网络服务呢？显然不能只靠IP地址，因为IP 地址与网络服务的关系是一对多的关系。实际上是通过“IP地址+端口号”来区分不同的服务的。

linux 下，也是使用netstat

## label 创建、更改或删除磁盘的卷标。

LABEL [drive:][label]

  drive:          指定驱动器号。
  label           指定卷标。

## net user 查看添加删除用户
类似linux cat /etc/passwd; useradd; userdel

## net localgroup 查看添加删除组用户
net localgroup administrator user1 /add   把user1 添加到 administrator  组
net localgroup administrator user1 /delete   把user1 从 administrator  组删除

## net share 查看共享文件

## ftp 
ftp 192.168.129.128
get 下载
put 上传

## defrag 磁盘碎片整理程序

## format 格式化

## telnet

## title 设置命令提示窗口的窗口标题 和 color 设置控制台前景和背景颜色

