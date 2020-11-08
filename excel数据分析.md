# EXCEL (excellent)

常见对象
- 工作簿：工作表的集合
- 工作表：数据的集合
- 字段：数据的列标题
- 记录：一行数据

数据类型
- 数字类型（默认右对齐）
- 字符类型（默认左对齐）

数据导入
- 从网站导入
- 从文本导入
- 从mysql数据库导入

创建数据库,可以用命令行，也可以用Navicat Premium

```
show databases;
create database demo charset=utf8;
use demo;
create table info (id int unsigned primary key auto_increment, name varchar(10) not null);
show tables;
insert into info values (0,'zf'), (0,'gy');
select * from info;
```

服务器：localhost:3306
数据库：demo

## EXCEL基本使用

### 拆分数据
快速填充
- 方法1：填充第二个单元格看到淡出的建议列表，立即按Enter
- 方法2：选中第一个单元格，单击“开始>填充>快速填充”。
快速填充快捷键"Ctrl+E"

基于分隔符分列：选中需要分隔的内容，单击“数据——分列”

使用公式拆分：LEFT/RIGHT/FIND/LEN
### 转置 将行列对掉
- 复制数据，“开始>粘贴按钮小箭头>选择性粘贴>转置”
- 使用TRANSPOSE数组公式转置，Ctrl+shift+Enter完成数组公式。

### 排序和筛选
开始>排序和筛选>升序/筛选

对两列进行排序：
1. 先对某一列进行排序
2. 单击“开始>排序和筛选>自定义排序>添加条件”

### 表格
表转化成表格：插入>表格；快捷键Ctrl+T

表格中的计算列：按alt=，按Enter等于求和。

清除表格格式：设计>转换为区域

### 下拉列表
下拉列表做法1
1. 数据>数据验证>允许>序列；
2. 数据验证页面，来源框输入各分类，用英文逗号隔开。
下拉列表最佳做法：引用表格
1. 将分类做成表格 Ctrl+T，建议放在另外一个工作表中以防随意更改。
2. 数据>数据验证>允许>序列；来源框选中表格中的分类

### 分析
快速制作图表
1. Ctrl+Q 快速分析：包括格式化，图表，汇总，表格，迷你图

### 组合图表
1. 插入>推荐的图表>所有图表>组合，勾选最后一个字段对应的次坐标轴复选框；
2. 删除第一个字段数据产生的图形。
3. 更换水平（分类）轴标签：选择数据源>编辑>选定水平分类数据

### 数据透视表
插入>数据透视表

其他相关知识：
- 推荐书目《Excel2010数据处理与分析》
- Power pivot 超级数据透视表，一般用来建模
- Power query
- Power map 结合bing
- tableau public

## EXCEL函数

中位数：MEDIAN