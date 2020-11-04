import re

# 指定路径
path = "/home/python/Desktop/pythonABC/"
# 源文件（原来的答案）
originalFile = path + 'originalAnswer.rtf'
# 目标文件 (修改后的文件)
alteredFile = path + 'alteredAnswer.rtf'

# 读取原来的答案
original = open(originalFile, 'r')
text = original.read()
original.close()

# 匹配字符串
pattern = r"(\d+\.\s*\w+/?\w).*\n+"
# 将回车换成tab
newText = re.sub(pattern, r'\1\t', text)

# 将修改好的答案写到文件中去
altered = open(alteredFile, 'w')
altered.write(newText)
altered.close()


