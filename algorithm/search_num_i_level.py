#!/usr/bin/env python
# coding=utf-8

import random

"""
    随机选取数组中的一个数，将比这个数小的放在左边，大的放在右边
"""
def random_depart(array,p,q):
    k = random.randint(p,q)
    print k
    x = p
    y = q
    key = array[k]
    print key
    while x < y:
        if array[x] > key and x < k:
            array[k] = array[x]
            k = x 
        if array[y] < key and k < y:
            array[k] = array[y]             
            k = y
#        print x,y,array
        while(array[x] <= key and x < k):
            x += 1
        while(array[y] >= key and k < y):
            y -= 1
        if x >= y:
            break

    array[k] = key
    print array
    return k


"""
    求无序数组array[q],array[r-1] 中第i小的数
"""
def get_num_i_level(array,q,r,i):
    if r-q+1 < i:
        return None
    p = random_depart(array,q,r)
    if p-q+1 == i:
        return array[p]
    if p-q+1 > i:
        return get_num_i_level(array,q,p,i)
    if p-q+1 < i:
        return get_num_i_level(array,p,r,i - (p-q))

a = [9,1,3,4,5,8,0,5]
for i in range(1,100):
    a.append(random.randint(0,100))
print a
print random_depart(a,0,len(a)-1)
print get_num_i_level(a,0,len(a)-1,3)
