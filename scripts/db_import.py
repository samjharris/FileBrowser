import pymongo
import zipfile
import tarfile
import os
import sys
import json
import datetime
import time

#pip install python-dateutil==2.6.0
import dateutil.parser


# --- List of script parameters --- #
# Where is the zip file of the dump located?
DUMP_URI = "data-export-aggregate-compressed.tar.gz"
# Where to extract all the JSON files?
EXTRACTION_DIR = "data-export-extracted"
# MongoDB URL
MONGO_URI = "aws.kylesilverman.com"
# MongoDB database to use
MONGO_DB = "dump"
# MongoDB user
MONGO_USER = "json_derulo"
# MongoDB password
MONGO_PASSWORD = "Br0ws3r!"


if len(sys.argv) > 1:
    DUMP_URI = sys.argv[1]
# Current working directory
CWD = os.getcwd()
# extract dump JSON files to a folder
tar = tarfile.open(DUMP_URI)
tar.extractall(EXTRACTION_DIR)
tar.close()

# get all JSON file names that were jsut extracted by the tarfile object
json_files = []
for filename in os.listdir(EXTRACTION_DIR):
    # only get JSON files
    if filename.endswith(".json"):
        if filename.startswith('._'):
          continue
        json_files.append(CWD + "/" + EXTRACTION_DIR + "/" + filename)

# connect to mongo
MONGO_URI = "mongodb://" + MONGO_USER + ":" + MONGO_PASSWORD + "@" + MONGO_URI + "/" + MONGO_DB
client = pymongo.MongoClient(MONGO_URI)

# grab the DB object that contains all the data for our project
db = client[MONGO_DB]
if not db:
    print(" ERROR: database is of type None")
    exit(1)

if "dataLogs" not in db.list_collection_names():
    print(" Warning: collection 'dataLogs' does not exist in database. Creating it.")
    

# get cursor to d='dataLogs' collection in database
dataLogs_collection = db.get_collection("dataLogs")

# create an empty list to hold all of the json files as dictionaries
json_dicts = []

# open, convert, and add each proper file to the json_dicts list
for filePath in enumerate(json_files):
    try:
        with open(filePath[1]) as data_file:
            cur_dict = json.load(data_file)
            json_dicts.append(cur_dict)
    except IOError as e:
        print
        print("IOError: Unable to open .json file. Terminating execution.")
        exit(1)

# add the useful field 'historyIndex' to each proper json file
for cur_properLog in json_dicts:
  cur_properLog['historyIndex'] = 0
  cur_properSerial = cur_properLog['serialNumberInserv']
  
  # convert the ISO formatted date stored in the JSON  
  # to a python dateutil objectfor comparisons 
  cur_properDate = cur_properLog['date']
  cur_properDate_dateutil = dateutil.parser.parse(cur_properDate)
  
  # get a cursor to a list off all logs in the database with a matching serial number
  cursor_dbLog = dataLogs_collection.find({'serialNumberInserv' : cur_properSerial})

  # declare and fill a list of all relevant info (i.e. '_id', 'date', 'historyIndex')
  # this list contains one entry for each log in the database with serial numbers matching cur_properSerial
  list_matching_dbLog = []
  for cur_dbLog in cursor_dbLog:
    curElem = {}
    curElem['id'] = cur_dbLog.get('_id')
    curElem['date'] = dateutil.parser.parse(cur_dbLog.get('date'))
    curElem['hist'] = cur_dbLog.get('historyIndex')
    list_matching_dbLog.append(curElem)

  # if there are no other logs in the database for this serial number, we can add directly  
  if len(list_matching_dbLog) == 0:
    cur_properLog['historyIndex'] = 1
    dataLogs_collection.insert_one(cur_properLog)
    continue

  # if there are other logs we must re-order the history indexes 
  else:

    # add identifying information about the current proper log file
    # into the list of logs with matching serial numbers, for ordering
    propElem = {}
    propElem['id'] = 'PROPERLOG'
    propElem['date'] = cur_properDate_dateutil
    propElem['hist'] = 0
    list_matching_dbLog.append(propElem)

    # sort the list by date newest->oldest (bubble sort)
    # note, dateutil comparator defined such that more
    # recent dates are treated as 'greater' than older ones
    for i in range(len(list_matching_dbLog)-1,0,-1):
        for j in range(i):
            if list_matching_dbLog[j]['date'] > list_matching_dbLog[j+1]['date']:
                temp = list_matching_dbLog[j]
                list_matching_dbLog[j] = list_matching_dbLog[j+1]
                list_matching_dbLog[j+1] = temp

    # since the list is now sorted, we can easily
    # adjust hist fields for each entry in the list of 
    # all logs with matching serial number
    i = 1
    for curElem in list_matching_dbLog:
      curElem['hist'] = i
      i += 1

    # now, update each entry with matching serial numbers
    # in the database, using the information we have been
    # storing in our list
    for curElem in list_matching_dbLog:

      # if the current item is the new proper log that does not
      # exist in the database already, we handle with an insert
      if curElem['id'] == 'PROPERLOG':
        cur_properLog['historyIndex'] = curElem['hist']
        dataLogs_collection.insert_one(cur_properLog)

      # otherwise, the current item exists and we handle
      # with an update
      else:

        # find the matching entry by unique _id field we have stored, 
        # then update the db with the other info we have stored
        dataLogs_collection.find_one_and_update({'_id' : curElem['id']},{'$set': {'historyIndex' : curElem['hist']}})
