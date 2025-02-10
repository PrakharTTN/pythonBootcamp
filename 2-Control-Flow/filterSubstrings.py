"""Q1. Write a code to filter all sub-strings which has even number of vowel?
 example Input: "I have an input string which contains even and odd numbers of vowels aA aa aaa ae aeo”
 output: I an string which contains and odd of aaa aeo"""

input_string='I have an input string which contains even and odd numbers of vowels aA aa aaa ae aeo'
final_string=""
input_list=input_string.split(' ',-1)
vowels=['a','e','i','o','u']
for i in input_list:
    ctr=0
    for k in i.lower():
        if k in vowels:
            ctr+=1
    if ctr==1 or ctr%2!=0:
        final_string+=i+' '
print(final_string)