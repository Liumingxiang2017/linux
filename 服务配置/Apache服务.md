# 使用Apache服务部署静态网站

apache 印第安语 力量无穷

协议名 http
服务名 httpd
软件包名 httpd

编辑配置文件

1. Linux中一切皆是文件
2. 配置服务就是修改服务配置文件
3. 要想让服务程序获取运行参数，就要重启相应服务程序 systemctl restart serviceName
4. 顺手加入开机启动 systemctl enable serviceName

网站无法访问

- 没有网页资源
- 没有权限SElinux,以及目录普通权限

## 网站服务程序

1970年，作为互联网前身的ARPANET（阿帕网）已初具雏形，并开始向非军用部门开放，许多大学和商业部门开始接入。虽然彼时阿帕网的规模（只有4台主机联网运行）还不如现在的局域网成熟，但是它依然为网络技术的进步打下了扎实的基础。

想必我们大多数人都是通过访问网站而开始接触互联网的吧。我们平时访问的网站服务就是Web网络服务，一般是指允许用户通过浏览器访问到互联网中各种资源的服务。如图10-1所示，Web网络服务是一种被动访问的服务程序，即只有接收到互联网中其他主机发出的请求后才会响应，最终用于提供服务程序的Web服务器会通过HTTP（超文本传输协议）或HTTPS（安全超文本传输协议）把请求的内容传送给用户。

目前能够提供Web网络服务的程序有IIS、Nginx和Apache等。其中，IIS（Internet Information Services，互联网信息服务）是Windows系统中默认的Web服务程序，这是一款图形化的网站管理工具，不仅可以提供Web网站服务，还可以提供FTP、NMTP、SMTP等服务。但是，IIS只能在Windows系统中使用，而我们这本书的名字是《Linux就该这么学》，所以它也就不在我们的学习范围之内了。

第10章 使用Apache服务部署静态网站。第10章 使用Apache服务部署静态网站。

图10-1  主机与Web服务器之间的通信

2004年10月4日，为俄罗斯知名门户站点而开发的Web服务程序Nginx横空出世。Nginx程序作为一款轻量级的网站服务软件，因其稳定性和丰富的功能而快速占领服务器市场，但Nginx最被认可的还当是系统资源消耗低且并发能力强，因此得到了国内诸如新浪、网易、腾讯等门户站的青睐。本书将在第20章讲解Nginx服务程序。

Apache程序是目前拥有很高市场占有率的Web服务程序之一，其跨平台和安全性广泛被认可且拥有快速、可靠、简单的API扩展。图10-2所示为Apache服务基金会的著名Logo，它的名字取自美国印第安人的土著语，寓意着拥有高超的作战策略和无穷的耐性。Apache服务程序可以运行在Linux系统、UNIX系统甚至是Windows系统中，支持基于IP、域名及端口号的虚拟主机功能，支持多种认证方式，集成有代理服务器模块、安全Socket层（SSL），能够实时监视服务状态与定制日志消息，并有着各类丰富的模块支持。

Apache程序是在RHEL 5、6、7系统的默认Web服务程序，其相关知识点一直也是RHCSA和RHCE认证考试的重点内容。

第10章 使用Apache服务部署静态网站。第10章 使用Apache服务部署静态网站。

图10-2  Apache软件基金会著名的Logo

总结来说，Nginx服务程序作为后起之秀，已经通过自身的优势与努力赢得了大批站长的信赖。本书配套的在线学习站点https://www.linuxprobe.com就是基于Nginx服务程序部署的，不得不说Nginx也真的很棒！

但是，Apache程序作为老牌的Web服务程序，一方面在Web服务器软件市场具有相当高的占有率，另一方面Apache也是RHEL 7系统中默认的Web服务程序，而且还是RHCSA和RHCE认证考试的必考内容，因此无论从实际应用角度还是从应对红帽认证考试的角度，我们都有必要好好学习Apache服务程序的部署，并深入挖掘其可用的丰富功能。

第1步：把光盘设备中的系统镜像挂载到/media/cdrom目录。

[root@linuxprobe ~]# mkdir -p /media/cdrom
[root@linuxprobe ~]# mount /dev/cdrom /media/cdrom
mount: /dev/sr0 is write-protected, mounting read-only
第2步：使用Vim文本编辑器创建Yum仓库的配置文件，下述命令中具体参数的含义可参考4.1.4小节。

[root@linuxprobe ~]# vim /etc/yum.repos.d/rhel7.repo
[rhel7]
name=rhel7
baseurl=file:///media/cdrom
enabled=1
gpgcheck=0
第3步：动手安装Apache服务程序。注意，使用yum命令进行安装时，跟在命令后面的Apache服务的软件包名称为httpd。如果直接执行yum install apache命令，则系统会报错。

```shell
[root@linuxprobe ~]# yum install httpd
Loaded plugins: langpacks, product-id, subscription-manager
………………省略部分输出信息………………
Dependencies Resolved
================================================================================
 Package Arch Version Repository Size
================================================================================
Installing:
 httpd x86_64 2.4.6-17.el7 rhel 1.2 M
Installing for dependencies:
 apr x86_64 1.4.8-3.el7 rhel 103 k
 apr-util x86_64 1.5.2-6.el7 rhel 92 k
 httpd-tools x86_64 2.4.6-17.el7 rhel 77 k
 mailcap noarch 2.1.41-2.el7 rhel 31 k
Transaction Summary
================================================================================
Install 1 Package (+4 Dependent packages)
Total download size: 1.5 M
Installed size: 4.3 M
Is this ok [y/d/N]: y
Downloading packages:
--------------------------------------------------------------------------------
………………省略部分输出信息………………
Complete!
```

第4步：启用httpd服务程序并将其加入到开机启动项中，使其能够随系统开机而运行，从而持续为用户提供Web服务：

