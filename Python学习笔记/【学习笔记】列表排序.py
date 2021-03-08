#对列表排序，简单的就直接用内置的 sort 或 sorted 方法。

sort和sorted排序区别：

1、sort 方法会直接改变原序列的排序。

```
list_tail = [1, 23, 24, 99, 45, 68]
list_add = list_tail.sort()
print(list_tail)
print(list_add)

# 输出结果
[1, 23, 24, 45, 68, 99]
None
```
从输出结果可以看出，list.sort() 直接在原序列 list_tail  上进行了排序，新序列 list_add 返回的是 None。

2、sorted 方法不会改变原序列的排序，它会新建一个排好序的序列对象。

```
list_tail = [1, 23, 24, 99, 45, 68]
list_add = sorted(list_tail)
print(list_tail)
print(list_add)

# 输出结果
[1, 23, 24, 99, 45, 68]
[1, 23, 24, 45, 68, 99]
```
从输出结果可以看出，sorted(list) 并没有改变原序列 list_tail 的排序，而是新建一个排好序的序列对象。

sort 和 sorted 默认都是升序排列，如果要降序排列的话，直接在方法里加入 reverse=True 即可。

```
list_add = list_tail.sort(reverse=True)

list_add = sorted(list_tail, reverse=True)
```

列表排序，复杂的就要用到算法的知识了，常见的排序算法有：冒泡排序、选择排序、插入排序、希尔排序、归并排序、快速排序、堆排序、计数排序、桶排序、基数排序等