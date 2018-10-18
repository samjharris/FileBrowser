from flask import Flask
from flask_pymongo import PyMongo
#__name__ is a variable passed to the class 'Flask', which is a
#python specific predefined variable, which is set to
#the name of the module used, and functions as a 'starting point'
app = Flask(__name__)

#App configuration settings
app.config["MONGO_URI"] = "mongodb://json_derulo:Br0ws3r!@aws.kylesilverman.com:27017/dump"
app.config["SECRET_KEY"] = '12345' #so secret, very security
app.config["MONGODB_DB"] = 'dump'

from app import routes
