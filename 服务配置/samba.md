# samba

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


