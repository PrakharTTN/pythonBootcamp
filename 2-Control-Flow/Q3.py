#Programing: From a multi-words and multi-line string, prepare a filter the list of 
# words which have multiple occurances in string. 
# output: Python Using the triple quotes one and to a multiline string. at

astring = """Python Multiline String Using Triple-Quotes Using the triple quotes style is one of the 
easiest and most common ways to split a large string into a multiline Python string. 
Triple quotes (''' or \""") can be used to create a multiline string. 
It allows you to format text over many lines and include line breaks. 
Put two triple quotes around the multiline Python string, one at the start and one at the end, to define it.""" 

alist=astring.replace('\n', '').split(' ',-1)
adict={}
afinallist=[]
for i in alist:
    if i in adict.keys():
        adict[i]+=1
    else:
        adict[i]=1
for i,j in adict.items():
    if j>1:
        print(i)
