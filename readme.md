
MAC Media Access Control

ARP Address Resolve Protocal

Socket  ip:port

OSI

TCP/IP

MTU

TTL Time-To-Live

TCP Transmission Control Protocal
UDP User Datagram Protocal

DHCP Dynamic Host Configuration Protocal

/etc/sysconfig/network-scripts/ifcfg-eth0
/etc/sysconfig/network-scripts/route-eth0
/etc/resolv.conf
/etc/hosts
/etc/sysconfig/network

usr universal shared read-only

/bin /sbin
/lib
/etc
/usr/share/man

/usr/bin /usr/sbin /usr/lib /usr/etc

/usr/local/bin /usr/local/sbin /usr/local/lib /usr/local/etc /usr/local/man

Redhat SUSE : RPM (Redhat Package Manager) , (RPM is Package Manager)
Debian : dpt (debian package tools)

yum : Yellowdog Update Modifier
apt-get 

yum repository

createrepo

XML eXtended Mark Language
JSON 

meta data
primary.xml.gz

/etc/yum.conf
/etc/yum.repos.d/

yum repolist 
yum install -y 
yum install --nogpgcheck

yum localinstall [--nogpgcheck] filename

gcc GNU C Complier
g++

make makefile

automake, makefile.in
autoconf, configure
make install


# tar
# cd
./configure
	--help
	--prefix=/path/to/somewhere
	--sysconfdir=/path/to/conffile
# make
# make install


tar xvf tengine-1.4.2.tar.gz
cd tengine-1.4.2
./configure --prefix=/usr/local/tengine --conf-path=/etc/tengine/tengine.conf
make
make install
/usr/local/tengine/sbin/nginx


1 PATH 
	/etc/profile
	/etc/profile.d  xxx.sh export PATH=$PATH:/path/to/somewhere
2 /lib /usr/lib  
	/etc/ld.so.conf.d/xxx.conf
	ldconfig -v
3 /usr/include
	ln -s /usr/local/tengine/include/* /usr/include/
	ln -s /usr/local/tengine/include /usr/include/tengine
4 /usr/share/man
	man -M /path/to/man_dir command
	/etc/man.config MANPATH


