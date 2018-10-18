from app import app
from flask import request
from flask_pymongo import PyMongo
from flask import jsonify

from bson import Binary, Code
from bson.json_util import dumps

#low level connector to mongoDB
mongo = PyMongo(app)
print([c for c in mongo.db.test.find({})])

@app.route('/')
def index():
    machines = mongo.db.test.find({})
    return dumps(machines.next())

@app.route('/message', methods=['POST'])
def hello():
    online_users = mongo.db.users.find({"name": "Paul"})
    print(online_users != None)
    request_data = request.get_json(force = True)
    if request_data is not None:
        s = request_data['message']
        print("Recieved the message: " + s)
    else:
        print("did not get JSON")
    return "Endpoint has been hit."
