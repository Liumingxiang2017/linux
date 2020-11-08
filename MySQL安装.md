问题：OFFICE连接Excel数据源提示此链接需要安装一个或多个其他组件才能使用

直接最快解决策略
1. 缺少插件(mysql-connector-net-8.0.18)
2. 链接地址：https://dev.mysql.com/downloads/connector/net/
3.下载安装并重启Excel

## mac安装mysql
1. 安装安装包
2. 配置路径 ~/.bash_profile 中的路径,即添加export PATH=$PATH:/usr/local/mysql/bin

mac中打开当前路径的图形化界面：open .


忘记sql的root密码
```sql
# 修改mysql 配置文件, [mysql]下添加skip-grant-tables
vi /etc/my.cnf
# 重启数据库
service mysqld restart
# 进入mysql (-u和root可以不需要空格，-p和密码也可以不要)
mysql -u root
# 换mysql数据表：
mysql> use mysql;
# 更换密码，root_password替换成你想要的密码
mysql> update mysql.user set authentication_string=password('root_password') where user='root'; 
```

