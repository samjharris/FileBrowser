"""
This file defines several classes and methods which support the MongoDB driver for HPE
"""

import pymongo
import json
import re

"""
This class is meant for representing the important fields that would make up a "machine document"
within our database.  The MachineDoc object has some crucial attributes such as the database the machine
exists in, its model, its serialNum, the tennants it belongs to, etc.
This class will take care of interfacing with a machine in the database with these certain properties you define
about this machine.
"""


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
        }

    def update_db(self, validator=None):
        """
        Updates this machine document into the db specified.  Collections are retrieved
        via the tenants list, which has a default value of HPE for all machines.
        If there already is a machine document in the database (searched for by ssn), then that document will be
        updated to the new values. If the document does not exist, then a new one is created and the logs array
        is updated to the most recent log.

        Args:
            validator: a PyMongo validator which will ensure the new collection that is created will only accept machine documents of the correct type
        """
        # this document must be inserted for each of the tenants it belongs to
        for tenant in self.tenants:
            coll = self.db[tenant]
            # update
            doc = coll.find_one({"ssn": self.ssn})
            if doc:
                print(" exisitng machine document found, updating...")
                # append this machine document's tenants array to the existing tenants array that
                # alreadys exists within this document as well as the last time it was updated
                #
                coll.find_one_and_update(
                    {"ssn": self.ssn},
                    {"$set": {"tenants": list(set(doc["tenants"]).add(set(self.tenants)))}},
                    {"$set": {"last-update": self.last_update}},
                )
                print(" machine document sucesfully updated:", self.data)
            else:
                # if a validator is supplied, then:
                # [TODO] create the collection with the specified validation rules
                # else insert the document anyways without a validator

                if validator:
                    print(" WARNING: validator not yet implemented")
                    coll.insert_one(self.data)
                    print(" new machine document inserted:", self.data)
                else:
                    coll.insert_one(self.data)
                    print(" new machine document inserted:", self.data)

    def update_log_links(self, docs=None, strays=False):
        """
        Updates this machine document into the db specified.  If the machine document cannot be found, the
        function returnsself.
        ollections where logs for this machine could live are retrieved via the tenants list of this object.
        Setting strays to True will cause the update function to search the database for all matching log
        documents with the serialNumberInserv and fetch their <ObjectID>s if those <ObjectID>s cannot be
        found in each machine document's log array, then that machine document's log array is updated.


        Args:
            strays: a Boolean to toggle a search to link possibly stray documents to any machine document that
                    matches the serialNum of this MachineDoc object
            docs: an array of <ObjectID>s already existing in the database of log documents needing to be linked
                    to the logs array of each machine document represented by this object MachineDoc
        """
        for tenant in self.tenants:
            coll = self.db[tenant]
            # get the _id of one existing log for this machine
            doc = coll.find_one({"ssn": self.ssn})
            # if not machine is found then return
            if not doc:
                return
            gen = doc["logs"][0]
            if not gen:
                print(" no logs for this machine")

            if strays:
                # find all documents in this collection that have a serialNum the same as this machine
                cur = coll.find({"serialNumberInserv": gen["serialNumberInserv"]})
                for res in cur:
                    res_id = res["_id"]
                    # if the <ObjectID> from this document is not in this machine document's logs array, then update it with the <ObjectID>
                    if res_id not in doc["logs"]:
                        coll.find_one_and_update(
                            {"ssn": self.ssn},
                            {"$set": {"logs": list(set(doc["logs"]).add(set(res_id)))}},
                            {"$set": {"last-update": self.last_update}},
                        )
                        print(" added log %s to this machine's logs" % (str(res_id)))

            if docs:
                for log_id in docs:
                    coll.find_one_and_update(
                        {"ssn": self.ssn},
                        {"$set": {"logs": list(set(doc["logs"]).add(set(log_id)))}},
                        {"$set": {"last-update": self.last_update}},
                    )
                    print(" added log %s to this machine's logs" % (str(log_id)))

    def exists(self):
        """
        Tests whether there are any machine documents in any of the tenant's collections that match
        this MachineDoc object.  Testing is performd by serialNumberInserv

        Returns:
            A boolean representing if this machine was found to exist in any tenant's collection
        """
        for tenant in self.tenants:
            coll = self.db[tenant]
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
            print("error, JsonWorker created with non-JSON files")
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
        print(" created %i new dictionaries in self.dicts" % n_dicts)
        return self.dicts

    def insert_docs(self, dicts=None):
        """
        Inserts all the document in this object's dicts array into the database that was
        specified during the instantiation of this object.  Every time a document is sucesfully
        inserted, it is added to the inserted_docs array, holding the <ObjectID>s of the
        sucesfully inserted documents.  This array is then returned so that it can be added to
        a MachineDoc class for updating.

        Args:
            dicts: a list of Python dictionaries representing additional dicitonaries of JSON data that should be inserted

        Returns:
            The array of <ObjectID>s of sucesfully inserted documents to the database
        """
        inserted = []
        if dicts:
            for dict in dicts:
                tenants = dict["authorized"]["tenants"]
                for tenant in tenants:
                    coll = self.db[tenant]
                    _id = coll.insert_one(dict)
                    # exit loop if error
                    if not _id.acknowledged:
                        print(" error inserting document:", dict)
                        break
                    # add this document's <ObjectID> to the list of inserted <ObjectID>s
                    _id = _id.inserted_id
                    self.inserted_docs.append(_id)
                    inserted.append(_id)
            return inserted

        for dict in self.dicts:
            # the list of tenants lives in the [object].authorized.tenants array
            tenants = dict["authorized"]["tenants"]
            # get the collection from the database for each tenant retrieved from the JSON, and isnert
            for tenant in tenants:
                coll = self.db[tenant]
                _id = coll.insert_one(dict)
                # exit loop if error
                if not _id.acknowledged:
                    print(" error inserting document:", dict)
                    break
                # add this document's <ObjectID> to the list of inserted <ObjectID>s
                _id = _id.inserted_id
                self.inserted_docs.append(_id)
                inserted.append(_id)
        return inserted

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
            print(" ERROR: cannot create a machine document from an empty dictionary")
            return None
        ssn = log_dict["serialNumberInserv"]
        model = log_dict["system"]["model"]
        tenants = log_dict["authorized"]["tenants"]
        mach = MachineDoc(self.db, ssn, model, tenants)
        return mach
