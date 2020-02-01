# 使用LNMP架构部署动态网站环境

本章目录结构 [收起]

20.1 源码包程序
20.2 LNMP动态网站架构
20.2.1 配置Mysql服务
20.2.2 配置Nginx服务
20.2.3 配置php服务
20.3 搭建Discuz论坛
20.4 选购服务器主机
20.1 源码包程序

源码包：

1. 下载、解压
2. 编译，分析系统
3. 生成二进制程序
4. 安装

本书第1章中曾经讲到，在RPM（红帽软件包管理器）技术出现之前，Linux系统运维人员只能通过源码包的方式来安装各种服务程序，这是一件非常繁琐且极易消耗时间与耐心的事情；而且在安装、升级、卸载程序时还要考虑到与其他程序或函数库的相互依赖关系，这就要求运维人员不仅要掌握更多的Linux系统理论知识以及高超的实操技能，还需要有极好的耐心才能安装好一个源码软件包。考虑到本书的读者都是刚入门或准备入门的运维新人，因为本书在前面的章节中一直都是采用Yum软件仓库的方式来安装服务程序。但是，现在依然有很多软件程序只有源码包的形式，如果我们只会使用Yum软件仓库的方式来安装程序，则面对这些只有源码包的软件程序时，将充满无力感，要么需要等到第三方组织将这些软件程序编写成RPM软件包之后再行使用，要么就只能寻找相关软件程序的替代品了（而且替代软件还必须具备RPM软件包的形式）。由此可见，如果运维人员只会使用Yum软件仓库来安装服务程序，将会形成知识短板，对日后的运维工作带来不利。

本着不能让自己的读者在运维工作中吃亏的想法，刘遄老师接下来会详细讲解如何使用源码包的方式来安装服务程序。

其实，使用源码包来安装服务程序具有两个优势。

源码包的可移植性非常好，几乎可以在任何Linux系统中安装使用，而RPM软件包是针对特定系统和架构编写的指令集，必须严格地符合执行环境才能顺利安装（即只会去“生硬地”安装服务程序）。

使用源码包安装服务程序时会有一个编译过程，因此可以更好地适应安装主机的系统环境，运行效率和优化程度都会强于使用RPM软件包安装的服务程序。也就是说，可以将采用源码包安装服务程序的方式看作是针对系统的“量体裁衣”。

一般来讲，在安装软件时，如果能通过Yum软件仓库来安装，就用Yum方式；反之则去寻找合适的RPM软件包来安装；如果是在没有资源可用，那就只能使用源码包来安装了。

使用源码包安装服务程序的过程看似复杂，其实在归纳汇总后只需要4～5个步骤即可完成安装。刘遄老师接下来会对每一个步骤进行详解。

需要提前说明的是，在使用源码包安装程序时，会输出大量的过程信息，这些信息的意义并不大，因此本章会省略这部分输出信息而不作特殊备注，请大家在具体操作时以实际为准。

第1步：下载及解压源码包文件。为了方便在网络中传输，源码包文件通常会在归档后使用gzip或bzip2等格式进行压缩，因此一般会具有.tar.gz与.tar.bz2的后缀。要想使用源码包安装服务程序，必须先把里面的内容解压出来，然后再切换到源码包文件的目录中：

```shell
[root@linuxprobe ~]# tar xzvf FileName.tar.gz

[root@linuxprobe ~]# cd FileDirectory
```

第2步：编译源码包代码。在正式使用源码包安装服务程序之前，还需要使用编译脚本针对当前系统进行一系列的评估工作，包括对源码包文件、软件之间及函数库之间的依赖关系、编译器、汇编器及连接器进行检查。我们还可以根据需要来追加--prefix参数，以指定稍后源码包程序的安装路径，从而对服务程序的安装过程更加可控。当编译工作结束后，如果系统环境符合安装要求，一般会自动在当前目录下生成一个Makefile安装文件。

```shell
[root@linuxprobe ~]# ./configure --prefix=/usr/local/program
```

第3步：生成二进制安装程序。刚刚生成的Makefile文件中会保存有关系统环境、软件依赖关系和安装规则等内容，接下来便可以使用make命令来根据Makefile文件内容提供的合适规则编译生成出真正可供用户安装服务程序的二进制可执行文件了。

```shell
[root@linuxprobe ~]# make
```

第4步：运行二进制的服务程序安装包。由于不需要再检查系统环境，也不需要再编译代码，因此运行二进制的服务程序安装包应该是速度最快的步骤。如果在源码包编译阶段使用了--prefix参数，那么此时服务程序就会被安装到那个目录，如果没有自行使用参数定义目录的话，一般会被默认安装到/usr/local/bin目录中。

```shell
[root@linuxprobe ~]# make install
```

第5步：清理源码包临时文件。由于在安装服务程序的过程中进行了代码编译的工作，因此在安装后目录中会遗留下很多临时垃圾文件，本着尽量不要浪费磁盘存储空间的原则，可以使用make clean命令对临时文件进行彻底的清理工作。

```shell
[root@linuxprobe ~]# make clean
```

估计有读者会有疑问，为什么通常是安装一个服务程序，源码包的编译工作（configure）与生成二进制文件的工作（make）会使用这么长的时间，而采用RPM软件包安装就特别有效率呢？其实原因很简单，在RHCA认证的RH401考试中，会要求考生写一个RPM软件包。刘遄老师会在本书的进阶篇中讲到，其实RPM软件包就是把软件的源码包和一个针对特定系统、架构、环境编写的安装规定打包成一起的指令集，因此为了让用户都能使用这个软件包来安装程序，通常一个软件程序会发布多种格式的RPM软件包（例如i386、x86_64等架构）来让用户选择。而源码包的软件作者肯定希望自己的软件能够被安装到更多的系统上面，能够被更多的用户所了解、使用，因此便会在编译阶段（configure）来检查用户当前系统的情况，然后制定出一份可行的安装方案，所以会占用很多的系统资源，需要更长的等待时间。

20.2 LNMP动态网站架构

LNMP动态网站部署架构是一套由Linux + Nginx + MySQL + PHP组成的动态网站系统解决方案（其logo见图20-1）。LNMP中的字母L是Linux系统的意思，不仅可以是RHEL、CentOS、Fedora，还可以是Debian、Ubuntu等系统。本书的配套站点https://www.linuxprobe.com就是基于LNMP部署出来的，目前的运行一直很稳定，访问速度也很快。

图20-1  LNMP动态网站部署架构的Logo

在使用源码包安装服务程序之前，首先要让安装主机具备编译程序源码的环境，他需要具备C语言、C++语言、Perl语言的编译器，以及各种常见的编译支持函数库程序。因此请先配置妥当Yum软件仓库，然后把下面列出的这些软件包都统统安装上：

