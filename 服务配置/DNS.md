# DNS

ip与域名解析

通过本地/etc/hosts文件可以进行解析

ipaddr 域名

```shell
rpm -qa | grep bind 
rpm -ql bind | more
# 在/var/named目录下放置的是配置文件
# /etc/rc.d/init.d/named 说明是Systemv
rpm -ql bind-chroot
# 根变成/var/named/chroot,配置文件在/var/named/chroot/etc/named/
# 必须安装的包：bind bind-utils bin-chroot bin-libs system-config-bind（可选,还有配置文件模板）
service named start
cp /usr/share/system-config-bind/profiles/default/named.conf /var/named/chroot/etc/named/
```