```shell
[root@linuxprobe ~]# systemctl start httpd
[root@linuxprobe ~]# systemctl enable httpd
ln -s '/usr/lib/systemd/system/httpd.service' '/etc/systemd/system/multi-user.target.wants/httpd.service'
```

大家在浏览器（这里以Firefox浏览器为例）的地址栏中输入http://127.0.0.1并按回车键，就可以看到用于提供Web服务的httpd服务程序的默认页面了，如图10-3所示。

[root@linuxprobe ~]# firefox
第10章 使用Apache服务部署静态网站。第10章 使用Apache服务部署静态网站。

图10-3  httpd服务程序的默认页面

10.2 配置服务文件参数
需要提醒大家的是，前文介绍的httpd服务程序的安装和运行，仅仅是httpd服务程序的一些皮毛，我们依然有很长的道路要走。在Linux系统中配置服务，其实就是修改服务的配置文件，因此，还需要知道这些配置文件的所在位置以及用途，httpd服务程序的主要配置文件及存放位置如表10-1所示。

表10-1  Linux系统中的配置文件

服务目录	/etc/httpd
主配置文件	/etc/httpd/conf/httpd.conf
网站数据目录	/var/www/html
访问日志	/var/log/httpd/access_log
错误日志	/var/log/httpd/error_log
大家在首次打开httpd服务程序的主配置文件，可能会吓一跳—竟然有353行！这得至少需要一周的时间才能看完吧？！但是，大家只要仔细观看就会发现刘遄老师在这里调皮了。因为在这个配置文件中，所有以井号（#）开始的行都是注释行，其目的是对httpd服务程序的功能或某一行参数进行介绍，我们不需要逐行研究这些内容。

在httpd服务程序的主配置文件中，存在三种类型的信息：注释行信息、全局配置、区域配置，如图10-4所示。

第10章 使用Apache服务部署静态网站。第10章 使用Apache服务部署静态网站。
图10-4  httpd服务程序的主配置文件的构成

各位读者在学习第4章时已经接触过注释信息，因此这里主要讲解全局配置参数与区域配置参数的区别。顾名思义，全局配置参数就是一种全局性的配置参数，可作用于对所有的子站点，既保证了子站点的正常访问，也有效减少了频繁写入重复参数的工作量。区域配置参数则是单独针对于每个独立的子站点进行设置的。就像在大学食堂里面打饭，食堂负责打饭的阿姨先给每位同学来一碗标准大小的白饭（全局配置），然后再根据每位同学的具体要求盛放他们想吃的菜（区域配置）。在httpd服务程序主配置文件中，最为常用的参数如表10-2所示。

表10-2  配置httpd服务程序时最常用的参数以及用途描述

ServerRoot	服务目录
ServerAdmin	管理员邮箱
User	运行服务的用户
Group	运行服务的用户组
ServerName	网站服务器的域名
DocumentRoot	网站数据目录
Listen	监听的IP地址与端口号
DirectoryIndex	默认的索引页页面
ErrorLog	错误日志文件
CustomLog	访问日志文件
Timeout	网页超时时间，默认为300秒
从表10-2中可知，DocumentRoot参数用于定义网站数据的保存路径，其参数的默认值是把网站数据存放到/var/www/html目录中；而当前网站普遍的首页面名称是index.html，因此可以向/var/www/html目录中写入一个文件，替换掉httpd服务程序的默认首页面，该操作会立即生效。

在执行上述操作之后，再在Firefox浏览器中刷新httpd服务程序，可以看到该程序的首页面内容已经发生了改变，如图10-5所示。

[root@linuxprobe ~]# echo "Welcome To LinuxProbe.Com" > /var/www/html/index.html
[root@linuxprobe ~]# firefox
第10章 使用Apache服务部署静态网站。第10章 使用Apache服务部署静态网站。
图10-5  httpd服务程序的首页面内容已经被修改

大家在完成这个实验之后，是不是信心爆棚了呢？！在默认情况下，网站数据是保存在/var/www/html目录中，而如果想把保存网站数据的目录修改为/home/wwwroot目录，该怎么操作呢？且看下文。

第1步：建立网站数据的保存目录，并创建首页文件。

[root@linuxprobe ~]# mkdir /home/wwwroot
[root@linuxprobe ~]# echo "The New Web Directory" > /home/wwwroot/index.html
第2步：打开httpd服务程序的主配置文件，将约第119行用于定义网站数据保存路径的参数DocumentRoot修改为/home/wwwroot，同时还需要将约第124行用于定义目录权限的参数Directory后面的路径也修改为/home/wwwroot。配置文件修改完毕后即可保存并退出。

```shell
[root@linuxprobe ~]# vim /etc/httpd/conf/httpd.conf 
………………省略部分输出信息………………
113 
114 #
115 # DocumentRoot: The directory out of which you will serve your
116 # documents. By default, all requests are taken from this directory, bu t
117 # symbolic links and aliases may be used to point to other locations.
118 #
119 DocumentRoot "/home/wwwroot"
120 
121 #
122 # Relax access to content within /var/www.
123 #
124 <Directory "/home/wwwroot">
125 AllowOverride None
126 # Allow open access:
127 Require all granted
128 </Directory>
………………省略部分输出信息………………
[root@linuxprobe ~]#
```

第3步：重新启动httpd服务程序并验证效果，浏览器刷新页面后的内容如图10-6所示。奇怪！为什么看到了httpd服务程序的默认首页面？按理来说，只有在网站的首页面文件不存在或者用户权限不足时，才显示httpd服务程序的默认首页面。我们在尝试访问http://127.0.0.1/index.html页面时，竟然发现页面中显示“Forbidden,You don't have permission to access /index.html on this server.”。而这一切正是SELinux在捣鬼。

[root@linuxprobe ~]# systemctl restart httpd
[root@linuxprobe ~]# firefox
第10章 使用Apache服务部署静态网站。第10章 使用Apache服务部署静态网站。

图10-6  httpd服务程序的默认首页面

出现问题?大胆提问!

