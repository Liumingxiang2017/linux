# samba 文件服务器

## 入门概述

### windows网上邻居

#### 工作原理

通过SMB协议共享传输文件，具有自己的主机名称解析系统(wins)。

SMB (Server Messsage Block)/CIFS (Common Internet File System)是基于Netbios协议的，所以不能跨越子网通信。

认证模式

工作组模式：用户账号密码存放在每台主机上，通过对方主机的认证授权。
域服务器模式：用户账号集中存放在域服务器，每台主机通过域服务器认证授权。

跟linux共享必须安装TCP/IP

直接输入\\server\sharename

#### 设置共享文件夹

1. 文件夹右键属性
2. 共享标签卡---高级共享---勾选共享此文件夹

#### 设置可访问用户

默认所有人都可以访问，删除everyone，然后指定用户权限。

1. 文件夹右键属性
2. 共享标签卡---高级共享---权限
3. 删除everyone---添加用户并指定权限

### Linux访问网上邻居

- 需要samba客户端
- 挂载

```shell
# 方式1
mount -t smbfs //server/sharename /localdir
# 方式2
smbmount //server/sharename /localname
```

- 使用smbclient

```shell
smbclient //server/sharename -U name%passwd
```

## samba工具集

samba软件与工具介绍

samba为windows提供共享

安全级别

用户账号与认证

samba项目开发 http://www.samba.org

相关软件包

samba 服务器软件包
samba-client 客户端工具
samba-common 通用工具和库

## 安装Samba软件包

安装samba软件包

    rpm -ivh --aid samba*.rpm

检查软件包内容

    rpm -ql samba | more
    rpm -ql samba-common | more
    rpm -ql samba-client | more

    启动脚本 /etc/rc.d/init.d/smb

## Samba客户端工具

smbtree

作用：显示局域网中所有共享主机和目录列表

用法：smbtree [-b] [-D] [-U username%password]

nmblookup

作用：显示一台主机的netbios主机名

smbclient

作用：显示/登录共享局域网中的共享文件夹

用法：

    smbclient -L host
    smbclient //HOST/SHARE

smbtar

作用：远程备份网上邻居中的文件
用法：

    smbtar -s SERVER -u USER -p PASSWORD -x SHARENAME -t output
    
    smbtar -s win2000 -u redhat -p redhat -x lmxshare -t lmxshare.tar

smbmount

作用：挂载远程目录，之后类似于磁盘映射

smbmount //host/share /mnt -o username=USERNAME%PASSWORD

## Samba服务器配置

修改配置文件/etc/samba/smb.conf

    workgroup = WORKGROUP
    security = share
    [docs]
        path = /usr/share/doc
        comment = share documents
        public = yes

重启smb服务器

    service smb restart
    chkconfig smb on

测试

    smbclient -L localhost

