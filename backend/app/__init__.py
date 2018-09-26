from flask import Flask

#__name__ is a variable passed to the class 'Flask', which is a
#python specific predefined variable, which is set to
#the name of the module used, and functions as a 'starting point'
app = Flask(__name__)

from app import routes