因读者们硬件不同或操作错误都可能导致实验配置出错，请耐心再仔细看看操作步骤吧，不要气馁~

10.3 SELinux安全子系统

SElinux域：限制服务功能
SElinux安全上下文：限制文件能够被那些服务所访问

SELinux（Security-Enhanced Linux）是美国国家安全局在Linux开源社区的帮助下开发的一个强制访问控制（MAC，Mandatory Access Control）的安全子系统。RHEL 7系统使用SELinux技术的目的是为了让各个服务进程都受到约束，使其仅获取到本应获取的资源。

例如，您在自己的电脑上下载了一个美图软件，当您全神贯注地使用它给照片进行美颜的时候，它却在后台默默监听着浏览器中输入的密码信息，而这显然不应该是它应做的事情（哪怕是访问电脑中的图片资源，都情有可原）。SELinux安全子系统就是为了杜绝此类情况而设计的，它能够从多方面监控违法行为：对服务程序的功能进行限制（SELinux域限制可以确保服务程序做不了出格的事情）；对文件资源的访问限制（SELinux安全上下文确保文件资源只能被其所属的服务程序进行访问）。

刘遄老师经常会把“SELinux域”和“SELinux安全上下文”称为是Linux系统中的双保险，系统内的服务程序只能规规矩矩地拿到自己所应该获取的资源，这样即便黑客入侵了系统，也无法利用系统内的服务程序进行越权操作。但是，非常可惜的是，SELinux服务比较复杂，配置难度也很大，加之很多运维人员对这项技术理解不深，从而导致很多服务器在部署好Linux系统后直接将SELinux禁用了；这绝对不是明智的选择。

SELinux服务有三种配置模式，具体如下。

- enforcing：强制启用安全策略模式，将拦截服务的不合法请求。

- permissive：遇到服务越权访问时，只发出警告而不强制拦截。

- disabled：对于越权的行为不警告也不拦截。

本书中的所有实验都是在强制启用安全策略模式下进行的，虽然在禁用SELinux服务后确实能够减少报错几率，但这在生产环境中相当不推荐。建议大家检查一下自己的系统，查看SELinux服务主配置文件中定义的默认状态。如果是permissive或disabled，建议赶紧修改为enforcing。

```shell
[root@linuxprobe ~]# vim /etc/selinux/config
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
# enforcing - SELinux security policy is enforced.
# permissive - SELinux prints warnings instead of enforcing.
# disabled - No SELinux policy is loaded.
SELINUX=enforcing
# SELINUXTYPE= can take one of these two values:
# targeted - Targeted processes are protected,
# minimum - Modification of targeted policy. Only selected processes are protected. 
# mls - Multi Level Security protection.
SELINUXTYPE=targeted
```

SELinux服务的主配置文件中，定义的是SELinux的默认运行状态，可以将其理解为系统重启后的状态，因此它不会在更改后立即生效。可以使用getenforce命令获得当前SELinux服务的运行模式：

```shell
[root@linuxprobe ~]# getenforce
Enforcing
```

为了确认确实是因为SELinux而导致的，可以用setenforce [0|1]命令修改SELinux当前的运行模式（0为禁用，1为启用）。注意，这种修改只是临时的，在系统重启后就会失效：

```shell
[root@linuxprobe ~]# setenforce 0
[root@linuxprobe ~]# getenforce
Permissive
```

如果想要永久生效
```shell
vim /etc/selinux/config
SELINUX=permissive
```

再次刷新网页，就会看到正常的网页内容了，如图10-7所示。可见，问题确实是出在了SELinux服务上面。

```shell
[root@linuxprobe wwwroot]# firefox
```

现在，我们来回忆一下前面的操作中到底是哪里出问题了呢？

httpd服务程序的功能是允许用户访问网站内容，因此SELinux肯定会默认放行用户对网站的请求操作。但是，我们将网站数据的默认保存目录修改为了/home/wwwroot，而这就产生问题了。在6.1小节中讲到，/home目录是用来存放普通用户的家目录数据的，而现在，httpd提供的网站服务却要去获取普通用户家目录中的数据了，这显然违反了SELinux的监管原则。

现在，我们把SELinux服务恢复到强制启用安全策略模式，然后分别查看原始网站数据的保存目录与当前网站数据的保存目录是否拥有不同的SELinux安全上下文值：

```shell
[root@linuxprobe ~]# setenforce 1
[root@linuxprobe ~]# ls -Zd /var/www/html
drwxr-xr-x. root root system_u:object_r:httpd_sys_content_t:s0 /var/www/html
[root@linuxprobe ~]# ls -Zd /home/wwwroot
drwxrwxrwx. root root unconfined_u:object_r:home_root_t:s0 /home/wwwroot
```

在文件上设置的SELinux安全上下文是由用户段、角色段以及类型段等多个信息项共同组成的。其中，用户段system_u代表系统进程的身份，角色段object_r代表文件目录的角色，类型段httpd_sys_content_t代表网站服务的系统文件。由于SELinux服务实在太过复杂，现在大家只需要简单熟悉SELinux服务的作用就可以，刘遄老师未来会在本书的进阶篇中单独拿出一个章节仔细讲解SELinux服务。

针对当前这种情况，我们只需要使用semanage命令，将当前网站目录/home/wwwroot的SELinux安全上下文修改为跟原始网站目录的一样就可以了。

semanage命令 

RHEL 5,6 chcon 安全上下文 
RHEL 7 semanage 安全上下文+域

semanage命令用于管理SELinux的策略，格式为“semanage [选项] [文件]”。

SELinux服务极大地提升了Linux系统的安全性，将用户权限牢牢地锁在笼子里。semanage命令不仅能够像传统chcon命令那样—设置文件、目录的策略，还可以管理网络端口、消息接口（这些新特性将在本章后文中涵盖）。使用semanage命令时，经常用到的几个参数及其功能如下所示：

- -l参数用于查询；

- -a参数用于添加；

- -m参数用于修改；

