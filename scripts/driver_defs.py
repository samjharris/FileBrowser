"""
This file defines several classes and methods which support the MongoDB driver for HPE
"""

import pymongo
import json
import re
import datetime
import time

"""
This class is meant for representing the important fields that would make up a "machine document"
within our database.  The MachineDoc object has some crucial attributes such as the database the machine
exists in, its model, its serialNum, the tennants it belongs to, etc.
This class will take care of interfacing with a machine in the database with these certain properties you define
about this machine.
"""

# colors for command line output of database migrations
HEADER = "\033[95m"
OKBLUE = "\033[94m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"


class MachineDoc:
    def __init__(self, db, ssn, model, tenants=["HPE"]):
        """
        Initializes the MachineDoc object.

        Args:
            db: a PyMongo database that is to be containing this machine doc.
            ssn: a string representing the serial number of this machine
            tenants: a list of strings listing all the tenants that this machine belongs to.  Default tenant is HPE
        """
        self.db = db
        self.ssn = ssn
        self.model = model
        self.tenants = tenants
        self.last_update = datetime.datetime.now()
        self.logs = []
        self.data = {
            "ssn": self.ssn,
            "model": self.model,
            "tenants": self.tenants,
            "last_update": self.last_update,
            "logs": self.logs,
        }

    def update_db(self, validator=None):
        """
        Updates this machine document into the machine doc collection.
        If there already is a machine document in the database (searched for by ssn), then that document will be
        updated to the new values. If the document does not exist, then a new one is created and the logs array
        is updated to the most recent log.
        Args:
            validator: a PyMongo validator which will ensure the new collection that is created will only accept machine documents of the correct type
        """
        coll = self.db["machines"]
        # update
        doc = coll.find_one({"ssn": self.ssn})
        if doc:
            print((WARNING + " exisitng machine document found, updating..." + ENDC))
            # append this machine document's tenants array to the existing tenants array that
            # alreadys exists within this document as well as the last time it was updated
            #
            coll.find_one_and_update(
                {"ssn": self.ssn},
                {
                    "$set": {
                        "tenants": doc["tenants"] + list(set(self.tenants) - set(doc["tenants"])),
                        "last-update": self.last_update,
                    }
                },
            )
            print((OKGREEN + " machine document sucesfully updated: ssn = %s" + ENDC) % self.ssn)
        else:
            # if a validator is supplied, then:
            # [TODO] create the collection with the specified validation rules
            # else insert the document anyways without a validator
            if validator:
                print((WARNING + " WARNING: validator not yet implemented" + ENDC))
                coll.insert_one(self.data)
                print((OKGREEN + " new machine document inserted: ssn = %s" + ENDC) % self.ssn)
            else:
                coll.insert_one(self.data)
                print((OKGREEN + " new machine document inserted: ssn = %s" + ENDC) % self.ssn)

    def update_log_links(self, docs=None, strays=False):
        """
        Updates this machine document into the db specified.  If the machine document cannot be found, the
        function returnsself.
        Setting strays to True will cause the update function to search the database for all matching log
        documents with the serialNumberInserv and fetch their <ObjectID>s if those <ObjectID>s cannot be
        found in each machine document's log array, then that machine document's log array is updated.


        Args:
            strays: a Boolean to toggle a search to link possibly stray documents to any machine document that
                    matches the serialNum of this MachineDoc object
            docs: an array of <ObjectID>s already existing in the database of log documents needing to be linked
                    to the logs array of each machine document represented by this object MachineDoc
        """
        coll = self.db["machines"]
        # get the _id of one existing log for this machine
        doc = coll.find_one({"ssn": self.ssn})
        # if not machine is found then return
        if not doc:
            return
        if "logs" not in doc.keys():
            print(
                (FAIL + " ERROR: cannot find logs[] array for machine with ssn: %s" + ENDC)
                % self.ssn
            )
            exit()
        gen = doc["logs"]
        if len(gen) < 1:
            print((WARNING + " WARNING: no logs for this machine" + ENDC))
            gen = None
        else:
            gen = gen[0]

        if strays:
            if not gen:
                print(
                    (
                        FAIL
                        + " ERROR: cannot link stray documents witout a document already linked to this machine for finding the serial number"
                        + ENDC
                    )
                )
            else:
                # find all documents in this collection that have a serialNum the same as this machine
                cur = coll.find({"serialNumberInserv": gen["serialNumberInserv"]})
                for res in cur:
                    res_id = res["_id"]
                    # if the <ObjectID> from this document is not in this machine document's logs array, then update it with the <ObjectID>
                    if res_id not in doc["logs"]:
                        coll.find_one_and_update(
                            {"ssn": self.ssn},
                            {
                                "$set": {
                                    "logs": doc["logs"] + list(set([res_id]) - set(doc["logs"])),
                                    "last-update": self.last_update,
                                }
                            },
                        )
                        print(
                            (OKGREEN + " added log %s to this machine's logs" + ENDC)
                            % (str(res_id))
                        )
        if docs:
            for log_id in docs:
                coll.find_one_and_update(
                    {"ssn": self.ssn},
                    {
                        "$set": {
                            "logs": doc["logs"] + list(set([log_id]) - set(doc["logs"])),
                            "last-update": self.last_update,
                        }
                    },
                )
                print((OKGREEN + " added log %s to this machine's logs" + ENDC) % (str(log_id)))

    def exists(self):
        """
        Tests whether there are any machine documents in any of the tenant's collections that match
        this MachineDoc object.  Testing is performd by serialNumberInserv

        Returns:
            A boolean representing if this machine was found to exist in any tenant's collection
        """
        coll = self.db["machines"]
        # get the _id of one existing log for this machine
        doc = coll.find_one({"ssn": self.ssn})
        # if not machine is found then return
        if doc:
            return True
        # no documents were found, return False
        return False


