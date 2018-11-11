import pymongo
import os
import sys
import json
from collections import namedtuple
import datetime
import time
import re

if len(sys.argv) < 2:
	print("ERROR usage: /python db_test.py <path from CWD to proper decompressed data dumps>")
	exit()

#Print useful info to console
print("----------------------------------------------")
print("-       Begin database integrity tests       -")
print("----------------------------------------------")

#Declare which tests to run:
test_database_propercollections = True
test_database_machines_count = True
test_database_machines_names_duplicates = True
test_database_logs_count = True
test_database_logs_exists_exhaustive = True

#Declare useful options:
flag_v = False #VERBOSE MODE
MONGO_URI = "aws.kylesilverman.com" #MongoDB host
MONGO_DB = "dump" #MongoDB db name
MONGO_USER = "json_derulo" #MongoDB username
MONGO_PASSWORD = "Br0ws3r!" #MongoDB password

#Initialize useful variables:
tests_run = 0
tests_passed = 0
CWD = os.getcwd()
DATA_PATH = sys.argv[1]
DATA_ITEM = CWD + "/" + DATA_PATH
MONGO_URI = "mongodb://" + MONGO_USER + ":" + MONGO_PASSWORD + "@" + MONGO_URI + "/" + MONGO_DB
client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]

if not db:
    print("ERROR: could not run tests (database is of type None)")
    exit()

#Begin test_database_propercollections
if test_database_propercollections:
	tests_run += 1
	db_collectionNames = db.list_collection_names()
	proper_collectionNames = ["machines", "logs", "users"]
	if set(proper_collectionNames) == set(db_collectionNames) and\
	len(proper_collectionNames) == len(db_collectionNames):
		print("PASS: test-database-propercollections")
		tests_passed += 1
	else:
		print("FAIL: test-database-propercollections")
		msg = "" 
		for cur in proper_collectionNames:
			if cur in db_collectionNames:
				msg += cur + " , "
		if len(msg) > 1:
			msg = "\t- DB contains proper collection[s]: " + msg[0:-2]
			print(msg)
		else:
			print("\t- DB contains no proper collections.")
		msg = ""
		for cur in proper_collectionNames:
			if cur not in db_collectionNames:
				msg += cur + " , "
		if len(msg) > 1:
			msg = "\t- DB missing collection[s]: " + msg[0:-2]
			print(msg)
		msg = ""
		for cur in db_collectionNames:
			if cur not in proper_collectionNames:
				msg += cur + " , "
		if len(msg) > 1:
			msg = "\t- DB contains superfluous collection[s]: " + msg[0:-2]
			print(msg)

#Begin test_database_machines_count
if test_database_machines_count:
	tests_run += 1
	proper_machines = []
	proper_numMachines = 0
	db_numMachines = 0
	db_collectionNames = db.list_collection_names()
	
	for filename in os.listdir(DATA_ITEM):
		if re.search(r"/\._.*\.json$", filename):
			continue
		name = filename.split('-')[0]
		if name in proper_machines:
			continue
		proper_machines.append(name)
		proper_numMachines+=1

	if "machines" in db_collectionNames:
		db_machines = db.get_collection("machines")
		db_numMachines = db_machines.count_documents({})
		if proper_numMachines == db_numMachines:
			print("PASS: test_database_machines_count")
		else:
			print("FAIL: test_database_machines_count")
			print("\t- Expected: " + str(proper_numMachines) + " actual: " + str(db_numMachines))
	else:
		print("FAIL: test_database_machines_count")
		print("\t- Collection \"machines\" does not exist")