- -d参数用于删除。

例如，可以向新的网站数据目录中新添加一条SELinux安全上下文，让这个目录以及里面的所有文件能够被httpd服务程序所访问到：

```shell
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot

# fcontext 安全上下文
# -a 修改
# -t 具体使用的值
# 目录最后面不可以有/

[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/*
```

注意，执行上述设置之后，还无法立即访问网站，还需要使用restorecon命令将设置好的SELinux安全上下文立即生效。在使用restorecon命令时，可以加上-Rv参数对指定的目录进行递归操作，以及显示SELinux安全上下文的修改过程。最后，再次刷新页面，就可以正常看到网页内容了，结果如图10-8所示。 

```shell
[root@linuxprobe ~]# restorecon -Rv /home/wwwroot/
restorecon reset /home/wwwroot context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
restorecon reset /home/wwwroot/index.html context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0

# -R 递归
# -v 显示过程
# restorecon让SELinux的值立即生效

[root@linuxprobe ~]# firefox
```

真可谓是一波三折！原本认为只要把httpd服务程序配置妥当就可以大功告成，结果却反复受到了SELinux安全上下文的限制。所以，建议大家在配置httpd服务程序时，一定要细心、耐心。一旦成功配妥httpd服务程序之后，就会发现SELinux服务并没有那么难。

因为在RHCSA、RHCE或RHCA考试中，都需要先重启您的机器然后再执行判分脚本。因此，建议读者在日常工作中要养成将所需服务添加到开机启动项中的习惯，比如这里就需要添加systemctl enable httpd命令。

### 个人用户主页功能

如果想在系统中为每位用户建立一个独立的网站，通常的方法是基于虚拟网站主机功能来部署多个网站。但这个工作会让管理员苦不堪言（尤其是用户数量很庞大时），而且在用户自行管理网站时，还会碰到各种权限限制，需要为此做很多额外的工作。其实，httpd服务程序提供的个人用户主页功能完全可以胜任这个工作。该功能可以让系统内所有的用户在自己的家目录中管理个人的网站，而且访问起来也非常容易。

#### 第1步

在httpd服务程序中，默认没有开启个人用户主页功能。为此，我们需要编辑下面的配置文件，然后在第17行的UserDir disabled参数前面加上井号（#），表示让httpd服务程序开启个人用户主页功能；同时再把第24行的UserDir public_html参数前面的井号（#）去掉（UserDir参数表示网站数据在用户家目录中的保存目录名称，即public_html目录）。最后，在修改完毕后记得保存。

```shell
[root@linuxprobe ~]# vim /etc/httpd/conf.d/userdir.conf
 1 #
 2 # UserDir: The name of the directory that is appended onto a user's home
 3 # directory if a ~user request is received.
 4 #
 5 # The path to the end user account 'public_html' directory must be
 6 # accessible to the webserver userid. This usually means that ~userid
 7 # must have permissions of 711, ~userid/public_html must have permissions
 8 # of 755, and documents contained therein must be world-readable.
 9 # Otherwise, the client will only receive a "403 Forbidden" message.
 10 #
 11 <IfModule mod_userdir.c>
 12 #
 13 # UserDir is disabled by default since it can confirm the presence
 14 # of a username on the system (depending on home directory
 15 # permissions).
 16 #
 17 #   UserDir disabled #将此行注释

 19 #
 20 # To enable requests to /~user/ to serve the user's public_html
 21 # directory, remove the "UserDir disabled" line above, and uncomment
 22 # the following line instead:
 23 # 
 24   UserDir public_html # 取消注释，public_html每个用户保存自己网站的路径
 25 </IfModule>
 26 
 27 #
 28 # Control access to UserDir directories. The following is an example
 29 # for a site where these directories are restricted to read-only.
 30 #
 31 <Directory "/home/*/public_html">
 32 AllowOverride FileInfo AuthConfig Limit Indexes
 33 Options MultiViews Indexes SymLinksIfOwnerMatch IncludesNoExec
 34 Require method GET POST OPTIONS
 35 </Directory>
```

#### 第2步

在用户家目录中建立用于保存网站数据的目录及首页面文件。另外，还需要把家目录的权限修改为755，保证其他人也有权限读取里面的内容。

```shell
[root@linuxprobe home]# su - linuxprobe
Last login: Fri May 22 13:17:37 CST 2017 on :0
[linuxprobe@linuxprobe ~]$ mkdir public_html
[linuxprobe@linuxprobe ~]$ echo "This is linuxprobe's website" > public_html/index.html
[linuxprobe@linuxprobe ~]$ chmod -Rf 755 /home/linuxprobe
```

#### 第3步

重新启动httpd服务程序，在浏览器的地址栏中输入网址，其格式为“网址/~用户名”（其中的波浪号是必需的，而且网址、波浪号、用户名之间没有空格），从理论上来讲就可以看到用户的个人网站了。不出所料的是，系统显示报错页面，如图10-9所示。这一定还是SELinux惹的祸。

图10-9  禁止访问用户的个人网站

第4步：思考这次报错的原因是什么。httpd服务程序在提供个人用户主页功能时，该用户的网站数据目录本身就应该是存放到与这位用户对应的家目录中的，所以应该不需要修改家目录的SELinux安全上下文。但是，前文还讲到了SELinux域的概念。SELinux域确保服务程序不能执行违规的操作，只能本本分分地为用户提供服务。httpd服务中突然开启的这项个人用户主页功能到底有没有被SELinux域默认允许呢？

接下来使用getsebool命令查询并过滤出所有与HTTP协议相关的安全策略。其中，off为禁止状态，on为允许状态。