"""
This class is meant for working with JSON files from a data dump, which represent the log data given by the HPE machines.
The JsonWorker stores some important information about the data dump being processed, such as into which DB the data
should end up, and the file objects of all the json files.
The class is meant for sorting through data and converting it into Python dictionaries, which can then easily
be inserted into the database.
"""


class JsonWorker:
    def __init__(self, db, json_files_names):
        """
        Creates this JsonWorker object.  The class will hold all the file objects representing the
        data dump in Python dictionaries in the dicts array, and record documents it has inserted in
        the inserted_docs array.

        Args:
            db: a PyMongo object describing to what database this data dump belongs to
            json_files_objects: an array of file objects that represent the JSON files this class will work on
        """
        self.dicts = []
        self.inserted_docs = []
        self.db = db
        self.json_files = []

        # if the object is created with invalid JSON files, then warn and set the array to empty
        if json_files_names[0].endswith(".json"):
            self.json_files = json_files_names
        else:
            print((FAIL + " ERROR: JsonWorker created with non-JSON files" + ENDC))
            self.json_files = []

    def make_dicts(self):
        """
        Fills in this object's dicts array, which will hold Python dictionaries representing
        individual JSON files opened during the instantiation of this object.

        Returns:
            an array of Python dictionaries that were made from the JSON file objects
        """
        n_dicts = 0
        # must open file objects one by one to avoid file descriptor overload during large dumps
        for i, file in enumerate(self.json_files):
            invalid_file = re.search(r"/\._.*\.json$", file)
            # certain files the begin with [DIR]/._[name].json do nto contain valid logs from dump
            if invalid_file:
                continue
            f = open(file)
            self.dicts.append(json.load(f))
            n_dicts = i
        print((OKBLUE + " created %i new dictionaries in self.dicts" + ENDC) % n_dicts)
        return self.dicts

    def exist_doc(self, dic, duplicates):
        """
        Checks whether a document exists in the DB and prints an error message if so, and returns true of false
        """
        coll = self.db["logs"]
        res = coll.find_one({"serialNumberInserv": dic["serialNumberInserv"], "date": dic["date"]})
        if res:
            print(
                (
                    FAIL
                    + "   WARNING: existing identical log document found in dump directory!  Please make sure this is a new set of log documents"
                )
            )
            print(
                (
                    "   no new documents were or will be inserted because"
                    + ENDC
                    + " 'duplicates' "
                    + WARNING
                    + "is set to %s"
                    + ENDC
                )
                % duplicates
            )
            return True
        else:
            return False

    def insert_docs(self, dicts=None, duplicates=False):
        """
        Inserts all the document in this object's dicts array into the database that was
        specified during the instantiation of this object.  Every time a document is sucesfully
        inserted, it is added to the inserted_docs array, holding the <ObjectID>s of the
        sucesfully inserted documents.  This array is then returned so that it can be added to
        a MachineDoc class for updating.

        Args:
            dicts: a list of Python dictionaries representing additional dicitonaries of JSON data that should be inserted
            duplicates: whether to add duplicate documents to the database, default is false since we only want one log per dump datas

        Returns:
            The array of <ObjectID>s of sucesfully inserted documents to the database, or None if nothing was inserted
        """
        inserted = []
        if dicts:
            for dic in dicts:
                if self.exist_doc(dic, duplicates):
                    continue
                coll = self.db["logs"]
                _id = coll.insert_one(dic)
                # exit loop if error
                if not _id.acknowledged:
                    print(
                        (FAIL + " ERROR: inserting document with ssn: %s" + ENDC)
                        % dic["serialNumberInserv"]
                    )
                    break
                # add this document's <ObjectID> to the list of inserted <ObjectID>s
                _id = _id.inserted_id
                self.inserted_docs.append(_id)
                inserted.append(_id)
            return inserted

        for dic in self.dicts:
            if self.exist_doc(dic, duplicates):
                continue
            # get the collection from the database for each tenant retrieved from the JSON, and isnert
            coll = self.db["logs"]
            _id = coll.insert_one(dic)
            # exit loop if error
            if not _id.acknowledged:
                print(
                    (FAIL + " ERROR: inserting document with ssn: %s" + ENDC)
                    % dic["serialNumberInserv"]
                )
                break
            # add this document's <ObjectID> to the list of inserted <ObjectID>s
            _id = _id.inserted_id
            self.inserted_docs.append(_id)
            inserted.append(_id)
        if len(self.dicts) > 0:
            return inserted
        else:
            return None

    def create_machine_doc(self, log_dict):
        """
        Creates a MachineDoc object representing the machine that this log belongs to.
        This MachineDoc object can perform certain operations like inserting, updating, and linking of log documents
        to any and all machine documents represented by this MachineDoc object.

        Args:
            log_dict: a Python dictionary representing the log from the JSON file

        Returns:
            a MachineDoc object if creation was sucesfull, None otherwise
        """
        if not log_dict:
            print(
                (
                    FAIL
                    + " ERROR: cannot create a machine document from an empty dictionary, skipping this machine document creation"
                    + ENDC
                )
            )
            return None
        ssn = log_dict["serialNumberInserv"]
        model = log_dict["system"]["model"]
        tenants = log_dict["authorized"]["tenants"]
        mach = MachineDoc(self.db, ssn, model, tenants)
        return mach
