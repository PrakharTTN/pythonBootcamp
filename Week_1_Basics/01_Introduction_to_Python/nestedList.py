"""Q6. Reassign 'hello' in this nested list to say 'goodbye' instead:
"""

list3 = [1,2,[3,4,'hello']]
print("Before Reassign: ", list3)
list3[2][2]='goodbye'
print("After Reassign: ", list3)