```shell
[root@linuxprobe ~]# yum install -y apr* autoconf automake bison bzip2 bzip2* compat* cpp curl curl-devel fontconfig fontconfig-devel freetype freetype* freetype-devel gcc gcc-c++ gd gettext gettext-devel glibc kernel kernel-headers keyutils keyutils-libs-devel krb5-devel libcom_err-devel libpng libpng-devel libjpeg* libsepol-devel libselinux-devel libstdc++-devel libtool* libgomp libxml2 libxml2-devel libXpm* libtiff libtiff* make mpfr ncurses* ntp openssl openssl-devel patch pcre-devel perl php-common php-gd policycoreutils telnet t1lib t1lib* nasm nasm* wget zlib-devel
Loaded plugins: langpacks, product-id, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
………………省略部分安装过程………………
Installing:
 apr                         x86_64       1.4.8-3.el7               rhel7       103 k
 apr-devel                   x86_64       1.4.8-3.el7               rhel7       188 k
 apr-util                    x86_64       1.5.2-6.el7               rhel7        92 k
 apr-util-devel              x86_64       1.5.2-6.el7               rhel7        76 k
 autoconf                    noarch       2.69-11.el7               rhel7       701 k
 automake                    noarch       1.13.4-3.el7              rhel7       679 k
 bison                       x86_64       2.7-4.el7                 rhel7       578 k
 bzip2-devel                 x86_64       1.0.6-12.el7              rhel7       218 k
 compat-dapl                 x86_64       1:1.2.19-3.el7            rhel7       109 k
 compat-db-headers           noarch       4.7.25-27.el7             rhel7        48 k
 compat-db47                 x86_64       4.7.25-27.el7             rhel7       795 k
 compat-gcc-44               x86_64       4.4.7-8.el7               rhel7        10 M
 compat-gcc-44-c++           x86_64       4.4.7-8.el7               rhel7       6.3 M
 compat-glibc                x86_64       1:2.12-4.el7              rhel7       1.2 M
 compat-glibc-headers        x86_64       1:2.12-4.el7              rhel7       452 k
 compat-libcap1              x86_64       1.10-7.el7                rhel7        19 k
 compat-libf2c-34            x86_64       3.4.6-32.el7              rhel7       155 k
 compat-libgfortran-41       x86_64       4.1.2-44.el7              rhel7       142 k
 compat-libtiff3             x86_64       3.9.4-11.el7              rhel7       135 k
 compat-openldap             x86_64       1:2.3.43-5.el7            rhel7       174 k
 cpp                         x86_64       4.8.2-16.el7              rhel7       5.9 M
 fontconfig-devel            x86_64       2.10.95-7.el7             rhel7       128 k
 freetype-devel              x86_64       2.4.11-9.el7              rhel7       355 k
 gcc                         x86_64       4.8.2-16.el7              rhel7        16 M
 gcc-c++                     x86_64       4.8.2-16.el7              rhel7       7.1 M
………………省略部分安装过程………………
Complete!
```

刘遄老师已经把安装LNMP动态网站部署架构所需的16个软件源码包和1个用于检查效果的论坛网站系统软件包上传到与本书配套的站点服务器上。大家可以在Windows系统中下载后通过ssh服务传送到打算部署LNMP动态网站架构的Linux服务器中，也可以直接在Linux服务器中使用wget命令下载这些源码包文件。根据第6章讲解的FHS协议，建议把要安装的软件包存放在/usr/local/src目录中：

```shell
[root@linuxprobe ~]# cd /usr/local/src
[root@linuxprobe src] # wget https://www.linuxprobe.com/Software/cmake-2.8.11.2.tar.gz
[root@linuxprobe src] # wget https://www.linuxprobe.com/Software/Discuz_X3.2_SC_GBK.zip
[root@linuxprobe src] # wget https://www.linuxprobe.com/Software/freetype-2.5.3.tar.gz
[root@linuxprobe src] # wget https://www.linuxprobe.com/Software/jpegsrc.v9a.tar.gz
[root@linuxprobe src] # wget https://www.linuxprobe.com/Software/libgd-2.1.0.tar.gz
[root@linuxprobe src] # wget https://www.linuxprobe.com/Software/libmcrypt-2.5.8.tar.gz
[root@linuxprobe src] # wget https://www.linuxprobe.com/Software/libpng-1.6.12.tar.gz
[root@linuxprobe src] # wget https://www.linuxprobe.com/Software/libvpx-v1.3.0.tar.bz2
[root@linuxprobe src] # wget https://www.linuxprobe.com/Software/mysql-5.6.19.tar.gz
[root@linuxprobe src] # wget https://www.linuxprobe.com/Software/nginx-1.6.0.tar.gz
[root@linuxprobe src] # wget https://www.linuxprobe.com/Software/openssl-1.0.1h.tar.gz
[root@linuxprobe src] # wget https://www.linuxprobe.com/Software/php-5.5.14.tar.gz
[root@linuxprobe src] # wget https://www.linuxprobe.com/Software/pcre-8.35.tar.gz
[root@linuxprobe src] # wget https://www.linuxprobe.com/Software/t1lib-5.1.2.tar.gz
[root@linuxprobe src] # wget https://www.linuxprobe.com/Software/tiff-4.0.3.tar.gz
[root@linuxprobe src] # wget https://www.linuxprobe.com/Software/yasm-1.2.0.tar.gz
[root@linuxprobe src] # wget https://www.linuxprobe.com/Software/zlib-1.2.8.tar.gz
[root@linuxprobe src]# ls
zlib-1.2.8.tar.gz       libmcrypt-2.5.8.tar.gz  pcre-8.35.tar.gz
cmake-2.8.11.2.tar.gz   libpng-1.6.12.tar.gz    php-5.5.14.tar.gz
Discuz_X3.2_SC_GBK.zip  libvpx-v1.3.0.tar.bz2   t1lib-5.1.2.tar.gz
freetype-2.5.3.tar.gz   mysql-5.6.19.tar.gz     tiff-4.0.3.tar.gz
jpegsrc.v9a.tar.gz      nginx-1.6.0.tar.gz      yasm-1.2.0.tar.gz
libgd-2.1.0.tar.gz      openssl-1.0.1h.tar.gz
```

CMake是Linux系统中一款常用的编译工具。要想通过源码包安装服务程序，就一定要严格遵守上面总结的安装步骤—下载及解压源码包文件、编译源码包代码、生成二进制安装程序、运行二进制的服务程序安装包。接下来在解压、编译各个软件包源码程序时，都会生成大量的输出信息，下文中将其省略，请读者以实际操作为准。

```shell
[root@linuxprobe src]# tar xzvf cmake-2.8.11.2.tar.gz
[root@linuxprobe src]# cd cmake-2.8.11.2/
[root@linuxprobe cmake-2.8.11.2]# ./configure
[root@linuxprobe cmake-2.8.11.2]# make 
[root@linuxprobe cmake-2.8.11.2]# make install
```

20.2.1 配置Mysql服务

本书在第18章讲解过MySQL和MariaDB数据库管理系统之间的因缘和特性，也狠狠地夸奖了MariaDB数据库，但是MySQL数据库当前依然是生产环境中最常使用的关系型数据库管理系统之一，坐拥极大的市场份额，并且已经通过十几年不断的发展向业界证明了自身的稳定性和安全性。另外，虽然第18章已经讲解了基本的数据库管理知识，但是为了进一步帮助大家夯实基础，本章依然在这里整合了MySQL数据库内容，使大家在温故的同时可以知新。

