"""String with name of animals seperated by space, can be repeated. Every animal should be named by a unique code"""


def animal_codex(animal_list: list) -> dict:
    """This function is to create unique code for each animal"""
    starting_code = 97  # ascii value of a is 97
    animal_dict = {}
    for i in animal_list:
        if i not in animal_dict:
            animal_dict[i] = chr(starting_code)  # converts ascii value to word
            starting_code += 1

    return animal_dict


def animal_code(animal_dict: dict, animal_list: list) -> str:
    """This function generates the final code from the dictionary."""
    final_code = ""
    for i in animal_list:
        final_code += str(animal_dict[i])
    return final_code


animal_string = "cat dog hen cat"  # Output "abca"
animal_list = animal_string.lower().split(" ")
animal_dict = animal_codex(animal_list)
final_code = animal_code(animal_dict, animal_list)
print("Final Code: ", final_code)

for i in animal_list:
    print(hash(i))


from datetime import datetime

a = datetime.now().strptime("%Y-%M-D - %HH:%MM:%SS")
print(a)
