import copy
from copy import deepcopy

list1 = [[1], [2, 3]]
list2 = deepcopy(list1)
list3 = list1.copy()
list1[1][1] = 5
print(list1)
print(list2)
print(list3)
