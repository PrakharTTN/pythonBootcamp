import csv
import json
def json_to_csv():
    '''This block reads JSON file and writes them into a CSV file'''
    with open("username.json", 'r') as json_file, open("csvusername.csv", 'w') as csv_file:
        my_json_file=json.load(json_file)
        writer=csv.DictWriter(csv_file, delimiter=';', fieldnames = my_json_file[0].keys())
        writer.writeheader()
        for i in my_json_file:
            writer.writerow(i)
        print("Converted JSON to CSV.")
json_to_csv()
    
