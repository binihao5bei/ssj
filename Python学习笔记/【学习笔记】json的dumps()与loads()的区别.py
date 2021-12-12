#1.json.dumps()与json.loads()的区别：

import json
info_dict = {'name': 'Joe', 'age': 20, 'job': 'driver'}

#json.dumps(dict）是将字典转化为json字符串
a=json.dumps(info_dict)
print(a)
print(type(a))
'''
输出结果：
{"name": "Joe", "age": 20, "job": "driver"}
<class 'str'>
'''


#json.loads(str）是将json字符串转化为字典
b=json.loads(a)
print(b)
print(type(b))
'''
输出结果：
{'name': 'Joe', 'age': 20, 'job': 'driver'}
<class 'dict'>
'''



#2.json.dumps()、json.loads()与json.dump()、json.load()的区别：

#json.dump( )、json.load()与json.dumps()、json.loads()基本原理一致，但json.dump( )、json.load()是对json文件的读写操作，而json.dumps()、json.loads()是对json数据的操作
with  open('data.json', 'w') as f:
	#json.dump()需要2个参数：要储存的数据+要储存数据的文件，侧重于“写”
	#下面例子表示将数据data储存在文件data.json中
	json.dump(data,f)
	
	
	
	
	#json.load()只需要1个参数：储存数据的文件，侧重于“读”
	#下面例子表示读取json文件data.json中的数据到内存中
with  open('data.json', 'w') as f:
	data=json.load(f)	
	
	