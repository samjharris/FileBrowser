import pymongo
import zipfile
import os
import json
from collections import namedtuple

#--- List of script parameters
#Where is the zip file of the dump located?
DUMP_URI = './dump.tar'
#Were to extract all the JSON files?
EXTRACTION_DIR = '.'
#MongoDB URL
MONGO_URI = 'aws.kylesilverman.com'
#MongoDB database to use
MONGO_DB = 'dump'
#MongoDB user
MONGO_USER = 'json_derulo'
#MongoDB password
MONGO_PASSWORD = 'Br0ws3r!'


#extract dump JSON files to a folder
zip_ref = zipfile.ZipFile(DUMP_URI, 'r')
zip_ref.extractall(EXTRACTION_DIR)
zip_ref.close()

#get all JSON file references
json_files = []
for filename in os.listdir(EXTRACTION_DIR):
  if filename.endswith(".json"):
    json_files.append(filename)



#connect to mongo
client = pymongo.MongoClient('mongodb://' + MONGO_USER + ':' + MONGO_PASSWORD + '@' + MONGO_URI + '/' + MONGO_DB)
db = client[MONGO_DB]


tenants = []

//TODO:gather set of tenantids

for(tenant in tenants):
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

#TODO LOOP THROUGH ALL JSON files
#   (!machineExists)
#      Create MachineDoc
#      Add fields <last_updated : "string">, <datadocs : "array">
#
#   CreateDataDoc
#   Update
