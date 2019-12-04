# Shell函数

## 定义函数

```shell
function_name()
{
    commmand
}

function function_name()
{
    commmand
}
```

## 调用函数

- 直接使用函数名
- 在函数开始的地方引入函数文件(. /Path/Of/File)

## 参数传递

使用位置变量$1, $2, $3 ...

- shift n
  - 位置变量左移n位
- getopts
  - 获得多个命令行参数

## 检查载入函数和删除函数

- 查看载入函数
  - set
- 删除函数
  - unset function_name

## 函数返回状态值

- $? 状态返回值
- 0代表正常，其他值为错误