```shell
[root@linuxprobe ~]# getsebool -a | grep http
httpd_anon_write --> off
httpd_builtin_scripting --> on
httpd_can_check_spam --> off
httpd_can_connect_ftp --> off
httpd_can_connect_ldap --> off
httpd_can_connect_mythtv --> off
httpd_can_connect_zabbix --> off
httpd_can_network_connect --> off
httpd_can_network_connect_cobbler --> off
httpd_can_network_connect_db --> off
httpd_can_network_memcache --> off
httpd_can_network_relay --> off
httpd_can_sendmail --> off
httpd_dbus_avahi --> off
httpd_dbus_sssd --> off
httpd_dontaudit_search_dirs --> off
httpd_enable_cgi --> on
httpd_enable_ftp_server --> off
httpd_enable_homedirs --> off
httpd_execmem --> off
httpd_graceful_shutdown --> on
httpd_manage_ipa --> off
httpd_mod_auth_ntlm_winbind --> off
httpd_mod_auth_pam --> off
httpd_read_user_content --> off
httpd_run_stickshift --> off
httpd_serve_cobbler_files --> off
httpd_setrlimit --> off
httpd_ssi_exec --> off
httpd_sys_script_anon_write --> off
httpd_tmp_exec --> off
httpd_tty_comm --> off
httpd_unified --> off
httpd_use_cifs --> off
httpd_use_fusefs --> off
httpd_use_gpg --> off
httpd_use_nfs --> off
httpd_use_openstack --> off
httpd_use_sasl --> off
httpd_verify_dns --> off
named_tcp_bind_http_port --> off
prosody_bind_http_port --> off
```

面对如此多的SELinux域安全策略规则，实在没有必要逐个理解它们，我们只要能通过名字大致猜测出相关的策略用途就足够了。比如，想要开启httpd服务的个人用户主页功能，那么用到的SELinux域安全策略应该是httpd_enable_homedirs吧？大致确定后就可以用setsebool命令来修改SELinux策略中各条规则的布尔值了。大家一定要记得在setsebool命令后面加上-P参数，让修改后的SELinux策略规则永久生效且立即生效。随后刷新网页，其效果如图10-10所示。

```shell
[root@linuxprobe ~]# setsebool -P httpd_enable_homedirs=on
[root@linuxprobe ~]# firefox
```

图10-10  正常看到个人用户主页面中的内容

有时，网站的拥有者并不希望直接将网页内容显示出来，只想让通过身份验证的用户访客看到里面的内容，这时就可以在网站中添加口令功能了。

第1步：先使用htpasswd命令生成密码数据库。-c参数表示第一次生成；后面再分别添加密码数据库的存放文件，以及验证要用到的用户名称（该用户不必是系统中已有的本地账户）。

```shell
[root@linuxprobe ~]# htpasswd -c /etc/httpd/passwd linuxprobe
New password:此处输入用于网页验证的密码
Re-type new password:再输入一遍进行确认
Adding password for user linuxprobe
```

第2步：编辑个人用户主页功能的配置文件。把第31～35行的参数信息修改成下列内容，其中井号（#）开头的内容为刘遄老师添加的注释信息，可将其忽略。随后保存并退出配置文件，重启httpd服务程序即可生效。

```shell
[root@linuxprobe ~]# vim /etc/httpd/conf.d/userdir.conf
27 #
28 # Control access to UserDir directories. The following is an example
29 # for a site where these directories are restricted to read-only.
30 #
31 <Directory "/home/*/public_html">
32 AllowOverride all # 是否允许伪静态，数据库资料转换为静态文件形式，实际并没有
# all表示开启，none表示关闭。
#刚刚生成出来的密码验证文件保存路径
33 authuserfile "/etc/httpd/passwd"
#当用户尝试访问个人用户网站时的提示信息
34 authname "My privately website"
35 authtype basic
#用户进行账户密码登录时需要验证的用户名称
36 require user linuxprobe
37 </Directory>
[root@linuxprobe ~]# systemctl restart httpd
```

此后，当用户再想访问某个用户的个人网站时，就必须要输入账户和密码才能正常访问了。另外，验证时使用的账户和密码是用htpasswd命令生成的专门用于网站登录的口令密码，而不是系统中的用户密码，请不要搞错了。登录界面如图10-11所示。

图10-11  网站提示需要输入账户和密码才能访问

### 虚拟网站主机功能

如果每台运行Linux系统的服务器上只能运行一个网站，那么人气低、流量小的草根站长就要被迫承担着高昂的服务器租赁费用了，这显然也会造成硬件资源的浪费。在虚拟专用服务器（Virtual Private Server，VPS）与云计算技术诞生以前，IDC服务供应商为了能够更充分地利用服务器资源，同时也为了降低购买门槛，于是纷纷启用了虚拟主机功能。

服务器中存在多个网站时，有跨站攻击。

利用虚拟主机功能，可以把一台处于运行状态的物理服务器分割成多个“虚拟的服务器”。但是，该技术无法实现目前云主机技术的硬件资源隔离，让这些虚拟的服务器共同使用物理服务器的硬件资源，供应商只能限制硬盘的使用空间大小。出于各种考虑的因素（主要是价格低廉），目前依然有很多企业或个人站长在使用虚拟主机的形式来部署网站。

Apache的虚拟主机功能是服务器基于用户请求的不同IP地址、主机域名或端口号，实现提供多个网站同时为外部提供访问服务的技术，如图10-12所示，用户请求的资源不同，最终获取到的网页内容也各不相同。如果大家之前没有做过网站，可能不太理解其中的原理，等一会儿搭建出实验环境并看到实验效果之后，您一定就会明白了。

虚拟主机基于方式

- IP地址
- 主机域名
- 端口号


图10-12 用户请求网站资源[原图附件]

#### 基于IP地址

如果一台服务器有多个IP地址，而且每个IP地址与服务器上部署的每个网站一一对应，这样当用户请求访问不同的IP地址时，会访问到不同网站的页面资源。而且，每个网站都有一个独立的IP地址，对搜索引擎优化也大有裨益。因此以这种方式提供虚拟网站主机功能不仅最常见，也受到了网站站长的欢迎（尤其是草根站长）。

