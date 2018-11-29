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

def create(argv):

    if len(argv) < 3:

        print("Invalid args")

        # create-user.py 
        
        #  - <username> 
        
        #  - <tenant>
        
        #  - <password>

        return "Error: args"


    # default value

    pswd = "password"

    if len(argv) == 4:

        pswd = argv[3]


    # hash the password for security
    
    hashed = sha256_crypt.hash(pswd)

    
    client.data.users.insert_one({

        "username": argv[1],

        "tenant": argv[2],

        "password": hashed
        
    })

################################################################################
# Parse Args ###################################################################
################################################################################

create(sys.argv)

################################################################################
################################################################################
################################################################################
