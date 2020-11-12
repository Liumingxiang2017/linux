# VMware Workstation的使用

虚拟机：虚拟计算机

稍后安装操作系统，桥接网络/NAT，1核，1G，20G

## VMware支持三种类型的网络：NAT，Bridged，Host-only

- NAT 地址转换

- 虚拟网卡VMnet8 ，在虚拟路由下
- 系统的 VMWare NAT Service 服务就充当了虚拟路由器的作用，负责将虚拟机发到 VMnet8 的包进行地址转换之后发到实际的网络上，再将实际网络上返回的包进行地址转换后通过 VMnet8 发送给虚拟机。
- VMWare DHCP Service 负责为虚拟机提供 DHCP 服务。
- 内可以访问外，虚拟路由做地址转换；外不可以访问内，没有地址转换。有路由器，就有子网。虚拟机内的linux系统和宿主机不在一个网段。

vmnet8网卡 和 linux虚拟机在一个网段。虚拟网络编辑器可以修改子网IP网段。但vnmet8和linux虚拟机必须在一个网段，才能使得虚拟机linux和宿主windows通信。


- Bridged 桥接

- 人数众多时，IP地址不够用。

- 这种方式下，虚拟机就像一台真正的计算机一样，直接连接到实际的网络上，与宿主机同在一个网段。192.168.0.1/24 如果Vmware用桥接，只有254个地址可用，人多就不够用了。

Host-only 仅主机

- 几乎没用

- 这种方式下，虚拟机的网卡连接到宿主的 VMnet1 上，但系统并不为虚拟机提供任何路由服务，因此虚拟机只能和宿主机进行通信，而不能连接到实际网络上。


网络检查

1. 检查windows的NAT service和DHCP service是否开启
2. 检查vmware网络编辑器NAT模式的默认网关和子网掩码

网络设置
1. 设置网卡为nat模式
2. 确保windows下的服务已开启（dhcp，net服务）
3. 编辑文件 vim /etc/sysconfig/network-scripts/ifcfg-eth0
4. ONBOOT=yes
5. 设置IP
```SHELL
# 以下是需要改动行
BOOTPROTO="static"
IPADDR=192.168.n.3 
# 192.168.n.1不能用，因为是vmnet8网口的地址
NETMASK=255.255.255.0 
# 即24位，如果需要改，需要改网络编辑器
GATEWAY=196.168.n.2
#网关地址
```

more /etc/inittab
- int 0 关机 shutdown now
- int 1 单用户模式
- int 2 多用户模式，无桌面
- int 4 预留
- int 3 多用户模式
- int 5 X11 带桌面的，完整版默认是5，可以改成3
- int 6 重启 reboot

