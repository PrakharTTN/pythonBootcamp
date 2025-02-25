""" Q3. Programing: From a multi-words and multi-line string, prepare a filter the list of 
 words which have multiple occurances in string. 
 output: Python Using the triple quotes one and to a multiline string. at """

astring = """Python Multiline String Using Triple-Quotes Using the triple quotes style is one of the 
easiest and most common ways to split a large string into a multiline Python string. 
Triple quotes (''' or \""") can be used to create a multiline string. 
It allows you to format text over many lines and include line breaks. 
Put two triple quotes around the multiline Python string, one at the start and one at the end, to define it.""" 


#Converting String to a list with each word as an element with proper formatting
alist=astring.replace('\n', '').split(' ',-1)
adict={}
afinallist=[]

#Adding keys to a dictionary from List, incrementing if already exists
for i in alist:
    if i in adict:
        adict[i]+=1
    else:
        adict[i]=1
#Printing the words which have multiple occurence
"""Output:
Python
from
string
...
"""
for i,j in adict.items():
    if j>1:
        print(i)
