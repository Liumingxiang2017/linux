# U-Boot

## 编译U-Boot
安装辅助程序（SD或Nor）——USB下载线（U-Boot）——>开发板的Nand Flash
## U-Boot命令详解
### 帮助命令
尽管UBOOT提供了丰富的命令集，但不同的开发板所支持的命令却不一样（可配置），help 命令可用于察看当前单板所支持的命令。

autoscr -run script from memory
base -print or set address offset
bdinfo -print Board Info structure
bootm -boot application image from memory

### 环境变量相关命令

### 程序下载命令
### 内存操作命令
### Flash操作命令
### 程序执行命令
### 设置自动启动

## U—Boot 使用方法

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