在使用Yum软件仓库安装服务程序时，系统会自动根据RPM软件包中的指令集完整软件配置等工作。但是一旦选择使用源码包的方式来安装，这一切就需要自己来完成了。针对MySQL数据库来讲，我们需要在系统中创建一个名为mysql的用户，专门用于负责运行MySQL数据库。请记得要把这类账户的Bash终端设置成nologin解释器，避免黑客通过该用户登录到服务器中，从而提高系统安全性。

[root@linuxprobe cmake-2.8.11.2]# cd ..
[root@linuxprobe src]# useradd mysql -s /sbin/nologin
创建一个用于保存MySQL数据库程序和数据库文件的目录，并把该目录的所有者和所属组身份修改为mysql。其中，/usr/local/mysql是用于保存MySQL数据库服务程序的目录，/usr/local/mysql/var则是用于保存真实数据库文件的目录。

[root@linuxprobe src]# mkdir -p /usr/local/mysql/var
[root@linuxprobe src]# chown -Rf mysql:mysql /usr/local/mysql
接下来解压、编译、安装MySQL数据库服务程序。在编译数据库时使用的是cmake命令，其中，-DCMAKE_INSTALL_PREFIX参数用于定义数据库服务程序的保存目录，-DMYSQL_DATADIR参数用于定义真实数据库文件的目录，-DSYSCONFDIR则是定义MySQL数据库配置文件的保存目录。由于MySQL数据库服务程序比较大，因此编译的过程比较漫长，在此期间可以稍微休息一下。

```shell
[root@linuxprobe src]# tar xzvf mysql-5.6.19.tar.gz
[root@linuxprobe src]# cd mysql-5.6.19/
[root@linuxprobe mysql-5.6.19]# cmake . -DCMAKE_INSTALL_PREFIX=/usr/local/mysql -DMYSQL_DATADIR=/usr/local/mysql/var -DSYSCONFDIR=/etc
[root@linuxprobe mysql-5.6.19]# make
[root@linuxprobe mysql-5.6.19]# make install
```

为了让MySQL数据库程序正常运转起来，需要先删除/etc目录中的默认配置文件，然后在MySQL数据库程序的保存目录scripts内找到一个名为mysql_install_db的脚本程序，执行这个脚本程序并使用--user参数指定MySQL服务的对应账号名称（在前面步骤已经创建），使用--basedir参数指定MySQL服务程序的保存目录，使用--datadir参数指定MySQL真实数据库的文件保存目录，这样即可生成系统数据库文件，也会生成出新的MySQL服务配置文件。

```shell
[root@linuxprobe mysql-5.6.19]# rm -rf /etc/my.cnf
[root@linuxprobe mysql-5.6.19]# cd /usr/local/mysql
[root@linuxprobe mysql]# ./scripts/mysql_install_db --user=mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/var
```

把系统新生成的MySQL数据库配置文件链接到/etc目录中，然后把程序目录中的开机程序文件复制到/etc/rc.d/init.d目录中，以便通过service命令来管理MySQL数据库服务程序。记得把数据库脚本文件的权限修改成755以便于让用户有执行该脚本的权限：

```shell
[root@linuxprobe mysql]# ln -s my.cnf /etc/my.cnf 
# 加入开机启动项
[root@linuxprobe mysql]# cp ./support-files/mysql.server /etc/rc.d/init.d/mysqld
[root@linuxprobe mysql]# chmod 755 /etc/rc.d/init.d/mysqld
```

编辑刚复制的MySQL数据库脚本文件，把第46、47行的basedir与datadir参数分别修改为MySQL数据库程序的保存目录和真实数据库的文件内容。

```shell
[root@linuxprobe mysql]# vim /etc/rc.d/init.d/mysqld 
………………省略部分输出信息………………
 39 #
 40 # If you want to affect other MySQL variables, you should make your changes
 41 # in the /etc/my.cnf, ~/.my.cnf or other MySQL configuration files.
 42 
 43 # If you change base dir, you must also change datadir. These may get
 44 # overwritten by settings in the MySQL configuration files.
 45 
 46 basedir=/usr/local/mysql
 47 datadir=/usr/local/mysql/var
 48 
………………省略部分输出信息………………
```

配置好脚本文件后便可以用service命令启动mysqld数据库服务了。mysqld是MySQL数据库程序的服务名称，注意不要写错。顺带再使用chkconfig命令把mysqld服务程序加入到开机启动项中。

```shell
[root@Linuxprobe mysql]# service mysqld start
Starting MySQL. SUCCESS! 
[root@linuxprobe mysql]# chkconfig mysqld on
```

MySQL数据库程序自带了许多命令，但是Bash终端的PATH变量并不会包含这些命令所存放的目录，因此我们也无法顺利地对MySQL数据库进行初始化，也就不能使用MySQL数据库自带的命令了。想要把命令所保存的目录永久性地定义到PATH变量中，需要编辑/etc/profile文件并写入追加的命令目录，这样当物理设备在下一次重启时就会永久生效了。如果不想通过重启设备的方式来生效，也可以使用source命令加载一下/ect/profile文件，此时新的PATH变量也可以立即生效了。

```shell
[root@linuxprobe mysql]# vim /etc/profile
………………省略部分输出信息………………
 64 
 65 for i in /etc/profile.d/*.sh ; do
 66 if [ -r "$i" ]; then
 67 if [ "${-#*i}" != "$-" ]; then
 68 . "$i"
 69 else
 70 . "$i" >/dev/null
 71 fi
 72 fi
 73 done
 # 把命令所保存的目录永久性地定义到PATH变量
 74 export PATH=$PATH:/usr/local/mysql/bin
 75 unset i
 76 unset -f pathmunge
[root@linuxprobe mysql]# source /etc/profile
```

MySQL数据库服务程序还会调用到一些程序文件和函数库文件。由于当前是通过源码包方式安装MySQL数据库，因此现在也必须以手动方式把这些文件链接过来。

```shell
[root@linuxprobe mysql]# mkdir /var/lib/mysql
# rhel7中下面3个步骤系统已经做好了，需要做，rhel5,6需要。
[root@linuxprobe mysql]# ln -s /usr/local/mysql/lib/mysql /usr/lib/mysql
[root@linuxprobe mysql]# ln -s /tmp/mysql.sock /var/lib/mysql/mysql.sock
[root@linuxprobe mysql]# ln -s /usr/local/mysql/include/mysql /usr/include/mysql
```

现在，MySQL数据库服务程序已经启动，调用的各个函数文件已经就位，PATH环境变量中也加入了MySQL数据库命令的所在目录。接下来准备对MySQL数据库进行初始化，这个初始化的配置过程与MariaDB数据库是一样的，只是最后变成了Thanks for using MySQL!

