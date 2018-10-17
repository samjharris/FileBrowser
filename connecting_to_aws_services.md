# Accessing Services via AWS

This is a tutorial on how to use all our services running on AWS.

## SSH

### Server Information
* IP: aws.kylesilverman.com
* User: ec2-user
* Auth: [Private Key](https://drive.google.com/file/d/1n0IADU0a1ho1Jx_A81_kBRYFSu5XKKUp/view?usp=sharing) (Do not distribute)

### Connect Using PuTTY
* Under 'Host Name', the information provided above in this format: `<user>@<ip>` Also, ensure that the 'Port' is set to 22
* On the left-hand side under the 'Category' box, expand the 'SSH' option. Then, go into the 'Auth' option
* At the bottom, you'll see an option to browse you file system to add the private key. Find the private key that you saved from the link above.
* Press 'Open' at the bottom of the window to establish the connection

## MongoDB

**NOTE:** Make sure you have Mongo installed on your system with all the necessary dependencies. See [backend_setup.md](https://github.com/samjharris/FileBrowser/blob/master/backend_setup.md#mongodb-setup).

### Server Information
* IP: aws.kylesilverman.com
* User: json_derulo
* Password: Br0ws3r! (Do not distribute)
* Database: dump
* Port: 27017

### Connect via CLI
* Use the following notation from your local machine with the information above: `mongo -u <user> -p <password> <ip>/<database>`

### Connect via PyMongo
* Import the PyMongo module: `import pymongo`
* Set a client variable with the information above: `client = pymongo.MongoClient("mongodb://<user>:<password>@<ip>/<database>")`
* Set a database variable my extracting the database instance from the client: `db = client.<database>`
