import random
list1=['a','b','c','d','e','f','g','h','i','j','k']

num=input('抽取幸运人数：')
list2=[]

for i in range(int(num)):
    luck=random.choice(list1)
    print('第{}个幸运儿是{}'.format(i+1,luck))
    list2.append(luck)
print("本次抽奖的幸运儿是：{}".format(list2))
print("本次抽奖的非幸运儿是：{}，继续加油啦".format(list(set(list1).difference(set(list2)))))   #先将list转化为set集合，然后根据集合的属性（set(list1).difference(set(list2))来筛选出2个集合不同的元素