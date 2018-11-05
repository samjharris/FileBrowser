import json
import os
import sys


def convert(json):
    # Path to example.json file
    CWD = os.getcwd()
    JSON_Example_File_Path = "%s/%s" % (CWD, json)

    # Dictionary holding example.json values
    Example_Dict = {}

    # open example.json parse values and store them in Dictionary
    try:
        with open(JSON_Example_File_Path) as data_file:
            Example_Dict = json.load(data_file)
    except IOError as e:
        print
        print("IOError: Unable to open json file. Terminating execution")
        exit(1)

    print(Example_Dict)
