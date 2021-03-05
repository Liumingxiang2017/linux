# python安装

## Linux平台Python软件包源码安装

1. 下载：https://www.python.org/downloads/source/
2. 在linux中解压：tar zxvf /usr/local/src/Python-3.9.2.tgz；cd /usr/local/src/Python-3.9.2
3. 准备编译环境：yum install gcc
4. 准备安装依赖包: zlib, openssl。python的pip需要依赖这两个包 yum install zlib* openssl*
5. 预编译：./configure --prefix=/usr/python-3.9.2 --enable-optimizations 指定安装目录（最后一级目录会自动创建），防止分散安装
./configure --help（查看使用帮助）
6. 编译：make 大概7分钟
7. 安装：make install
8. 配置系统环境变量： 
	- 方法一：vim ~/.bash_profile 或者vim ~/.bashrc, 追加PATH=$PATH:/usr/python-3.9.2/bin, 并重新加载使其立刻生效source ~/.bashrc 
	- 方法二：PYTHON_HOME=/usr/python-3.9.2；PAHT=$PATH:$PYTHON_HOME/bin，并使重新加载其立刻生效source ~/.bashrc, 优点是当python安装目录变化后仅需改变PYTHON_HOME变量
	- /etc/profile 整个系统的环境变量配置文件，~/.bashrc 当前用户的环境变量配置文件，优先使用后者
9. 补充安装一个工具ipython：执行命令pip3 install ipython3，注意使用python3时尽量对应使用3的工具，ipython3可以使用shell内部命令


解决linux中，Python版本升级后，交互模式下方向键、退格键等出现乱码的问题
由于系统缺少了readline相关模块，没有安装readline-devel模块，所以只要安装下即可。
yum list | grep readline
yum -y install readline-devel.x86_64

安装完成readline-devel后，再重新编译安装Python3.6即可解决问题。

## windows安装
1. exe文件安装
2. 高级系统设置
    - 方法一：PYTHON_HOME=C:\python3 PATH=.;%PYTHON_HOME%;%PYTHON_HOME%\Scripts; 因为pip在Scripts文件夹中
    - 方法二：PYTHON_HOME=C:\python3 PATH=保留原来的;%PYTHON_HOME%;%PYTHON_HOME%\Scripts; 因为pip在Scripts文件夹中


安装pycharm，sublime软件

## 安装java

tar -zxvf jdk-8u241-linux-x64.tar.gz

mv jdk1.8.0_241/ /opt/

vim /etc/profile

在文本的最后一行粘贴如下
#java environment
export JAVA_HOME=/opt/jdk1.8.0_241
export CLASSPATH=.:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export PATH=$PATH:$JAVA_HOME/bin

生效配置   运行
source /etc/profile 
java -version

