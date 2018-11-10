import pymongo
import zipfile
import tarfile
import os
import sys
import json
from collections import namedtuple
import datetime
from driver_defs import *
import time

# --- List of script parameters --- #
# Where is the zip file of the dump located?
DUMP_URI = "./data-export-09-09-18.tar.gz"
# Were to extract all the JSON files?
EXTRACTION_DIR = "./dump_extraction"
# MongoDB URL
MONGO_URI = "aws.kylesilverman.com"
# MongoDB database to use
MONGO_DB = "data"
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
DATA_DIR = EXTRACTION_DIR + "/" + (os.listdir(EXTRACTION_DIR))[0]
for filename in os.listdir(DATA_DIR):
    # only get JSON files
    if filename.endswith(".json"):
        json_files.append(CWD + "/" + DATA_DIR + "/" + filename)


# connect to mongo
MONGO_URI = "mongodb://" + MONGO_USER + ":" + MONGO_PASSWORD + "@" + MONGO_URI + "/" + MONGO_DB
client = pymongo.MongoClient(MONGO_URI)

# grab the DB object that contains all the data for our project
db = client[MONGO_DB]
if not db:
    print(" ERROR: database is of type None")

worker = JsonWorker(db, json_files)
worker.make_dicts()
print(("\n\033[94m\033[1m BEGINNING DB MIGRATIONS \033[0m\n\n"))


for i, log in enumerate(worker.dicts):
    # creates a machine document that describes the machine which produced this log
    machine = worker.create_machine_doc(log)
    # updates the database to isnert this machine docuemnet if it does not exist, update otherwise
    machine.update_db()
    # insert this log into the database.  Arguments to the insert_docs() method is an array to support inserting multiple docs
    inserted_ids = worker.insert_docs([log])
    if i % 50 == 0:
        print(
            (
                "\n"
                + "\033[94m"
                + "\033[1m"
                + " STATUS: %i log documents have been inserted to the database ..."
                + "\033[0m"
                + "\n"
            )
            % i
        )
        time.sleep(1)
    # tells the machine document that was created earlier representing the machine that produced tihs log
    # to update all isntances of the machine doc in the database to contain this log's <ObjectID>
    machine.update_log_links(inserted_ids)


"""
for tenant in tenants:
    db.createCollection(tenant, {
      capped: false,
      autoIndexId: true,
      validator: {
        $jsonSchema: {
          bsonType: "object",
          required: ["serialNumberInserv","date"],
          //TODO Finish schema
        }
      },
      validationLevel: "strict",
      validationAction: "error"
    })
"""
