import copy
from copy import deepcopy
list1=[[1],[2,3]]
list2=deepcopy(list1)
list1[1][1]=5
print(list2)
