d1 = {'simple_key':'hello'}
d2 = {'k1':{'k2':'hello'}}
d3 = {'k1':[{'nest_key':['this is deep',['hello']]}]}
d4 = {'k1':[1,2,{'k2':['this is tricky',{'tough':[1,2,['hello']]}]}]}

print("From d1: " + d1.get('simple_key'))
print("From d2: " + d2.get('k1').get('k2'))
print("From d3: " + d3.get('k1')[0].get('nest_key')[1][0])
print("From d4: " + d4.get('k1')[2].get('k2')[1].get('tough')[2][0])