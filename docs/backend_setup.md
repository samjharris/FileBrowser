# First Time Setup

### Overview
This is a a guide on how to setup a backend and database using Flask and MongoDB.  Though we have not officially decided on a backend stack, this can help people get set up to try out these technologies.  
The backend runs on [Flask](http://flask.pocoo.org/) in a virtual environment which is connected to [MongoDB](https://docs.mongodb.com/manual/tutorial/getting-started/).  Flask connects to Mongo through [PyMongo](https://flask-pymongo.readthedocs.io/en/latest/), and uses security from [Flask Security](https://pythonhosted.org/Flask-Security/) to authenticate users and maintain sessions.  

### Python Setup
First thing is to do is to set up a virtual environment.  First get the virtualenv tool from pip:<br/>
_POSIX and Windows_:   `pip install virtualenv`
_(you might need superuser permissions for POSIX)_<br/>
This will create a folder containing all the libraries and binaries that your current version of Python needs to run, and is isolated from your system-wide installation.  You can install additional libraries and packages into this virtual environment with pip just like you usually would, but they will exist only within that environment.  <br/>This also means you will not be able to use any packages or libraries you already have installed for Python without first reinstalling them within your virtual environment.

To use this virtual environment, you must first create it:<br/>
_POSIX and Windows_ `virtualenv venv` <br/>where `venv` is the name of the folder which will hold your virtual environment.<br/>
Navigate to the location of the venv folder.  Now you must install the needed packages into venv.  To do this, first enter the virtual terminal:<br/>
_POSIX_: `. venv/bin/activate`<br/>
_Windows_: `\venv\Scripts\activate`<br/><br/>
Once you are in the virtual shell, you can install any packages you need with pip like you usually do.  Whenever you run Python code in the future for your project, make sure you first enter the virtual shell, then run scripts from inside there.
The `requirements.txt` file describes all the pip installations needed to run the application.  You can automatically install all of them using the recursive flag `-r` for pip and pointing to the location of the requirements.txt file:<br/>
_POSIX and Windows_: `pip install -r requirements.txt`<br/>
Now Python should be set up in a virtual environment with all needed packages.
<br/> To test the server, once in your virtual shell, run:
_POSIX and Windows_: `python -m flask run`, and
the server should start on port 5000.
### MongoDB Setup
MongoDB is a No-SQL database that uses the documents model to store data.  Documents can hold JSON-like data and are easy to work with because the models used in the database can be continuously updated and changed without major restructuring.  MongoDB is easy to setup because it comes with many package managers.  There are many different POSIX commands depending on your package manager, so please reference the[ official guide for installing MongoDB on your machine](https://docs.mongodb.com/manual/installation/).  MongoDB's default port is 27017.  <br/><br/>
To check if your installation is working, you can enter the Mongo shell by typing in `mongo` if you PATH environment variable is set to the mongo installation directory.  To see all the databases you have, use:
`show dbs`, or just `db` to see what database you are currently in.  Since you have not created any databases yet, this should return `test`.
 Hooray!<br/><br/>
To practice navigating the databases, creating, reading, and deleting data, read [the basic MongoDB CRUD operations](https://docs.mongodb.com/manual/crud/) and try making a database with a `users` document.  Here are some quickstart steps:<br/>
To use a database on the machine, enter the mongo shell and enter `use myDatabase1` to switch into `myDatabase1`.  If `myDatabase1` does not exist, then it will be automatically created when you run that command.<br/>
To insert a document, it must be a part of a _Collection_, which is part of the database itself.  You can create a collection by simply inserting a new document.  If the collection does not exist yet, then upon the creation of the document, the Collection will be created as well.  Let's insert a simple `users` document:<br/>
`myDatabase1.myNewCollection.insertOne( {
    name: "Troll Boy",
    age: 21,
} )`<br/>If you get an acknowledge message, then your document about Troll Boy has been successfully inserted into the database myDatabase1.
Finding documents within a database can be done by filtering via data values, data types, and many other useful features since document oriented databases use key-value pairs to store data.  <br/>
* See all documents: `myDatabase1.myNewCollection.find ( { } )`
* Find no more than 5 documents with an age greater than 18: <br/>`myDatabase1.myNewCollection.find( { age: {$gt: 18} } ).limit(5)`<br/>
* Find documents whose status is "A" and quantity is less than 30:<br/> `myDatabase1.myNewCollection.find( { status: "A", qty: { $lt: 30 } } )`<br/>

You can read about the comparison operators such as `$lt: 30` [at MongoDB's official docs](https://docs.mongodb.com/manual/reference/operator/query-comparison/). <br/>
Flask uses a great package for interfacing with MongoDB called PyMongo.  The syntax is almost identical for querying documents as above, and connecting to the database can be done in two lines of code which will be covered shortly.<br/><br/>
# Flask
_(information on how Flask works will go here)_
