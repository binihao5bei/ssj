data = [{'name':'小K','score':100},  
    {'name':'小J','score':98},  
    {'name':'小Q','score':100},  
    {'name':'小K','score':100}]  
datalists = [] # 用于存储去重后的list  
values = []  # 用于存储当前已有的值  
for d in data:  
    if d["name"] not in values:  
        datalists.append(d)  
    values.append(d["name"])  
print(datalists)