#Begin test_database_machines_names_duplicates		
if test_database_machines_names_duplicates:
	tests_run += 1
	proper_machines_dict = {}
	db_machines_dict = {}
	db_machines_list = []
	msg_dup = ""
	num_dup = 0
	msg_mis = ""
	num_mis = 0
	db_collectionNames = db.list_collection_names()
	for filename in os.listdir(DATA_ITEM):
		if re.search(r"/\._.*\.json$", filename):
			continue
		name = filename.split('-')[0]
		if name in proper_machines_dict:
			continue
		proper_machines_dict[name] = 0
	if "machines" in db_collectionNames:
		db_machines = db.get_collection("machines")
		db_machines_dict = db_machines.find({},{"_id" : 0, "ssn": 1})
		for cur in db_machines_dict:
			db_machines_list.append(cur.get("ssn"))
		for cur in db_machines_list:
			if cur in proper_machines_dict.keys():
				if proper_machines_dict.get(cur) == 1:
					msg_dup += (cur + " , ")
					num_dup += 1
				else:
					proper_machines_dict[cur] = 1
		for cur in proper_machines_dict.keys():
			if proper_machines_dict.get(cur) == 0:
				msg_mis += (cur + " , ")
				num_mis += 1
		if len(msg_dup) == 0 and len(msg_mis) == 0:
			print("PASS: test_database_machines_names_duplicates")
		else:
			print("FAIL: test_database_machines_names_duplicates")
			if len(msg_dup) > 0:
				print("\t- Collection 'machines' contains " + str(num_dup) + " duplicate[s]: ")
				if flag_v: 
					print("\t" + msg_dup[0:-2])
				else:
					print("\tSet 'flag_v' to view")
			if len(msg_mis) > 0:
				print("\t- Collection 'machines' missing "+ str(num_mis) + " machine SSN[s]: ")
				if flag_v: 
					print("\t" + msg_mis[0:-2])
				else:
					print("\tSet 'flag_v' to view")
	else:
		print("FAIL: test_database_machines_names_duplicates")
		print("\t- Collection \"machines\" does not exist")
	
#Begin test_database_logs_count
if test_database_logs_count:
	tests_run += 1
	proper_numLogs = 0
	db_numLogs = 0
	db_collectionNames = db.list_collection_names()
	for filename in os.listdir(DATA_ITEM):
		if re.search(r"/\._.*\.json$", filename):
			continue
		proper_numLogs+=1	
	if "logs" in db_collectionNames:
		db_logs = db.get_collection("logs")
		db_numLogs = db_logs.count_documents({})
		if proper_numLogs == db_numLogs:
			print("PASS: test_database_logs_count")
		else:
			print("FAIL: test_database_logs_count")
			print("\t- Expected: " + str(proper_numLogs) + " actual: " + str(db_numLogs))
	else:
		print("FAIL: test_database_logs_count")
		print("\t- Collection \"logs\" does not exist")

#Begin test_database_logs_exists_exhaustive
if test_database_logs_exists_exhaustive:
	tests_run += 1
	msg = ""
	proper_machines_dict = {} 
	db_logs_dict = {}
	db_collectionNames = db.list_collection_names()

	for filename in os.listdir(DATA_ITEM):	
			if re.search(r"/\._.*\.json$", filename):
				continue
			name = filename.split('-')[0]
			if name in proper_machines_dict:
				proper_machines_dict[name] += 1
			else:	
				proper_machines_dict[name] = 1

	if "logs" in db_collectionNames:
		db_logs = db.get_collection("logs")
		for cur_proper_log in proper_machines_dict.keys():
			db_cur_logs_count = 0
			db_cur_logs_dict = db_logs.find({"serialNumberInserv" : cur_proper_log},{"_id" : 0, "serialNumberInserv": 1})
			for cur_db_log in db_cur_logs_dict:
				db_cur_logs_count += 1
			if db_cur_logs_count > proper_machines_dict[cur_proper_log] or db_cur_logs_count < proper_machines_dict[cur_proper_log]:
				msg += ("ssn>" + str(cur_proper_log) + " Expected>" + str(proper_machines_dict[cur_proper_log]) + " Actual>" + str(db_cur_logs_count) + " | ")	

		if len(msg) == 0:
			print("PASS: test_database_logs_exists_exhaustive")
		else:
			print("FAIL: test_database_logs_exists_exhaustive")
			if(flag_v):
				print("\t- Some log documents are either missing or superfluous:")  
				print("\tformat: | ssn>[machine serial number] Expected>[Proper number of log documents] Actual>[Number of log documents in db] |")
				print("\t" + msg[0:-3])
			else:
				print("\t- Some log documents are either missing or superfluous:")
				print("\tSet 'flag_v' to view")
	
		

	else:
		print("FAIL: test_database_logs_exists_exhaustive")
		print("\t- Collection \"logs\" does not exist")
	
		
print("----------------------------------------------")
print("-    Tests run: " + str(tests_run) + "                            -")
print("-    Tests passed: " + str(tests_passed) + "                         -")
if tests_run == tests_passed: 
	print("-          ALL TESTS PASSED                  -")
print("----------------------------------------------")
