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

def create(tenant, pswd = "password"):

    # hash the password for security
    
    hashed = sha256_crypt.hash(pswd)

    
    client.data.users.insert_one({

        "tenant": tenant,

        "password": hashed
        
    })

################################################################################
# Parse Args ###################################################################
################################################################################

if len(sys.argv) == 2:

    tenant = sys.argv[1]
    
    create(tenant)


if len(sys.argv) == 3:

    tenant = sys.argv[1]

    psword = sys.argv[2]

    create(tenant, psword)

################################################################################
################################################################################
################################################################################