刘遄老师在第4章和第9章分别讲解了用于配置网络的两种方法，大家在实验中和工作中可随意选择。就当前的实验来讲，需要配置的IP地址如图10-13所示。在配置完毕并重启网卡服务之后，记得检查网络的连通性，确保三个IP地址均可正常访问，如图10-14所示（这很重要，一定要测试好，然后再进行下一步!）。

图10-13  使用nmtui命令配置网络参数

第1步：分别在/home/wwwroot中创建用于保存不同网站数据的3个目录，并向其中分别写入网站的首页文件。每个首页文件中应有明确区分不同网站内容的信息，方便我们稍后能更直观地检查效果。第10章 使用Apache服务部署静态网站。第10章 使用Apache服务部署静态网站。

图10-14  分别检查3个IP地址的连通性

```shell
[root@linuxprobe ~]# mkdir -p /home/wwwroot/10
[root@linuxprobe ~]# mkdir -p /home/wwwroot/20
[root@linuxprobe ~]# mkdir -p /home/wwwroot/30
[root@linuxprobe ~]# echo "IP:192.168.10.10" > /home/wwwroot/10/index.html
[root@linuxprobe ~]# echo "IP:192.168.10.20" > /home/wwwroot/20/index.html
[root@linuxprobe ~]# echo "IP:192.168.10.30" > /home/wwwroot/30/index.html
```

```shell
# 确保iptables没有干扰
iptables -F
# 保存防火墙状态
service iptables save
```

第2步：在httpd服务的配置文件中大约113行处开始，分别追加写入三个基于IP地址的虚拟主机网站参数，然后保存并退出。记得需要重启httpd服务，这些配置才生效。

```shell
[root@linuxprobe ~]# vim /etc/httpd/conf/httpd.conf
# apache不区分大小写
………………省略部分输出信息………………
113 <VirtualHost 192.168.10.10>
114 DocumentRoot /home/wwwroot/10
115 ServerName www.linuxprobe.com
116 <Directory /home/wwwroot/10 >
117 AllowOverride None
118 Require all granted #允许所有授权
119 </Directory> #目录结束符
120 </VirtualHost> #虚拟主机结束符

121 <VirtualHost 192.168.10.20>
122 DocumentRoot /home/wwwroot/20
123 ServerName bbs.linuxprobe.com
124 <Directory /home/wwwroot/20 >
125 AllowOverride None
126 Require all granted
127 </Directory>
128 </VirtualHost>

129 <VirtualHost 192.168.10.30>
130 DocumentRoot /home/wwwroot/30
131 ServerName tech.linuxprobe.com
132 <Directory /home/wwwroot/30 >
133 AllowOverride None
134 Require all granted
135 </Directory>
136 </VirtualHost>
………………省略部分输出信息………………
[root@linuxprobe ~]# systemctl restart httpd
```

第3步：此时访问网站，则会看到httpd服务程序的默认首页面。大家现在应该立刻就反应过来—这是SELinux在捣鬼。由于当前的/home/wwwroot目录及里面的网站数据目录的SELinux安全上下文与网站服务不吻合，因此httpd服务程序无法获取到这些网站数据目录。我们需要手动把新的网站数据目录的SELinux安全上下文设置正确（见前文的实验），并使用restorecon命令让新设置的SELinux安全上下文立即生效，这样就可以立即看到网站的访问效果了，如图10-15所示。

```shell
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/10
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/10/*
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/20
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/20/*
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/30
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/30/*
[root@linuxprobe ~]# restorecon -Rv /home/wwwroot
restorecon reset /home/wwwroot context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
restorecon reset /home/wwwroot/10 context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
restorecon reset /home/wwwroot/10/index.html context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
restorecon reset /home/wwwroot/20 context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
restorecon reset /home/wwwroot/20/index.html context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
restorecon reset /home/wwwroot/30 context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
restorecon reset /home/wwwroot/30/index.html context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
[root@linuxprobe ~]# firefox
```

图10-15  基于不同的IP地址访问虚拟主机网站

#### 基于主机域名

当服务器无法为每个网站都分配一个独立IP地址的时候，可以尝试让Apache自动识别用户请求的域名，从而根据不同的域名请求来传输不同的内容。在这种情况下的配置更加简单，只需要保证位于生产环境中的服务器上有一个可用的IP地址（这里以192.168.10.10为例）就可以了。由于当前还没有介绍如何配置DNS解析服务，因此需要手工定义IP地址与域名之间的对应关系。/etc/hosts是Linux系统中用于强制把某个主机域名解析到指定IP地址的配置文件。简单来说，只要这个文件配置正确，即使网卡参数中没有DNS信息也依然能够将域名解析为某个IP地址。

- linux /etc/hosts
- windows c:/windows/system32/drivers/etc/hosts 上google，屏蔽升级，DNS污染，ssr，vpn，openvz，pptpd

第1步：手工定义IP地址与域名之间对应关系的配置文件，保存并退出后会立即生效。可以通过分别ping这些域名来验证域名是否已经成功解析为IP地址。

```shell
[root@linuxprobe ~]# vim /etc/hosts
127.0.0.1 localhost localhost.localdomain localhost4 localhost4.localdomain4
::1 localhost localhost.localdomain localhost6 localhost6.localdomain6
192.168.10.10 www.linuxprobe.com bbs.linuxprobe.com tech.linuxprobe.com
# IP地址 域名（空格间隔）
[root@linuxprobe ~]# ping -c 4 www.linuxprobe.com
PING www.linuxprobe.com (192.168.10.10) 56(84) bytes of data.
64 bytes from www.linuxprobe.com (192.168.10.10): icmp_seq=1 ttl=64 time=0.070 ms
64 bytes from www.linuxprobe.com (192.168.10.10): icmp_seq=2 ttl=64 time=0.077 ms
64 bytes from www.linuxprobe.com (192.168.10.10): icmp_seq=3 ttl=64 time=0.061 ms
64 bytes from www.linuxprobe.com (192.168.10.10): icmp_seq=4 ttl=64 time=0.069 ms
--- www.linuxprobe.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 2999ms
rtt min/avg/max/mdev = 0.061/0.069/0.077/0.008 ms
[root@linuxprobe ~]#
```