```shell
[root@linuxprobe mysql]# mysql_secure_installation 
NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MySQL
      SERVERS IN PRODUCTION USE!  PLEASE READ EACH STEP CAREFULLY!
In order to log into MySQL to secure it, we'll need the current
password for the root user.  If you've just installed MySQL, and
you haven't set the root password yet, the password will be blank,
so you should just press enter here.
Enter current password for root (enter for none): 此处只需按下回车键
OK, successfully used password, moving on...
Setting the root password ensures that nobody can log into the MySQL
root user without the proper authorisation.
Set root password? [Y/n] y （要为root管理员设置数据库的密码）
New password: 输入要为root管理员设置的数据库密码
Re-enter new password: 再输入一次密码
Password updated successfully!
Reloading privilege tables..
 ... Success!
By default, a MySQL installation has an anonymous user, allowing anyone
to log into MySQL without having to have a user account created for
them.  This is intended only for testing, and to make the installation
go a bit smoother.  You should remove them before moving into a
production environment.
Remove anonymous users? [Y/n] y （删除匿名账户）
 ... Success!
Normally, root should only be allowed to connect from 'localhost'.  This
ensures that someone cannot guess at the root password from the network.
Disallow root login remotely? [Y/n] y （禁止root管理员从远程登录）
 ... Success!
By default, MySQL comes with a database named 'test' that anyone can
access.  This is also intended only for testing, and should be removed
before moving into a production environment.
Remove test database and access to it? [Y/n] y （删除test数据库并取消对其的访问权限）
 - Dropping test database...
 ... Success!
 - Removing privileges on test database...
 ... Success!
Reloading the privilege tables will ensure that all changes made so far
will take effect immediately.
Reload privilege tables now? [Y/n] y （刷新授权表，让初始化后的设定立即生效）
 ... Success!
All done!  If you've completed all of the above steps, your MySQL
installation should now be secure.
Thanks for using MySQL!
Cleaning up...
```

20.2.2 配置Nginx服务

Nginx是一款相当优秀的用于部署动态网站的轻量级服务程序，它最初是为俄罗斯门户站点而开发的，因其稳定性、功能丰富、占用内存少且并发能力强而备受用户的信赖。目前国内诸如新浪、网易、腾讯等门户站点均已使用了此服务。

Nginx服务程序的稳定性源自于采用了分阶段的资源分配技术，降低了CPU与内存的占用率，所以使用Nginx程序部署的动态网站环境不仅十分稳定、高效，而且消耗的系统资源也很少。此外，Nginx具备的模块数量与Apache具备的模块数量几乎相同，而且现在已经完全支持proxy、rewrite、mod_fcgi、ssl、vhosts等常用模块。更重要的是，Nginx还支持热部署技术，可以7×24不间断提供服务，还可以在不暂停服务的情况下直接对Nginx服务程序进行升级。

图20-2 Nginx与Apache著名LOGO

坦白来讲，虽然Nginx程序的代码质量非常高，代码很规范，技术成熟，模块扩展也很容易，但依然存在不少问题，比如是由俄罗斯人开发的，所以在资料文档方面还并不完善，中文资料的质量更是鱼龙混杂。但是Nginx服务程序在近年来增长势头迅猛，相信会在轻量级Web服务器市场具有不错的未来。

在正式安装Nginx服务程序之前，我们还需要为其解决相关的软件依赖关系，例如用于提供Perl语言兼容的正则表达式库的软件包pcre，就是Nginx服务程序用于实现伪静态功能必不可少的依赖包。下面来解压、编译、生成、安装Nginx服务程序的源码文件：

```shell
[root@linuxprobe ~]# cd /usr/local/src
[root@linuxprobe src]# tar xzvf pcre-8.35.tar.gz 
[root@linuxprobe src]# cd pcre-8.35
[root@linuxprobe pcre-8.35]# ./configure --prefix=/usr/local/pcre
[root@linuxprobe pcre-8.35]# make
[root@linuxprobe pcre-8.35]# make install 
```

openssl软件包是用于提供网站加密证书服务的程序文件，在安装该程序时需要自定义服务程序的安装目录，以便于稍后调用它们的时候更可控。

```shell
[root@linuxprobe pcre-8.35]# cd /usr/local/src
[root@linuxprobe src]# tar xzvf openssl-1.0.1h.tar.gz
[root@linuxprobe src]# cd openssl-1.0.1h
[root@linuxprobe openssl-1.0.1h]# ./config --prefix=/usr/local/openssl
[root@linuxprobe openssl-1.0.1h]# make
[root@linuxprobe openssl-1.0.1h]# make install
```

openssl软件包安装后默认会在/usr/local/openssl/bin目录中提供很多的可用命令，我们需要像前面的操作那样，将这个目录添加到PATH环境变量中，并写入到配置文件中，最后执行source命令以便让新的PATH环境变量内容可以立即生效：

```shell
[root@linuxprobe pcre-8.35]# vim /etc/profile
………………省略部分输出信息………………
 64 
 65 for i in /etc/profile.d/*.sh ; do
 66 if [ -r "$i" ]; then
 67 if [ "${-#*i}" != "$-" ]; then
 68 . "$i"
 69 else
 70 . "$i" >/dev/null
 71 fi
 72 fi
 73 done
 74 export PATH=$PATH:/usr/local/mysql/bin:/usr/local/openssl/bin
 75 unset i
 76 unset -f pathmunge
[root@linuxprobe pcre-8.35]# source /etc/profile
```

zlib软件包是用于提供压缩功能的函数库文件。其实Nginx服务程序调用的这些服务程序无需深入了解，只要大致了解其作用就已经足够了：

```shell
[root@linuxprobe pcre-8.35]# cd /usr/local/src
[root@linuxprobe src]# tar xzvf zlib-1.2.8.tar.gz 
[root@linuxprobe src]# cd zlib-1.2.8
[root@linuxprobe zlib-1.2.8]# ./configure --prefix=/usr/local/zlib
[root@linuxprobe zlib-1.2.8]# make
[root@linuxprobe zlib-1.2.8]# make install
```

在安装部署好具有依赖关系的软件包之后，创建一个用于执行Nginx服务程序的账户。账户名称可以自定义，但一定别忘记，因为在后续需要调用：

```shell
[root@linuxprobe zlib-1.2.8]# cd ..
[root@linuxprobe src]# useradd www -s /sbin/nologin
```

在使用命令编译Nginx服务程序时，需要设置特别多的参数，其中，--prefix参数用于定义服务程序稍后安装到的位置，--user与--group参数用于指定执行Nginx服务程序的用户名和用户组。在使用参数调用openssl、zlib、pcre软件包时，请写出软件源码包的解压路径，而不是程序的安装路径：

```shell
[root@linuxprobe src]# tar xzvf nginx-1.6.0.tar.gz
[root@linuxprobe src]# cd nginx-1.6.0/
[root@linuxprobe nginx-1.6.0]# ./configure --prefix=/usr/local/nginx --without-http_memcached_module --user=www --group=www --with-http_stub_status_module --with-http_ssl_module --with-http_gzip_static_module --with-openssl=/usr/local/src/openssl-1.0.1h --with-zlib=/usr/local/src/zlib-1.2.8 --with-pcre=/usr/local/src/pcre-8.35
[root@linuxprobe nginx-1.6.0]# make
[root@linuxprobe nginx-1.6.0]# make install
```

