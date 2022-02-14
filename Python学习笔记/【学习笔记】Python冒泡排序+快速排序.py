
'''
1.冒泡排序：    
   #重复地走访过要排序的数列，一次比较相邻的两个元素，如果他们的顺序错误就把他们交换过来。走访数列的工作是重复地进行直到没有再需要交换，也就是说该数列已经排序完成。

	【算法步骤】：
	（1）比较相邻的元素。如果第一个比第二个大，就交换他们两个。
	（2）对每一对相邻元素作同样的工作，从开始第一对到结尾的最后一对。这步做完后，最后的元素会是最大的数。
	（3）针对所有的元素重复以上的步骤，除了最后一个。
	（4）持续每次对越来越少的元素重复上面的步骤，直到没有任何一对数字需要比较。
'''
def maopao(array):
	if len(array)<2:
		return array
	else:
		for i in range(1,len(array)):
			for j in range(0,len(array)-i):
				if array[j]>array[j+1]:
					array[j],array[j+1]=array[j+1],array[j]
	return array
		
'''
2.快速排序：
   #总体来说就是选一个基准值，把小于基准值的分一拨，把大于基准值的分到另一拨，然后递归。
	【算法步骤】：
	（1）在数列之中，选择一个元素作为”基准”（pivot），或者叫比较值。
	（2）数列中所有元素都和这个基准值进行比较，如果比基准值小就移到基准值的左边，如果比基准值大就移到基准值的右边。
	（3）以基准值左右两边的子列作为新数列，不断重复第一步和第二步，直到所有子集只剩下一个元素为止。
'''
def kuaisu(array):
	if len(array)<2:
		return array
	else:
		mid=array[len(array)//2]
		left,right=[],[]
		for i in array:
			if i >mid:
				right.append(i)
			elif i<mid:
				left.append(i)
	return kuaisu(left)	+ [mid] + kuaisu(right)

'''
3.选择排序：
   #
	【算法步骤】：
   （1)首先在未排序序列中找到最小（大）元素，存放到排序序列的起始位置。
	(2)再从剩余未排序元素中继续寻找最小（大）元素，然后放到已排序序列的末尾。
	(3)重复第二步，直到所有元素均排序完毕。
'''	
def xuanze(array):
	for i in range(len(array)-1):
		min_index=i
		for j in range(i+1,len(array)):
			if array[i]<array[min_index]:
				min_index=j
		if  i!=min_index:
			array[i],array[min_index]=array[min_index],array[i]
	return array
	
array=[11, 99, 33, 69, 77, 88, 55, 36, 39, 66, 44, 22]
print(f'冒泡排序结果为：{maopao(array)}')
print(f'快速排序结果为：{kuaisu(array)}')
print(f'选择排序的结果为:{xuanze(array)}')