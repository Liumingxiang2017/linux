# LVM逻辑卷

LVM：
	扩展
	逻辑卷的缩减
	快照卷

10G, VG

vgcreate VG_NAME /PATH/TO/PV
	-s #: PE大小，默认为4MB
	
lvcreate -n LV_NAME -L #G VG_NAME


练习：创建一个由两个物理卷组成的大小为20G的卷组myvg，要求其PE大小为16M；而后在此卷组中创建一个大小为5G的逻辑卷lv1，此逻辑卷要能在开机后自动挂载至/users目录，且支持ACL功能；

缩减前面创建的逻辑卷lv1的大小至2G；

一、扩展逻辑卷；
lvextend
	-L [+]# /PATH/TO/LV

2G, +3G
5G	
	
resize2fs
	resize2fs -p /PATH/TO/LV


二、缩减逻辑卷；
注意：1、不能在线缩减，得先卸载；
	  2、确保缩减后的空间大小依然能存储原有的所有数据；
	  3、在缩减之前应该先强行检查文件，以确保文件系统处于一至性状态；
df -lh
umount 
e2fsck -f
	  	  
resize2fs 
	resize2fs /PATH/TO/PV 3G

lvreduce -L [-]# /PATH/TO/LV

重新挂载


三、快照卷
1、生命周期为整个数据时长；在这段时长内，数据的增长量不能超出快照卷大小；
2、快照卷应该是只读的；
3、跟原卷在同一卷组内；


lvcreate 
	-s
	-p r|w
	
lvcreate -L # -n SLV_NAME -p r /PATH/TO/LV