要想启动Nginx服务程序以及将其加入到开机启动项中，也需要有脚本文件。可惜的是，在安装完Nginx软件包之后默认并没有为用户提供脚本文件，因此刘遄老师给各位读者准备了一份可用的启动脚本文件，大家只需在/etc/rc.d/init.d目录中创建脚本文件并直接复制下面的脚本内容即可（相信各位读者在掌握了第4章的内容之后，应该可以顺利看懂这个脚本文件）。

```shell
[root@linuxprobe nginx-1.6.0]# vim /etc/rc.d/init.d/nginx
#!/bin/bash
# nginx - this script starts and stops the nginx daemon
# chkconfig: - 85 15
# description: Nginx is an HTTP(S) server, HTTP(S) reverse \
# proxy and IMAP/POP3 proxy server
# processname: nginx
# config: /etc/nginx/nginx.conf
# config: /usr/local/nginx/conf/nginx.conf
# pidfile: /usr/local/nginx/logs/nginx.pid
# Source function library.
. /etc/rc.d/init.d/functions
# Source networking configuration.
. /etc/sysconfig/network
# Check that networking is up.
[ "$NETWORKING" = "no" ] && exit 0
nginx="/usr/local/nginx/sbin/nginx"
prog=$(basename $nginx)
NGINX_CONF_FILE="/usr/local/nginx/conf/nginx.conf"
[ -f /etc/sysconfig/nginx ] && . /etc/sysconfig/nginx
lockfile=/var/lock/subsys/nginx
make_dirs() {
# make required directories
user=`$nginx -V 2>&1 | grep "configure arguments:" | sed 's/[^*]*--user=\([^ ]*\).*/\1/g' -`
        if [ -z "`grep $user /etc/passwd`" ]; then
                useradd -M -s /bin/nologin $user
        fi
options=`$nginx -V 2>&1 | grep 'configure arguments:'`
for opt in $options; do
        if [ `echo $opt | grep '.*-temp-path'` ]; then
                value=`echo $opt | cut -d "=" -f 2`
                if [ ! -d "$value" ]; then
                        # echo "creating" $value
                        mkdir -p $value && chown -R $user $value
                fi
        fi
done
}
start() {
[ -x $nginx ] || exit 5
[ -f $NGINX_CONF_FILE ] || exit 6
make_dirs
echo -n $"Starting $prog: "
daemon $nginx -c $NGINX_CONF_FILE
retval=$?
echo
[ $retval -eq 0 ] && touch $lockfile
return $retval
}
stop() {
echo -n $"Stopping $prog: "
killproc $prog -QUIT
retval=$?
echo
[ $retval -eq 0 ] && rm -f $lockfile
return $retval
}
restart() {
#configtest || return $?
stop
sleep 1
start
}
reload() {
#configtest || return $?
echo -n $"Reloading $prog: "
killproc $nginx -HUP
RETVAL=$?
echo
}
force_reload() {
restart
}
configtest() {
$nginx -t -c $NGINX_CONF_FILE
}
rh_status() {
status $prog
}
rh_status_q() {
rh_status >/dev/null 2>&1
}
case "$1" in
start)
        rh_status_q && exit 0
        $1
        ;;
stop)
        rh_status_q || exit 0
        $1
        ;;
restart|configtest)
$1
;;
reload)
        rh_status_q || exit 7
        $1
        ;;
force-reload)
        force_reload
        ;;
status)
        rh_status
        ;;
condrestart|try-restart)
        rh_status_q || exit 0
        ;;
*)
echo $"Usage: $0 {start|stop|status|restart|condrestart|try-restart|reload|force-reload|configtest}"
exit 2
esac
```

保存脚本文件后记得为其赋予755权限，以便能够执行这个脚本。然后以绝对路径的方式执行这个脚本，通过restart参数重启Nginx服务程序，最后再使用chkconfig命令将Nginx服务程序添加至开机启动项中。大功告成！

```shell
[root@linuxprobe nginx-1.6.0]# chmod 755 /etc/rc.d/init.d/nginx
[root@linuxprobe nginx-1.6.0]# /etc/rc.d/init.d/nginx restart
Restarting nginx (via systemctl):                          [  OK  ]
[root@linuxprobe nginx-1.6.0]# chkconfig nginx on
```

Nginx服务程序在启动后就可以在浏览器中输入服务器的IP地址来查看到默认网页了。相较于Apache服务程序的红色默认页面，Nginx服务程序的默认页面显得更加简洁，如图20-2所示。

图20-3  Nginx服务程序的默认页面

20.2.3 配置php服务

PHP（Hypertxt Preprocessor，超文本预处理器）是一种通用的开源脚本语言，发明于1995年，它吸取了C语言、Java语言及Perl语言的很多优点，具有开源、免费、快捷、跨平台性强、效率高等优良特性，是目前Web开发领域最常用的语言之一。本书的配套站点就是基于PHP语言编写的。

使用源码包的方式编译安装PHP语言环境其实并不复杂，难点在于解决PHP的程序包和其他软件的依赖关系。为此需要先安装部署将近十个用于搭建网站页面的软件程序包，然后才能正式安装PHP程序。

yasm源码包是一款常见的开源汇编器，其解压、编译、安装过程中生成的输出信息均已省略：

```shell
[root@linuxprobe nginx-1.6.0]# cd ..
[root@linuxprobe src]# tar zxvf yasm-1.2.0.tar.gz
[root@linuxprobe src]# cd yasm-1.2.0
[root@linuxprobe yasm-1.2.0]# ./configure
[root@linuxprobe yasm-1.2.0]# make
[root@linuxprobe yasm-1.2.0]# make install
```

libmcrypt源码包是用于加密算法的扩展库程序，其解压、编译、安装过程中生成的输出信息均已省略：

```shell
[root@linuxprobe yasm-1.2.0]# cd ..
[root@linuxprobe src]# tar zxvf libmcrypt-2.5.8.tar.gz
[root@linuxprobe src]# cd libmcrypt-2.5.8
[root@linuxprobe libmcrypt-2.5.8]# ./configure
[root@linuxprobe libmcrypt-2.5.8]# make
[root@linuxprobe libmcrypt-2.5.8]# make install
```

libvpx源码包是用于提供视频编码器的服务程序，其解压、编译、安装过程中生成的输出信息均已省略。相信会有很多粗心的读者顺手使用了tar命令的xzvf参数，但如果仔细观察就会发现libvpx源码包的后缀是.tar.bz2，即表示使用bzip2格式进行的压缩，因此正确的解压参数应该是xjvf：

```shell
[root@linuxprobe libmcrypt-2.5.8]# cd ..
[root@linuxprobe src]# tar xjvf libvpx-v1.3.0.tar.bz2
[root@linuxprobe src]# cd libvpx-v1.3.0
[root@linuxprobe libvpx-v1.3.0]# ./configure --prefix=/usr/local/libvpx --enable-shared --enable-vp9
[root@linuxprobe libvpx-v1.3.0]# make
[root@linuxprobe libvpx-v1.3.0]# make install
```

tiff源码包是用于提供标签图像文件格式的服务程序，其解压、编译、安装过程中生成的输出信息均已省略：

