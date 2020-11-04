# Git教程

## Git简介

Git是什么？

Git是目前世界上最先进的**分布式版本控制系统**（没有之一）

什么是版本控制系统？

| 版本 | 文件名      | 用户 | 说明                   | 日期       |
| - | ----------- | ---- | ---------------------- | ---------- |
| 1    | service.doc | 张三 | 删除了软件服务条款5    | 7/12 10:38 |
| 2    | service.doc | 张三 | 增加了License人数限制  | 7/12 18:09 |
| 3    | service.doc | 李四 | 财务部门调整了合同金额 | 7/13 9:51  |
| 4    | service.doc | 张三 | 延长了免费升级周期     | 7/14 15:17 |

### Git的诞生

linus在1991年创建了开源的Linux，从此Linux系统不断发展，已经成为最大的服务器系统软件。

Linux反对SVS和SVN这些集中式的版本控制系统，不但速度慢，而且必须联网才能使用。

Linus选择了一个商业的版本控制系统BitKeeper，BitKeeper的东家BItMover公司处于人道主义精神授权Linux社区免费使用这个版本控制系统。

2005年，开发Samba的Andrew试图破解BitKeeper协议。

BitMover公司要收回Linux社区的免费使用权利。

Linus花了两周时间自己用C写了一个分布式版本控制系统，就是Git！

2008年，GitHub网站上线，它为开源项目免费提供Git存储，包括jQuery，PHP, Ruby等

###  集中式VS分布式

#### 集中式版本控制系统

版本库是集中存放在中央处理器的。最大问题在于必须联网才能工作。

#### 分布式版本控制系统

分布式版本控制系统没有“中央服务器”，每个人的电脑都是一个完整的版本库，这样工作时就不需要联网了。

分布式版本控制系统通常也有一台充当“中央服务器”的电脑，但是这个服务器的作用仅仅是用来方便“交换”大家的修改。

Git极其强大的分支管理，把SVN等远远抛在后面。

CVS作为最早开源而且免费的集中式版本控制系统，由于自身设计问题，会造成提交文件不完整，版本库莫名其妙损坏的情况。

SVN修正了CVS的一些稳定性问题，是目前用的做多的集中式版本控制系统。

收费的集中式版本控制系统，IBM的ClearCase，特点是安装比Windows还大，运行比蜗牛还慢，用ClearCase的一般是世界500强，特点是财大气粗，或者人傻钱多。

微软自己也有集中式版本控制系统VSS，集成在Visual Studio中，反人类设计。

分布式版本控系统还有BitKeeper，Mercurial，Bazaar。

## 安装Git

### 在Linux上安装Git

首先，你可以试着输入`git`，看看系统有没有安装Git：

```shell
$ git
The program 'git' is currently not installed. You can install it by typing:
sudo apt-get install git
```

如果你碰巧用Debian或Ubuntu Linux，通过一条`sudo apt-get install git`就可以直接完成Git的安装，非常简单。 

如果是其他Linux版本，可以直接通过**源码安装**。先从Git官网下载源码，然后解压，依次输入：`./config`，`make`，`sudo make install`这几个命令安装就好了。

### 在Mac OS X上安装Git

一是安装homebrew，然后通过homebrew安装Git，具体方法请参考homebrew的文档：<http://brew.sh/>。

第二种方法更简单，也是推荐的方法，就是直接从AppStore安装Xcode，Xcode集成了Git，不过默认没有安装，你需要运行Xcode，选择菜单“Xcode”->“Preferences”，在弹出窗口中找到“Downloads”，选择“Command Line Tools”，点“Install”就可以完成安装了。


Xcode是Apple官方IDE，功能非常强大，是开发Mac和iOS App的必选装备！

### 在Windows上安装Git

在Windows上使用Git，可以从Git官网直接[下载安装程序](https://git-scm.com/downloads)，（网速慢的同学请移步[国内镜像](https://pan.baidu.com/s/1kU5OCOB#list/path=%2Fpub%2Fgit)），然后按默认选项安装即可。

安装完成后，在开始菜单里找到“Git”->“Git Bash”，蹦出一个类似命令行窗口的东西，就说明Git安装成功！


安装完成后，还需要最后一步设置，在命令行输入：

```
$ git config --global user.name "Your Name"
$ git config --global user.email "email@example.com"
```

因为Git是分布式版本控制系统，所以，每个机器都必须自报家门：你的名字和Email地址。

注意`git config`命令的`--global`参数，用了这个参数，表示你这台机器上所有的Git仓库都会使用这个配置。
