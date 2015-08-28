import logging
import math
import pickle
import random
import subprocess
from bson import Code

from bench_utils import get_random_data_slice
from Query import Query
from BlogGlobal import mongo_data, mongo_db
from BlogSettings import (
    DATA_SIZE,
    FILES_DIR,
    MONGO_FILENAME,
)

__author__ = 'Ahmed'

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class Query1Mongo(Query):
    def __init__(self):
        super(Query1Mongo, self).__init__("Selection Query 1")

    def prepare(self):
        # getting 10 percent of data
        self.arguments = get_random_data_slice(DATA_SIZE, 0.1)

    def db_command(self):
        return mongo_data.find(
            {"$and": [
                {"user_id": {"$gte": self.arguments[0]}},
                {"user_id": {"$lt": self.arguments[1]}}
            ]}
        )


class Query2Mongo(Query):
    def __init__(self):
        super(Query2Mongo, self).__init__("Selection Query 2")

    def prepare(self):
        # getting 10 percent of data
        self.arguments = get_random_data_slice(DATA_SIZE, 0.1)

    def db_command(self):
        return mongo_data.find(
            {"authored.comments": {
                "$elemMatch": {"user_id": {"$gte": self.arguments[0], "$lt": self.arguments[1]}}}
            },
            {"authored.comments": 1},
        )


class DropCollectionMongo(Query):

    def __init__(self):
        super(DropCollectionMongo, self).__init__("Dropping Data from Mongo")

    def db_command(self):
        mongo_db.drop_collection('blogdata')


class InitialLoadMongo(Query):
    def __init__(self):
        super(InitialLoadMongo, self).__init__("Initial Data Load")

    def db_command(self):
        #make a subprocess call to mongoimport
        file_name = FILES_DIR + MONGO_FILENAME
        load_data = subprocess.Popen(["mongoimport", "--db", "blogcompdb", "--collection", "blogdata", "--file", file_name], stdout=subprocess.PIPE)
        load_data.communicate()
