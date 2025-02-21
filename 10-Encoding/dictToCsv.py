import io

def dict_to_comma():
    '''This block of code uses an io string to imitate a file and writes the dictionary into comma seperated string'''
    
    output_string=io.StringIO()
    data={"name": "Alice", "age": 30, "city": "New York"}
    
    output_string.write(','.join(data.keys()) + '\n')    
    output_string.write(','.join(str(data[i])for i in data )+'\n')
    output_string.seek(0)
    print(output_string.read())

dict_to_comma()
