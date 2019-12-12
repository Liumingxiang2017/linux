# 使用vsftpd传输文件

## 查看软件包

- 查看软件是否安装：rpm -qa | grep ftp
  - vsftpd
  - ftpd
  - lftp

- 查看软件内容：rpm -ql vsftpd | more

## 启动服务

- service vsftpd start

下载文件：get filename

上传文件：put filename

退出： bye

ftp允许linux真实用户上传、下载、创建，并访问整个文件系统。身份验证采用真实系统用户密码。

将真实用户的/etc/passwd中/bin/bash改成/sbin/nologin，用户就不可登录了。

### 配置文件

anonymous_enable=YES，local_enable=YES 默认用户ftp无需密码登录，目录为/var/ftp/，只能下载不能上传。匿名用户已经使用了chroot功能。

chroot_list_enable=YES, chroot_list_file=/etc/vsftpd/chroot_list取消注释，重启服务。编辑/etc/vsftpd/chroot_list 每个用户名占用一行，可以改变根。

/etc/vsftpd/ftpusers 不允许通过ftp登录的用户，即黑名单，默认不允许root登录ftp因为其权限太大!

/etc/vsftpd/userlist 默认也是为黑名单，即当/etc/vsftpd/vsftpd.conf中的userlist_enable=YES时为黑名单，反之为白名单。