# U-Boot

## 编译U-Boot

1. 源文件 tar zxvf uboot.tar.gz
2. cd uboot, make xx_config 开发板配置，需找对应开发板文件
3. make ARCH=arm CROSS_COMPILE=arm-linux-  编译过程2分钟左右，arm-linux-前缀即可，arm-linux-gcc arm-linux-ld
4. 编译完成生成的uboot.bin就是烧写到开发板中的二进制镜像
5. U-boot烧写：安装辅助程序（SD或Nor）——USB下载线（U-Boot）——>开发板的Nand Flash

## U-Boot命令详解
### 帮助命令
尽管UBOOT提供了丰富的命令集，但不同的开发板所支持的命令却不一样（可配置），help 命令可用于察看当前单板所支持的命令。

help: print online help

### 环境变量相关命令

#### printenv 缩写 print

print ipaddr 单独打印

#### setenv 添加、修改、删除环境变量，
在内存中，需要保存。

setenv name value : add/modify environment variable 'name' to 'value'

set name : delete environment variable 'name'

#### saveenv 保存环境变量

将当前定义的所有变量及其值存入flash中

### 程序下载命令
uboot支持网络、usb、串口（速度太慢，大约是usb的十分之一）

tftp通过网络下载文件，远程电脑安装tftp服务器，开发板上安装tftp客户端

tftp服务器

vi /etc/xinetd.d/tftp 修改配置文件
diable =no
server_args = -s /tftpboot/  

chmod 777 ./ -R 修改/tftpboot目录的所有权

/etc/init.d/xinetd restart 重启服务
netstat -a | grep tftp 查看服务是否开启


注意：使用tftp，需要先配置好网络

setenv ethaddr 网卡mac地址（如果已有则无需设置）
setenv ipaddr IP开发板ip地址
setenv serverip IP tftp服务器地址
ping IP 检查网络通断

关闭防火墙 /etc/init.d/iptables stop; setenforce 0 临时关闭selinux模式

范例：tftp 0xc0008000 uImage.bin

把tftp服务器上的uImage.bin下载到0xc0008000

### 内存操作命令
#### md

md 显示内存区的内容，采用十六进制和ASCII码两种形式来显示存储单元的内容。 这条命令还可以采用长度标识码 .l, .w 和.b

md[.b, .w, ,l] address

范例: md.w 100000
#### mm
mm: memory modify 修改内存
范例：mm c0000000

### Flash操作命令

#### 擦除nand flash

nand erase 起始地址start 长度len

擦除start处开始的，长度为len的区域

范例：nand erase 0x400000 0x500000

#### 写/读 nand fash

nand write 内存起始地址 flash起始地址 长度len

将内存起始地址处，长度为len的数据，写入到flash起始地址处。

范例：nand write c0008000 400000 500000


nand read 内存起始地址 flash起始地址 长度len

将flash起始地址处，长度为len的数据，写入到flash起始地址处。

范例：nand read c0008000 400000 500000

### 程序执行命令

bootm {addr} {arg} 执行固定格式的2禁止程序

bootm c0008000 启动boot程序

### 设置自动启动
设置bootcmd环境变量

1. 设置从nand flash自动启动 setenv bootcmd nand read c0008000 400000 500000 \; bootm c0008000
2. 设置自动下载内核到内存后启动 setenv bootcmd tftp c0008000 uImage.bin \; bootm c0008000


## U—Boot 使用方法

不同开发板不同处：

1. 配置 U-Boot
- TQ210: make TQ210_config
- Smart210: make smart210_config
- OK210: make forlinx_linux_config
- OK6410: make forlinx_nand_ram256_config
- Tiny6410: make tiny6410_config
- TQ2440: make TQ2440_config
- Mini2440: make mini2440_config
2. 下载与运行
- TQ210: tftp 0xc0008000 uImage
- Smart210: tftp 0x20000000 uImage
- OK210: tftp 0xc0008000 uImage
- OK6410: tftp 0xc0008000 uImage
- Tiny6410: tftp 0xc0008000 uImage
- TQ2440: tftp 0x31000000
- Mini2440: tftp 0x31000000 uImage 