```shell
[root@linuxprobe libvpx-v1.3.0]# cd ..
[root@linuxprobe src]# tar zxvf tiff-4.0.3.tar.gz
[root@linuxprobe src]# cd tiff-4.0.3
[root@linuxprobe tiff-4.0.3]# ./configure --prefix=/usr/local/tiff --enable-shared
[root@linuxprobe tiff-4.0.3]# make
[root@linuxprobe tiff-4.0.3]# make install
```

libpng源码包是用于提供png图片格式支持函数库的服务程序，其解压、编译、安装过程中生成的输出信息均已省略：

```shell
[root@linuxprobe tiff-4.0.3]# cd ..
[root@linuxprobe src]# tar zxvf libpng-1.6.12.tar.gz
[root@linuxprobe src]# cd libpng-1.6.12
[root@linuxprobe libpng-1.6.12]# ./configure --prefix=/usr/local/libpng --enable-shared
[root@linuxprobe libpng-1.6.12]# make
[root@linuxprobe libpng-1.6.12]# make install
```

freetype源码包是用于提供字体支持引擎的服务程序，其解压、编译、安装过程中生成的输出信息均已省略：

```shell
[root@linuxprobe libpng-1.6.12]# cd ..
[root@linuxprobe src]# tar zxvf freetype-2.5.3.tar.gz
[root@linuxprobe src]# cd freetype-2.5.3
# 下面3步骤等同于 ./configure --prefix=/usr/local/freetype --enable-shared ; make ; install
[root@linuxprobe freetype-2.5.3]# ./configure --prefix=/usr/local/freetype --enable-shared
[root@linuxprobe freetype-2.5.3]# make
[root@linuxprobe freetype-2.5.3]# make install
```

jpeg源码包是用于提供jpeg图片格式支持函数库的服务程序，其解压、编译、安装过程中生成的输出信息均已省略：

```shell
[root@linuxprobe freetype-2.5.3]# cd ..
[root@linuxprobe src]# tar zxvf jpegsrc.v9a.tar.gz
[root@linuxprobe src]# cd jpeg-9a
[root@linuxprobe jpeg-9a]# ./configure --prefix=/usr/local/jpeg --enable-shared
[root@linuxprobe jpeg-9a]# make
[root@linuxprobe jpeg-9a]# make install
```

libgd源码包是用于提供图形处理的服务程序，其解压、编译、安装过程中生成的输出信息均已省略。在编译libgd源码包时，请记得写入的是jpeg、libpng、freetype、tiff、libvpx等服务程序在系统中的安装路径，即在上面安装过程中使用--prefix参数指定的目录路径：

```shell
[root@linuxprobe jpeg-9a]# cd ..
[root@linuxprobe src]# tar zxvf libgd-2.1.0.tar.gz
[root@linuxprobe src]# cd libgd-2.1.0
[root@linuxprobe libgd-2.1.0]# ./configure --prefix=/usr/local/libgd --enable-shared --with-jpeg=/usr/local/jpeg --with-png=/usr/local/libpng --with-freetype=/usr/local/freetype --with-fontconfig=/usr/local/freetype --with-xpm=/usr/ --with-tiff=/usr/local/tiff --with-vpx=/usr/local/libvpx
[root@linuxprobe libgd-2.1.0]# make
[root@linuxprobe libgd-2.1.0]# make install
```

t1lib源码包是用于提供图片生成函数库的服务程序，其解压、编译、安装过程中生成的输出信息均已省略。安装后把/usr/lib64目录中的函数文件链接到/usr/lib目录中，以便系统能够顺利调取到函数文件：

```shell
[root@linuxprobe cd libgd-2.1.0]# cd ..
[root@linuxprobe src]# tar zxvf t1lib-5.1.2.tar.gz
[root@linuxprobe src]# cd t1lib-5.1.2
[root@linuxprobe t1lib-5.1.2]# ./configure --prefix=/usr/local/t1lib --enable-shared
[root@linuxprobe t1lib-5.1.2]# make
[root@linuxprobe t1lib-5.1.2]# make install
[root@linuxprobe t1lib-5.1.2]# ln -s /usr/lib64/libltdl.so /usr/lib/libltdl.so 
[root@linuxprobe t1lib-5.1.2]# cp -frp /usr/lib64/libXpm.so* /usr/lib/
```

此时终于把编译php服务源码包的相关软件包都已经安装部署妥当了。在开始编译php源码包之前，先定义一个名为LD_LIBRARY_PATH的全局环境变量，该环境变量的作用是帮助系统找到指定的动态链接库文件，这些文件是编译php服务源码包的必须元素之一。编译php服务源码包时，除了定义要安装到的目录以外，还需要依次定义配置php服务程序配置文件的保存目录、MySQL数据库服务程序所在目录、MySQL数据库服务程序配置文件所在目录，以及libpng、jpeg、freetype、libvpx、zlib、t1lib等服务程序的安装目录路径，并通过参数启动php服务程序的诸多默认功能：

```shell
[root@linuxprobe t1lib-5.1.2]# cd ..
[root@linuxprobe src]# tar -zvxf php-5.5.14.tar.gz
[root@linuxprobe src]# cd php-5.5.14
[root@linuxprobe php-5.5.14]# export LD_LIBRARY_PATH=/usr/local/libgd/lib
[root@linuxprobe php-5.5.14]# ./configure --prefix=/usr/local/php --with-config-file-path=/usr/local/php/etc --with-mysql=/usr/local/mysql --with-mysqli=/usr/local/mysql/bin/mysql_config --with-mysql-sock=/tmp/mysql.sock --with-pdo-mysql=/usr/local/mysql --with-gd --with-png-dir=/usr/local/libpng --with-jpeg-dir=/usr/local/jpeg --with-freetype-dir=/usr/local/freetype --with-xpm-dir=/usr/ --with-vpx-dir=/usr/local/libvpx/ --with-zlib-dir=/usr/local/zlib --with-t1lib=/usr/local/t1lib --with-iconv --enable-libxml --enable-xml --enable-bcmath --enable-shmop --enable-sysvsem --enable-inline-optimization --enable-opcache --enable-mbregex --enable-fpm --enable-mbstring --enable-ftp --enable-gd-native-ttf --with-openssl --enable-pcntl --enable-sockets --with-xmlrpc --enable-zip --enable-soap --without-pear --with-gettext --enable-session --with-mcrypt --with-curl --enable-ctype 
[root@linuxprobe php-5.5.14]# make
[root@linuxprobe php-5.5.14]# make install
```

在php源码包程序安装完成后，需要删除当前默认的配置文件，然后将php服务程序目录中相应的配置文件复制过来：

```shell
[root@linuxprobe php-5.5.14]# rm -rf /etc/php.ini
[root@linuxprobe php-5.5.14]# ln -s /usr/local/php/etc/php.ini /etc/php.ini
[root@linuxprobe php-5.5.14]# cp php.ini-production /usr/local/php/etc/php.ini
[root@linuxprobe php-5.5.14]# cp /usr/local/php/etc/php-fpm.conf.default /usr/local/php/etc/php-fpm.conf
[root@linuxprobe php-5.5.14]# ln -s /usr/local/php/etc/php-fpm.conf /etc/php-fpm.conf
```