第2步：分别在/home/wwwroot中创建用于保存不同网站数据的三个目录，并向其中分别写入网站的首页文件。每个首页文件中应有明确区分不同网站内容的信息，方便我们稍后能更直观地检查效果。

```shell
[root@linuxprobe ~]# mkdir -p /home/wwwroot/www
[root@linuxprobe ~]# mkdir -p /home/wwwroot/bbs
[root@linuxprobe ~]# mkdir -p /home/wwwroot/tech
[root@linuxprobe ~]# echo "WWW.linuxprobe.com" > /home/wwwroot/www/index.html
[root@linuxprobe ~]# echo "BBS.linuxprobe.com" > /home/wwwroot/bbs/index.html
[root@linuxprobe ~]# echo "TECH.linuxprobe.com" > /home/wwwroot/tech/index.html
```

第3步：在httpd服务的配置文件中大约113行处开始，分别追加写入三个基于主机名的虚拟主机网站参数，然后保存并退出。记得需要重启httpd服务，这些配置才生效。

```shell
[root@linuxprobe ~]# vim /etc/httpd/conf/httpd.conf
………………省略部分输出信息………………
113 <VirtualHost 192.168.10.10>
114 DocumentRoot "/home/wwwroot/www"
115 ServerName "www.linuxprobe.com"
116 <Directory "/home/wwwroot/www">
117 AllowOverride None
118 Require all granted
119 </directory> 
120 </VirtualHost>
121 <VirtualHost 192.168.10.10>
122 DocumentRoot "/home/wwwroot/bbs"
123 ServerName "bbs.linuxprobe.com"
124 <Directory "/home/wwwroot/bbs">
125 AllowOverride None
126 Require all granted
127 </Directory>
128 </VirtualHost>
129 <VirtualHost 192.168.10.10>
130 DocumentRoot "/home/wwwroot/tech"
131 ServerName "tech.linuxprobe.com"
132 <Directory "/home/wwwroot/tech">
133 AllowOverride None
134 Require all granted
135 </directory>
136 </VirtualHost>
………………省略部分输出信息………………
```

第4步：因为当前的网站数据目录还是在/home/wwwroot目录中，因此还是必须要正确设置网站数据目录文件的SELinux安全上下文，使其与网站服务功能相吻合。最后记得用restorecon命令让新配置的SELinux安全上下文立即生效，这样就可以立即访问到虚拟主机网站了，效果如图10-16所示。

```shell
[root@linuxprobe ~]# ls -ldZ /var/www/html 
drwxr-xr-x. root system_u:object_r:httpd_sys_content_t:s0 /var/www/html
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/www
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/www/*
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/bbs
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/bbs/*
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/tech
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/tech/*
[root@linuxprobe ~]# restorecon -Rv /home/wwwroot
reset /home/wwwroot context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
restorecon reset /home/wwwroot/www context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
restorecon reset /home/wwwroot/www/index.html context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
restorecon reset /home/wwwroot/bbs context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
restorecon reset /home/wwwroot/bbs/index.html context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
restorecon reset /home/wwwroot/tech context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
restorecon reset /home/wwwroot/tech/index.html context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
[root@linuxprobe ~]# firefox 
```

图10-16  基于主机域名访问虚拟主机网站

#### 基于端口号

基于端口号的虚拟主机功能可以让用户通过指定的端口号来访问服务器上的网站资源。在使用Apache配置虚拟网站主机功能时，基于端口号的配置方式是最复杂的。因此我们不仅要考虑httpd服务程序的配置因素，还需要考虑到SELinux服务对新开设端口的监控。一般来说，使用80、443、8080等端口号来提供网站访问服务是比较合理的，如果使用其他端口号则会受到SELinux服务的限制。

在接下来的实验中，我们不但要考虑到目录上应用的SELinux安全上下文的限制，还需要考虑SELinux域对httpd服务程序的管控。

第1步：分别在/home/wwwroot中创建用于保存不同网站数据的两个目录，并向其中分别写入网站的首页文件。每个首页文件中应有明确区分不同网站内容的信息，方便我们稍后能更直观地检查效果。

```shell
[root@linuxprobe ~]# mkdir -p /home/wwwroot/6111
[root@linuxprobe ~]# mkdir -p /home/wwwroot/6222
[root@linuxprobe ~]# echo "port:6111" > /home/wwwroot/6111/index.html
[root@linuxprobe ~]# echo "port:6222" > /home/wwwroot/6222/index.html
```

第2步：在httpd服务配置文件的第43行和第44行分别添加用于监听6111和6222端口的参数。

```shell
[root@linuxprobe ~]# vim /etc/httpd/conf/httpd.conf 
………………省略部分输出信息……………… 
 33 #
 34 # Listen: Allows you to bind Apache to specific IP addresses and/or
 35 # ports, instead of the default. See also the <VirtualHost>
 36 # directive.
 37 #
 38 # Change this to Listen on specific IP addresses as shown below to 
 39 # prevent Apache from glomming onto all bound IP addresses.
 40 #
 41 #Listen 12.34.56.78:80
 42 Listen 80
 43 Listen 6111
 44 Listen 6222
………………省略部分输出信息……………… 
```

第3步：在httpd服务的配置文件中大约113行处开始，分别追加写入两个基于端口号的虚拟主机网站参数，然后保存并退出。记得需要重启httpd服务，这些配置才生效。

