################################################################################
# Imports ######################################################################
################################################################################

from flask import Flask, session, request

from flask_pymongo import PyMongo

from passlib.hash import sha256_crypt

from bson.json_util import loads, dumps

from flask_cors import CORS

################################################################################
# App Setup ####################################################################
################################################################################

app = Flask(__name__)
#cors = CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app)

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

# paging variables

SYS_PER_PAGE = 20

# init the connection to mongo
mongo = PyMongo(app, MONGO_URI)


################################################################################
# Logout Route #################################################################
################################################################################

@app.route("/logout", methods = ["POST"])

def logout():

    session.clear()

    return STATUS_200

################################################################################
# Login Route ##################################################################
################################################################################

@app.route("/login", methods = ["POST"])

def login():

    
    # extract the args from the query string
    username = request.args.get("username")

    pswd = request.args.get("password")

    if(authenticate_user(username, pswd)):

        return STATUS_200

    # unauthorized user
    
    return STATUS_401
    

################################################################################
# Get List of Machines #########################################################
################################################################################

@app.route("/machines", methods = ["POST"])

def machines():

    username = request.args.get("username")

    pswd = request.args.get("password")

    pagenum = int(request.args.get("page"))

    sortCode = request.args.get("sort")

    sortField = get_sort_field(sortCode)
    sortOrder = get_sort_order(sortCode)

    search = request.args.get("search")

    if(authenticate_user(username, pswd)):

    	#Get tenant associated with username

        user = mongo.db.users.find_one(
                {'username':username}
            )
        tenant = user['tenant']
        


        #First, handle cases when we are searching:
        if(search != ""):
        	search_machines = mongo.db.dataLogs.find( {'authorized.tenants':tenant,   
        											   '$or': [ {'serialNumberInserv': 
        											   				{'$regex': ('.*'+search+'.*'),'$options':'si'}}, 
        											   			{'system.companyName': 
        											   				{'$regex': ('.*'+search+'.*'),'$options':'si'}} ],
        											   'historyIndex':1},
                						   			  {'_id':0, 'historyIndex':0}
            							   ).sort(
            							   	 sortField,sortOrder
            							   ).skip( (pagenum - 1) * SYS_PER_PAGE ).limit( SYS_PER_PAGE )

           


        	search_numSystems = int(search_machines.count())

        	search_datadump = {'numSystems':search_numSystems,'machines':search_machines}
        	return dumps(search_datadump), 200
        


        #Get all files associated with <tenant> 
		#only files with historyIndex=1 (most recent)
		#strips fields '_id' and 'historyIndex'
		#skips to pagenum
		#limits to SYS_PER_PAGE
        machines = mongo.db.dataLogs.find( {'authorized.tenants':tenant, 'historyIndex':1},
                						   {'_id':0, 'historyIndex':0}
            							   ).sort(
            							   	 sortField,sortOrder
            							   ).skip( (pagenum - 1) * SYS_PER_PAGE ).limit( SYS_PER_PAGE )

        numSystems = int(machines.count())

        datadump = {'numSystems':numSystems,'machines':machines}

        # return data with success
        
        return dumps(datadump), 200


    # unauthorized user
    
    return STATUS_401


################################################################################
# Get History #############################################################
################################################################################

@app.route("/history", methods = ["POST"])

def history():
	username = request.args.get("username")
	pswd = request.args.get("password")
	serialnumber = request.args.get("sni")

	if(authenticate_user(username, pswd)):
		user = mongo.db.users.find_one({'username':username})
		tenant = user['tenant']

		#Get all files associated with <serialnumber> 
		#in ascending numerical order w/ respect to historyIndex.
		#strips fields '_id' and 'historyIndex'
		#limits to 10 most recent
		histories = mongo.db.dataLogs.find( {'serialNumberInserv':serialnumber, 'authorized.tenants':tenant},
											{'_id':0, 'historyIndex':0}
											).sort('historyIndex').limit(10)

		#return data with success
		return dumps(histories), 200


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

def authenticate_user(username, pswd):

    # search for the user according to the query args
    
    user = mongo.db.users.find_one({"username":username})


    if user is not None:

        # get the pswd field

        conf = user["password"]


        if sha256_crypt.verify(pswd, conf):

            # return successful

            return True

    # unauthorized user
    
    return False

def get_sort_field(code):
	if code == 'fslh':
		return 'capacity.total.freePct'
	elif code == 'fshl':
		return 'capacity.total.freePct'
	elif code == 'snlh':
		return 'serialNumberInserv'
	elif code == 'snhl':
		return 'serialNumberInserv'
	elif code == 'cnaz':
		return 'system.companyName'
	elif code == 'cnza':
		return 'system.companyName'
	else:
		return 'capacity.total.freePct'

def get_sort_order(code):
	if code == 'fslh':
		return 1
	elif code == 'fshl':
		return -1
	elif code == 'snlh':
		return 1
	elif code == 'snhl':
		return -1
	elif code == 'cnaz':
		return 1
	elif code == 'cnza':
		return -1
	else:
		return 1