a='xiaoming'
b=29.1261

c='fmale'
#方法一：
print(f'my name is {a},the age is {b},I am a {c}')
#输出结果：my name is xiaoming,the age is 29.1261,I am a fmale
#方法二：
print('my name is {},the age is {},I am a {}'.format(a,b,c))
#输出结果：my name is xiaoming,the age is 29.1261,I am a fmale
print('{:n}'.format(b))
#输出结果：29.1261
print('{:f}'.format(b))   # {:f}表示默认显示（小数点后6位）
#输出结果：29.126100
print('{:.2f}'.format(b)) # {:.2f}表示四舍五入后显示小数点后2位
#输出结果：29.13
print('{:.1f}'.format(b)) # {:.1f}表示四舍五入后显示小数点后1位
#输出结果：29.1
print('{:,.2f}'.format(12000)) # {:,.2f}表示千分位
#输出结果：12,0000
print('|{:<10}|'.format(12))  #左对齐
#输出结果：|12        |
print('|{:^10}|'.format(12))  #居中对齐
#输出结果：|    12    |
print('|{:>10}|'.format(12))  #右对齐
#输出结果：|        12|
print('|{:*<10}|'.format(12))  #左对齐
#输出结果：|12********|
print('|{:-^10}|'.format(12))  #居中对齐
#输出结果：|----12----|
print('|{:@>10}|'.format(12))  #右对齐
#输出结果：|@@@@@@@@12|
print('{:c}'.format(28888))#将int转换为unicode
#输出结果：烘
print('{:b}'.format(12))   #binary:将int转换为二进制
#输出结果：1100
print('{:o}'.format(12))   #octonary将int转换为八进制
#输出结果：14
print('{:d}'.format(12))   #decimalism:将int转换为十进制
#输出结果：12
print('{:x}'.format(12))   #hexadecimal:将int转换为十六进制
#输出结果：c
