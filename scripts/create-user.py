################################################################################
# Imports ######################################################################
################################################################################

from passlib.hash import sha256_crypt

import sys, pymongo

################################################################################
# Database Setup ###############################################################
################################################################################

MONGO_URI = "mongodb://{}:{}@{}/{}"

MONGO_HOST = "aws.kylesilverman.com"

MONGO_DATABASE = "data"

MONGO_USER = "json_derulo"

MONGO_PASSWORD = "Br0ws3r!"


# create the formatted string

MONGO_URI = MONGO_URI.format(

    MONGO_USER, MONGO_PASSWORD,

    MONGO_HOST, MONGO_DATABASE

)


# create connection to the AWS database

client = pymongo.MongoClient(MONGO_URI)

################################################################################
# Database Setup ###############################################################
################################################################################

def create(username, tenant, pswd = "password"):

    # hash the password for security
    
    hashed = sha256_crypt.hash(pswd)

    
    client.data.users.insert_one({

    	"username": username,

        "tenant": tenant,

        "password": hashed
        
    })

################################################################################
# Parse Args ###################################################################
################################################################################


if len(sys.argv) == 3:

    username = sys.argv[1]

    tenant = sys.argv[2]

    create(username, tenant)

if len(sys.argv) == 4:

    username = sys.argv[1]

    tenant = sys.argv[2]

    psword = sys.argv[3]

    create(username, tenant, psword)

################################################################################
################################################################################
################################################################################