```shell
[root@linuxprobe ~]# vim /etc/httpd/conf/httpd.conf
………………省略部分输出信息……………… 
113 <VirtualHost 192.168.10.10:6111>
114 DocumentRoot "/home/wwwroot/6111"
115 ServerName www.linuxprobe.com
116 <Directory "/home/wwwroot/6111">
117 AllowOverride None
118 Require all granted
119 </Directory> 
120 </VirtualHost>
121 <VirtualHost 192.168.10.10:6222>
122 DocumentRoot "/home/wwwroot/6222"
123 ServerName bbs.linuxprobe.com
124 <Directory "/home/wwwroot/6222">
125 AllowOverride None
126 Require all granted
127 </Directory>
128 </VirtualHost>
………………省略部分输出信息………………
```

第4步：因为我们把网站数据目录存放在/home/wwwroot目录中，因此还是必须要正确设置网站数据目录文件的SELinux安全上下文，使其与网站服务功能相吻合。最后记得用restorecon命令让新配置的SELinux安全上下文立即生效。

```shell
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/6111
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/6111/*
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/6222
[root@linuxprobe ~]# semanage fcontext -a -t httpd_sys_content_t /home/wwwroot/6222/*
[root@linuxprobe ~]# restorecon -Rv /home/wwwroot/
restorecon reset /home/wwwroot context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
restorecon reset /home/wwwroot/6111 context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
restorecon reset /home/wwwroot/6111/index.html context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
restorecon reset /home/wwwroot/6222 context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
restorecon reset /home/wwwroot/6222/index.html context unconfined_u:object_r:home_root_t:s0->unconfined_u:object_r:httpd_sys_content_t:s0
[root@linuxprobe ~]# systemctl restart httpd
Job for httpd.service failed. See 'systemctl status httpd.service' and 'journalctl -xn' for details.
```

见鬼了！在妥当配置httpd服务程序和SELinux安全上下文并重启httpd服务后，竟然出现报错信息。这是因为SELinux服务检测到6111和6222端口原本不属于Apache服务应该需要的资源，但现在却以httpd服务程序的名义监听使用了，所以SELinux会拒绝使用Apache服务使用这两个端口。我们可以使用semanage命令查询并过滤出所有与HTTP协议相关且SELinux服务允许的端口列表。

```shell
[root@linuxprobe ~]# semanage port -l | grep http
http_cache_port_t tcp 8080, 8118, 8123, 10001-10010
http_cache_port_t udp 3130
http_port_t tcp 80, 81, 443, 488, 8008, 8009, 8443, 9000
pegasus_http_port_t tcp 5988
pegasus_https_port_t tcp 5989
```

第5步：SELinux允许的与HTTP协议相关的端口号中默认没有包含6111和6222，因此需要将这两个端口号手动添加进去。该操作会立即生效，而且在系统重启过后依然有效。设置好后再重启httpd服务程序，然后就可以看到网页内容了，结果如图10-17所示。

端口号0~65535，不采用固定端口号不冲突即可。

```shell
[root@linuxprobe ~]# semanage port -a -t http_port_t -p tcp 6111
[root@linuxprobe ~]# semanage port -a -t http_port_t -p tcp 6222
[root@linuxprobe ~]# semanage port -l| grep http
http_cache_port_t tcp 8080, 8118, 8123, 10001-10010
http_cache_port_t udp 3130
http_port_t tcp  6222, 6111, 80, 81, 443, 488, 8008, 8009, 8443, 9000
# 允许的端口号
pegasus_http_port_t tcp 5988
pegasus_https_port_t tcp 5989
[root@linuxprobe ~]# systemctl restart httpd
[root@linuxprobe ~]# firefox
```

图10-17  基于端口号访问虚拟主机网站

## Apache的访问控制

Apache可以基于源主机名、源IP地址或源主机上的浏览器特征等信息对网站上的资源进行访问控制。它通过Allow指令允许某个主机访问服务器上的网站资源，通过Deny指令实现禁止访问。在允许或禁止访问网站资源时，还会用到Order指令，这个指令用来定义Allow或Deny指令起作用的顺序，其匹配原则是按照顺序进行匹配，若匹配成功则执行后面的默认指令。比如“Order Allow, Deny”表示先将源主机与允许规则进行匹配，若匹配成功则允许访问请求，反之则拒绝访问请求。

第1步：先在服务器上的网站数据目录中新建一个子目录，并在这个子目录中创建一个包含Successful单词的首页文件。

[root@linuxprobe ~]# mkdir /var/www/html/server
[root@linuxprobe ~]# echo "Successful" > /var/www/html/server/index.html
第2步：打开httpd服务的配置文件，在第129行后面添加下述规则来限制源主机的访问。这段规则的含义是允许使用Firefox浏览器的主机访问服务器上的首页文件，除此之外的所有请求都将被拒绝。使用Firefox浏览器的访问效果如图10-18所示。

```shell
[root@linuxprobe ~]# vim /etc/httpd/conf/httpd.conf
………………省略部分输出信息………………
129 <Directory "/var/www/html/server">
130 SetEnvIf User-Agent "Firefox" ff=1
# set environment if
131 Order allow,deny
132 Allow from env=ff
133 </Directory>
………………省略部分输出信息………………
[root@linuxprobe ~]# systemctl restart httpd
[root@linuxprobe ~]# firefox
```

图10-18  火狐浏览器成功访问

除了匹配源主机的浏览器特征之外，还可以通过匹配源主机的IP地址进行访问控制。例如，我们只允许IP地址为192.168.10.20的主机访问网站资源，那么就可以在httpd服务配置文件的第129行后面添加下述规则。这样在重启httpd服务程序后再用本机（即服务器，其IP地址为192.168.10.10）来访问网站的首页面时就会提示访问被拒绝了，如图10-19所示。

```shell
[root@linuxprobe ~]# vim /etc/httpd/conf/httpd.conf
………………省略部分输出信息………………
129 <Directory "/var/www/html/server">
130 Order allow,deny 
131 Allow from 192.168.10.20
132 </Directory>
………………省略部分输出信息………………
[root@linuxprobe ~]# systemctl restart httpd
[root@linuxprobe ~]# firefox
```
图10-19  因IP地址不符合要求而被拒绝访问
