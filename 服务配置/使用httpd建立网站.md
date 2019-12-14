# 使用httpd建立网站

1. 查看已安装的httpd
    - rpm -qa | grep httpd
2. 查看rpm包内容
    - rpm -ql | more
    - 配置文件/etc/httpd/conf/httpd.conf
    - /etc/rc.d/init.d/httpd 说明可以通过system V的方式对httpd控制
3. 启动httpd
    - service httpd start 或者 /etc/init.d/httpd start
4. 配置文件
    - /etc/httpd/conf/httpd.conf 
    - ServerRoot "/etc/httpd"
    - PidFile run/httpd.pid 其中run是基于ServerRoot基础之上的
    - Timeout 120 连接超过120s则断线
    - \<IfModule worker.c>...\</IfModule>设置连接数等等
    - Listen 80 监听窗口
    - UserDir public_html 用户家目录下创建public_html文件夹，在该文件夹中建立网页文件，增加apache对该文件执行权限，则可以通过http://127.0.0.1/~username/file.html访问
    - Options Indexs FollowSymLinks 在内容目录中不存在index.html时，则以列表方式展示
    
/etc/hosts 简单的地址映射文件