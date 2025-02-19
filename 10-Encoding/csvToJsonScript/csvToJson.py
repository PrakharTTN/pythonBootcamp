import csv
import json


def csv_to_json():
    """This block reads csv file and dumps data to json file with proper formatting."""
    with open("username.csv", "r") as csv_file, open("username.json", "w") as json_file:
        my_file = csv.DictReader(csv_file, delimiter=";", quotechar='"')
        json_list = [i for i in my_file]
        json.dump(json_list, json_file, indent=4)
        print("File converted from CSV to JSON.")


csv_to_json()
