## HTML表单

表单用于获取不同类型的用户输入，是页面设计不可缺少的一个元素，通过表单可以更好的与服务器进行交互。

```html
<form> </form>表单
<input> 输入域
<textarea> 文本域
<label> 控制标签
<fieldset> 定义域
<legend> 域的标题
<select> 选择列表
<optgroup> 选项组
<option> 下拉列表中的选项
<button> 按钮
```

```html
<!DOCTYPE html>
<html>
    <form action="">
        <input type="text">

        <input type="password">
        <!-- 多选框 -->
        <input type="checkbox">
        <input type="checkbox">
        <!-- 单选框 -->
        <input type="radio" name="sex">
        <input type="radio" name="sex">
        <!-- 下拉列表 -->
        <select name="" id="">
            <option value=""></option>
            <option value=""></option>
            <option value=""></option>
        </select>
        <!-- 文本域 -->
        <textarea name="" id="" cols="30" rows="10"></textarea>
        <!-- 按钮 -->
        <input type="button" value="">
        <!-- 提交 -->
        <input type="submit" value="">
        
    </form>
</html>
```

## PHP环境搭建

1. 安装xampp （包含windows linux macos版本）
2. 启动apachewebserver， mysql database
3. xampp/htdocs目录下就可以运行php脚本了

eclipse （强大的java开发工具），也可以写php，但需要安装插件

安装插件过程help——>install new software——>选中版本——>language——>php Development toll (PDT)

安装好以后，切换为php语言环境，新建项目，切换工作空间到htdocs目录下，就可以编写及调试了。



## 表单提交数据与PHP交互

```html
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title>表单与PHP交互</title>
</head>
<body>
    <form action="http://pathOfPhpFile" method="GET">
        用户名: <input type="text" name="name" id="">
        密码: <input type="password" name="password" id="">
        <br>
        <input type="submit" value="提交">
    </form>
</body>
</html>

<?php
echo "用户名：".$_GET['name']."<br>密码：".$GET['password'];

<html>
<head lang="en">
    <meta charset="UTF-8">
    <title>表单与PHP交互</title>
</head>
<body>
    <form action="http://pathOfPhpFile" method="POST">
        用户名: <input type="text" name="name">
        密码: <input type="password" name="password">
        <br>
        <input type="submit" value="提交">
    </form>
</body>
</html>
```

```php
<?php
echo "用户名：".$_POST['name']."<br>密码：".$_POST['password'];
```

GET 可以做资源定位