php-fpm.conf是php服务程序重要的配置文件之一，我们需要启用该配置文件中第25行左右的pid文件保存目录，然后分别将第148和149行的user与group参数分别修改为www账户和用户组名称：

```shell
[root@linuxprobe php-5.5.14]# vim /usr/local/php/etc/php-fpm.conf
1 ;;;;;;;;;;;;;;;;;;;;;
2 ; FPM Configuration ;
3 ;;;;;;;;;;;;;;;;;;;;;
4 
5 ; All relative paths in this configuration file are relative to PHP's instal l
6 ; prefix (/usr/local/php). This prefix can be dynamically changed by using t he
7 ; '-p' argument from the command line.
8 
9 ; Include one or more files. If glob(3) exists, it is used to include a bunc h of
10 ; files from a glob(3) pattern. This directive can be used everywhere in the
11 ; file.
12 ; Relative path can also be used. They will be prefixed by:
13 ; - the global prefix if it's been set (-p argument)
14 ; - /usr/local/php otherwise
15 ;include=etc/fpm.d/*.conf
16 
17 ;;;;;;;;;;;;;;;;;;
18 ; Global Options ;
19 ;;;;;;;;;;;;;;;;;;
20 
21 [global]
22 ; Pid file
23 ; Note: the default prefix is /usr/local/php/var
24 ; Default Value: none
25 pid = run/php-fpm.pid
26 
………………省略部分输出信息………………
145 ; Unix user/group of processes
146 ; Note: The user is mandatory. If the group is not set, the default user's g roup
147 ; will be used.
148 user = www
149 group = www
150 
………………省略部分输出信息………………
```

配置妥当后便可把用于管理php服务的脚本文件复制到/etc/rc.d/init.d中了。为了能够执行脚本，请记得为脚本赋予755权限。最后把php-fpm服务程序加入到开机启动项中：

```shell
[root@linuxprobe php-5.5.14]# cp sapi/fpm/init.d.php-fpm /etc/rc.d/init.d/php-fpm
[root@linuxprobe php-5.5.14]# chmod 755 /etc/rc.d/init.d/php-fpm
[root@linuxprobe php-5.5.14]# chkconfig php-fpm on
```

由于php服务程序的配置参数直接会影响到Web服务服务的运行环境，因此，如果默认开启了一些不必要且高危的功能（如允许用户在网页中执行Linux命令），则会降低网站被入侵的难度，入侵人员甚至可以拿到整台Web服务器的管理权限。因此我们需要编辑php.ini配置文件，在305行的disable_functions参数后面追加上要禁止的功能。下面的禁用功能名单是刘遄老师依据网站运行的经验而定制的，不见得适合每个生产环境，建议大家在此基础上根据自身工作需求酌情删减：

```shell
[root@linuxprobe php-5.5.14]# vim /usr/local/php/etc/php.ini
………………省略部分输出信息………………
300 
301 ; This directive allows you to disable certain functions for security reasons.
302 ; It receives a comma-delimited list of function names. This directive is
303 ; *NOT* affected by whether Safe Mode is turned On or Off.
304 ; http://php.net/disable-functions
305 disable_functions = passthru,exec,system,chroot,scandir,chgrp,chown,shell_exec,proc_open,proc_get_status,ini_alter,ini_alter,ini_restor e,dl,openlog,syslog,readlink,symlink,popepassthru,stream_socket_server,escapeshellcmd,dll,popen,disk_free_space,checkdnsrr,checkdnsrr,g etservbyname,getservbyport,disk_total_space,posix_ctermid,posix_get_last_error,posix_getcwd,posix_getegid,posix_geteuid,posix_getgid,po six_getgrgid,posix_getgrnam,posix_getgroups,posix_getlogin,posix_getpgid,posix_getpgrp,posix_getpid,posix_getppid,posix_getpwnam,posix_ getpwuid,posix_getrlimit,posix_getsid,posix_getuid,posix_isatty,posix_kill,posix_mkfifo,posix_setegid,posix_seteuid,posix_setgid,posix_ setpgid,posix_setsid,posix_setuid,posix_strerror,posix_times,posix_ttyname,posix_uname
306 
………………省略部分输出信息………………
```

这样就把php服务程序配置妥当了。最后，还需要编辑Nginx服务程序的主配置文件，把第2行的井号（#）删除，然后在后面写上负责运行Nginx服务程序的账户名称和用户组名称；在第45行的index参数后面写上网站的首页名称。最后是将第65～71行参数前的井号（#）删除来启用参数，主要是修改第69行的脚本名称路径参数，其中$document_root变量即为网站信息存储的根目录路径，若没有设置该变量，则Nginx服务程序无法找到网站信息，因此会提示“404页面未找到”的报错信息。在确认参数信息填写正确后便可重启Nginx服务与php-fpm服务。

```shell
[root@linuxprobe php-5.5.14]# vim /usr/local/nginx/conf/nginx.conf
 1 
 2 user www www;
 3 worker_processes 1;
 4 
 5 #error_log logs/error.log;
 6 #error_log logs/error.log notice;
 7 #error_log logs/error.log info;
 8 
 9 #pid logs/nginx.pid;
 10 
 11 
………………省略部分输出信息………………
 40 
 41 #access_log logs/host.access.log main;
 42 
 43 location / {
 44 root html;
 45 index index.html index.htm index.php;
 46 }
 47 
………………省略部分输出信息………………
 62 
 63 #pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
 64 
 65 location ~ \.php$ {
 66 root html;
 67 fastcgi_pass 127.0.0.1:9000;
 68 fastcgi_index index.php;
 69 fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
 70 include fastcgi_params;
 71 }
 72 
………………省略部分输出信息………………
[root@linuxprobe php-5.5.14]# systemctl restart nginx
[root@linuxprobe php-5.5.14]# systemctl restart php-fpm
```

至此，LNMP动态网站环境架构的配置实验全部结束。

20.3 搭建Discuz论坛

为了检验LNMP动态网站环境是否配置妥当，可以使用在上面部署Discuz!系统，然后查看结果。如果能够在LNMP动态网站环境中成功安装使用Discuz!论坛系统，也就意味着这套架构是可用的。Discuz! X3.2是国内最常见的社区论坛系统，在经过十多年的研发后已经成为了全球成熟度最高、覆盖率最广的论坛网站系统之一。

Discuz! X3.2软件包的后缀是.zip格式，因此应当使用专用的unzip命令来进行解压。解压后会在当前目录中出现一个名为upload的文件目录，这里面保存的就是Discuz！论坛的系统程序。我们把Nginx服务程序网站根目录的内容清空后，就可以把这些这个目录中的文件都复制进去了。记得把Nginx服务程序的网站根目录的所有者和所属组修改为本地的www用户（已在20.2.2小节创建），并为其赋予755权限以便于能够读、写、执行该论坛系统内的文件。

