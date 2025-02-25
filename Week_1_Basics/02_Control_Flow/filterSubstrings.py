"""Q1. Write a code to filter all sub-strings which has even number of vowel?
 example Input: "I have an input string which contains even and odd numbers of vowels aA aa aaa ae aeo”
 output: I an string which contains and odd of aaa aeo"""

input_string='I have an input string which contains even and odd numbers of vowels aA aa aaa ae aeo'

#Creating an empty string
final_string=""


#Splitting the string into list
input_list=input_string.lower().split(' ',-1)

#Declaring vowels in a list
vowels=['a','e','i','o','u']

#Iterating in the list
for i in input_list:
    ctr=0
    #Iterating each letter from the element in the list and if it is in vowels, incrementing ctr
    for k in i:
        if k in vowels:
            ctr+=1
    #After iterating through each letter, checking whether the word had odd vowels.
    if ctr%2!=0:
        final_string+=i+' '
#Since sample output had odd vowels, we filter out all the even ones
print(final_string)