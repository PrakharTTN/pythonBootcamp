"""Q2. Write a code to read a "Python_script.py" as input file and extract following information to prepare a JSON

* all package name which the input Python script use
* all function name which the  input Python script define
* all class name which the  input Python script define
* all the variable name  which the input Python script define

example output:
{
"package": ["os", "itertools"],
"funation": ["function1", "function2"],
"class": ["classA", "classB"],
"variable": ["num", "i", "j"]
}
"""


import os
import json
import keyword

def extract():
    package_names = set() #used set here to make sure no repeated names come
    function_names = set()
    class_names = set()
    variable_names = set()

    with open("python_script.py", 'r') as file:
        content = file.read()
    
    lines = content.splitlines()

    for i in lines:
        i = i.strip()

        if i.startswith('import '):
            package_name = i[len('import '):].strip()
            package_names.add(package_name.split()[0])

        elif i.startswith('from '):
            parts = i[len('from '):].split(' import ')
            package_name = parts[0].strip()
            package_names.add(package_name)

        if i.startswith('def '):
            function_name = i[len('def '):].split('(')[0].strip()
            function_names.add(function_name)

        if i.startswith('class '):
            class_name = i[len('class '):].split('(')[0].strip()
            class_names.add(class_name)

        if '=' in i:
            # To extact left side of assignment operator 
            left_side = i.split('=')[0].strip()
            if left_side and not keyword.iskeyword(left_side):
                variable_names.add(left_side)

    return {
        "packages": list(package_name), #Converting them into list here
        "functions": list(function_names),#  and returning whole as dict for json
        "classes": list(class_names),
        "variables": list(variable_names)
    }

info= extract()
with open("results.json",'w+') as f:
    json.dump(info,f,indent=4)
