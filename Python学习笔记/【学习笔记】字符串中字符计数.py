from collections import Counter

a = "hkskja;ldsjaf;hdsll;lahfbl;hl;ahlf;h"
'''
方法一：
num=Counter(a)
print(num)

方法二：
def statistics(_str):
	new_str = list(set(_str))  #set去重
	dic = {i: _str.count(i) for i in new_str}
	return dic
if __name__ == "__main__":
	_str = a
	dic = statistics(_str)
	print(dic)
	'''
#方法三：
list_qc=list(set(a))   #set去重
dic={i:a.count(i) for i in list_qc}
print(dic)