```shell
[root@linuxprobe php-5.5.14 ]# cd /usr/local/src/
[root@linuxprobe src]# unzip Discuz_X3.2_SC_GBK.zip
[root@linuxprobe src]# rm -rf /usr/local/nginx/html/{index.html,50x.html}*
[root@linuxprobe src]# mv upload/* /usr/local/nginx/html/
[root@linuxprobe src]# chown -Rf www:www /usr/local/nginx/html
[root@linuxprobe src]# chmod -Rf 755 /usr/local/nginx/html
```

第1步：接受Discuz!安装向导的许可协议。在把Discuz!论坛系统程序（即刚才upload目录中的内容）复制Nginx服务网站根目录后便可刷新浏览器页面，这将自动跳转到Discuz! X3.2论坛系统的安装界面，此处需单击“我同意”按钮，进入下一步的安装过程中，如图20-4所示。

图20-4  接受Discuz! X3.2论坛系统的安装许可

第2步：检查Discuz! X3.2论坛系统的安装环境及目录权限。我们部署的LNMP动态网站环境版本和软件都与Discuz!论坛的要求相符合，如果图20-5框中的目录状态为不可写，请自行检查目录的所有者和所属组是否为www用户，以及是否对目录设置了755权限，然后单击“下一步”按钮。

图20-5  检查Discuz! X3.2论坛系统的安装环境及目录权限

第3步：选择“全新安装Discuz! X（含UCenter Server）”。UCenter Server是站点的管理平台，能够在多个站点之间同步会员账户及密码信息，单击“下一步”按钮，如图20-6所示。

图20-6  选择全新安装Discuz!论坛及UCenter Server

第4步：填写服务器的数据库信息与论坛系统管理员信息。网站系统使用由服务器本地（localhost）提供的数据库服务，数据名称与数据表前缀可由用户自行填写，其中数据库的用户名和密码则为用于登录MySQL数据库的信息（以初始化MySQL服务程序时填写的信息为准）。论坛系统的管理员账户为今后登录、管理Discuz!论坛时使用的验证信息，其中账户可以设置得简单好记一些，但是要将密码设置得尽可能复杂一下。在信息填写正确后单击“下一步”按钮，如图20-7所示。

图20-7  填写服务器的数据库信息与论坛系统管理员信息

第5步：等待Discuz! X3.2论坛系统安装完毕，如图20-8所示。这个安装过程是非常快速的，大概只需要30秒左右，然后就可看到论坛安装完成的欢迎界面了。由于虚拟机主机可能并没有连接到互联网，因此该界面中可能无法正常显示Discuz!论坛系统的广告信息。在接入了互联网的服务器上成功安装完Discuz! X3.2论坛系统之后，其界面如图20-9所示。随后单击“您的论坛已完成安装，点此访问”按钮，即可访问到论坛首页，如图20-10所示。

图20-8  等待Discuz! X3.2论坛系统安装完毕

图20-9  成功安装Discuz! X3.2论坛系统后的欢迎界面

图20-10  Discuz! X3.2论坛系统的首页界面

20.4 选购服务器主机
我们日常访问的网站是由域名、网站源程序和主机共同组成的，其中，主机则是用于存放网页源代码并能够把网页内容展示给用户的服务器。在本书即将结束之际，刘遄老师再啰嗦几句有关服务器主机的知识以及选购技巧，这些技巧都是在近几年做网站时总结出来的，希望能对大家有所帮助。

虚拟主机：在一台服务器中划分一定的磁盘空间供用户放置网站信息、存放数据等；仅提供基础的网站访问、数据存放与传输功能；能够极大地降低用户费用，也几乎不需要用户来维护网站以外的服务；适合小型网站。

VPS（Virtual Private Server，虚拟专用服务器）：在一台服务器中利用OpenVZ、Xen或KVM等虚拟化技术模拟出多台“主机”（即VPS），每个主机都有独立的IP地址、操作系统；不同VPS之间的磁盘空间、内存、CPU、进程与系统配置完全隔离，用户可自由使用分配到的主机中的所有资源，为此需要具备一定的维护系统的能力；适合小型网站。

ECS（Elastic Compute Service，云服务器）：是一种整合了计算、存储、网络，能够做到弹性伸缩的计算服务；使用起来与VPS几乎一样，差别是云服务器是建立在一组集群服务器中，每个服务器都会保存一个主机的镜像（备份），从而大大提升了安全性和稳定性；另外还具备灵活性与扩展性；用户只需按使用量付费即可；适合大中小型网站。

独立服务器：这台服务器仅提供给用户一个人使用，其使用方式分为租用方式与托管方式。租用方式是用户将服务器的硬件配置要求告知IDC服务商，按照月、季、年为单位来租用它们的硬件设备。这些硬件设备由IDC服务商的机房负责维护，用户一般需要自行安装相应的软件并部署网站服务，这减轻了用户在硬件设备上的投入，适合大中型网站。托管方式则是用户需要自行购置服务器硬件设备，并将其交给IDC服务供应商进行管理（需要缴纳管理服务费）。用户对服务器硬件配置有完全的控制权，自主性强，但需要自行维护、修理服务器硬件设备，适合大中型网站。

另外需要提醒读者的是，在选择服务器主机供应商时请一定要注意查看口碑，并在综合分析后再决定购买。某些供应商会有限制功能、强制添加广告、隐藏扣费或强制扣费等恶劣行为，请各位读者一定擦亮眼睛，不要上当!


本章节的复习作业(答案就在问题的下一行哦，用鼠标选中即可看到的~)

1．使用源码包安装服务程序的最大优点和缺点是什么？

答：使用源码包安装服务程序的最大优势是，服务程序的可移植性好，而且能更好地提升服务程序的运行效率；缺点是源码包程序的安装、管理、卸载和维护都比较麻烦。

2．使用源码包的方式来安装软件服务的大致步骤是什么？

答：基本分为4个步骤，分别为下载及解压源码包文件、编译源码包代码、生成二进制安装程序、运行二进制的服务程序安装包。

3．LNMP动态网站部署架构通常包含了哪些服务程序？

答：LNMP动态网站部署架构通常包含Linux系统、Nginx网站服务、MySQL数据库管理系统，以及PHP脚本语言。

4．在MySQL数据库服务程序中，/usr/local/mysql与/usr/local/mysql/var目录的作用是什么？

答：/usr/local/mysql用于保存MySQL数据库服务程序的目录，/usr/local/mysql/var则用于保存真实数据库文件的目录。

5．较之于Apache服务程序，Nginx最显著的优势是什么？

答：Nginx服务程序比较稳定，原因是采用了的资源分配技术，降低了CPU与内存的占用率，所以使用Nginx程序部署的动态网站环境不仅十分稳定、高效，而且消耗的系统资源也很少。

6．如何禁止php服务程序中不安全的功能？

答：编辑php服务程序的配置文件（/usr/local/php/etc/php.ini），把要禁用的功能追加到disable_functions参数之后即可。

7． 对于处于创业阶段的小站长群体来说，适合购买哪种服务器类型呢？

答：刘遄老师建议他们选择云服务器类型，不但费用便宜（每个月费用不超过100元人民币），而且性能也十分强劲。