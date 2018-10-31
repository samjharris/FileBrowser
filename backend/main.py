################################################################################
# Imports ######################################################################
################################################################################

from flask import Flask, session, request

from flask_pymongo import PyMongo

from passlib.hash import sha256_crypt

from bson.json_util import loads, dumps

################################################################################
# App Setup ####################################################################
################################################################################

app = Flask(__name__)

app.secret_key = "JsOnDeRulO"

################################################################################
# Status Codes #################################################################
################################################################################

STATUS_200 = dumps({}), 200

STATUS_401 = dumps({}), 401

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


# init the connection to mongo

mongo = PyMongo(app, MONGO_URI)

################################################################################
# Logout Route #################################################################
################################################################################

@app.route("/logout", methods = ["POST"])

def logout():

    session.clear()

################################################################################
# Login Route ##################################################################
################################################################################

@app.route("/login", methods = ["POST"])

def login():

    
    # extract the args from the query string
    
    tenant = request.args.get("tenant")

    pswd = request.args.get("password")


    # search for the user according to the query args
    
    user = mongo.db.users.find_one({"tenant": tenant})


    if user is not None:

        # get the pswd field

        conf = user["password"]


        if sha256_crypt.verify(pswd, conf):

            # storing the session info
            
            session["tenant"] = tenant 

            # return successful

            return STATUS_200


    # unauthorized user
    
    return STATUS_401
    

################################################################################
# Get List of Machines #########################################################
################################################################################

@app.route("/machines", methods = ["POST"])

def machines():

    if "tenant" in session:

        machines = mongo.db.machines.find({

            # get machines with the tenant
            
            "tenants": session["tenant"]

        })

        # return data with success
        
        return dumps(machines), 200


    # unauthorized user
    
    return STATUS_401


################################################################################
# Get List of Logs #############################################################
################################################################################

@app.route("/machines/<ssn>/logs", methods = ["POST"])

def logs():

    if "tenant" in session:

        # attempt to find the machine specified by params

        machine = mongo.db.machines.find_one({"ssn": ssn})


        if machine is not None:

            logs = mongo.db.logs({

                # get objects from logs prop

                "_id": {"$in": machine.logs}

            }) 


            # return machine's logs

            return dumps(logs), 200


        # ssn non-existant

        return STATUS_200


    # unauthorized user
    
    return STATUS_401

################################################################################
# Run App ######################################################################
################################################################################

if __name__ == "__name__":

    app.run(debug = True)

################################################################################
################################################################################
################################################################################
