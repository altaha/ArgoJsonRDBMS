import pickle
import random
import subprocess
import math
from bson import Code

import nobench_gendata
from bench_utils import get_random_data_slice
from Query import Query
from Settings import (
    DATA_SIZE,
    FILES_DIR,
    MONGO_FILENAME,
    MONGO_EXTRA_FILENAME,
    MONGO_PICKLE_FILENAME,
)
from Global import data, mongo_db


__author__ = 'Gary'
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

try:
    with open(MONGO_PICKLE_FILENAME, "rb") as infile:
        recommended_strings = pickle.load(infile)
except Exception as e:
    log.error("Couldn't find pickle file!! (exception: {0})".format(str(e)))
    recommended_strings = []


def generate_data_mongo(items):
    global recommended_strings

    recommended_strings = nobench_gendata.main_non_cli(items, True, MONGO_FILENAME)

    with open(MONGO_PICKLE_FILENAME, 'wb') as outfile:
        pickle.dump(recommended_strings, outfile)


class DropCollectionMongo(Query):

    def __init__(self):
        super(DropCollectionMongo, self).__init__("Dropping Data from Mongo")

    def db_command(self):
        mongo_db.drop_collection('sampledata')


class Query1Mongo(Query):


    def __init__(self):
        super(Query1Mongo, self).__init__("Projection Query 1")

    def db_command(self):
        return data.find({}, ["str1", "num"])


class Query2Mongo(Query):


    def __init__(self):
        super(Query2Mongo, self).__init__("Projection Query 2")

    def db_command(self):
        return data.find({}, ["nested_obj.str", "nested_obj.num"])


class Query3Mongo(Query):

    def __init__(self):
        super(Query3Mongo, self).__init__("Projection Query 3")

    def db_command(self):
        return data.find(
            {"$or": [{"sparse_110": {"$exists": True}},
                        {"sparse_119": {"$exists": True}}]},
            ["sparse_110", "sparse_919"])


class Query4Mongo(Query):
    def __init__(self):
        super(Query4Mongo, self).__init__("Projection Query 4")

    def db_command(self):
        return data.find(
            {"$or": [{"sparse_110": {"$exists": True}},
                        {"sparse_229": {"$exists": True}}]},
            ["sparse_110", "sparse_919"])


class Query5Mongo(Query):
    def __init__(self):
        super(Query5Mongo, self).__init__("Selection Query 5")

    def prepare(self):
        seed = random.randint(0, DATA_SIZE - 1)
        self.arguments = [nobench_gendata.encode_string(seed)]

    def db_command(self):
        return data.find({"str1": "{}".format(self.arguments[0])})


class Query6Mongo(Query):
    def __init__(self):
        super(Query6Mongo, self).__init__("Selection Query 6")

    def prepare(self):
        #Changing the parameters of the query based on the trial size.
        self.arguments = get_random_data_slice(DATA_SIZE, 0.001)

    def db_command(self):
        #Select 0.1% of data. 1000 rows in this case.
        return data.find({"$and": [{"num": {"$gte": self.arguments[0]}}, {"num": {"$lt": self.arguments[1]}}]})


class Query7Mongo(Query):
    def __init__(self):
        super(Query7Mongo, self).__init__("Selection Query 7")

    def prepare(self):
        #Changing the parameters of the query based on the trial size.
        self.arguments = get_random_data_slice(DATA_SIZE, 0.001)

    def db_command(self):
        #Select 0.1% of data. 1000 rows in this case.
        return data.find({"$and": [{"dyn1": {"$gte": self.arguments[0]}}, {"dyn1": {"$lt": self.arguments[1]}}]})


class Query8Mongo(Query):
    def __init__(self):
        super(Query8Mongo, self).__init__("Selection Query 8")

    def prepare(self):
        global recommended_strings
        random.seed()
        random.shuffle(recommended_strings)
        self.arguments.append(recommended_strings[0])

    def db_command(self):
        return data.find({"nested_arr": self.arguments[0]})


class Query9Mongo(Query):

    def __init__(self):
        super(Query9Mongo, self).__init__("Selection Query 9")

    def prepare(self):
        results = data.find({}, {"sparse_500": 1, "_id": 0})
        for index, result in enumerate(results):
            try:
                self.arguments.append(result['sparse_500'])
            except KeyError:
                continue
            else:
                break

    def db_command(self):
        return data.find({"sparse_500": self.arguments[0]})


class Query10Mongo(Query):
    def __init__(self):
        super(Query10Mongo, self).__init__("Aggregation Query 10")

    def prepare(self):
        #getting 10 percent of data
        self.arguments = get_random_data_slice(DATA_SIZE, 0.1)

    def db_command(self):

        return data.group(
            {"thousandth": True},
            {"$and": [{"num": {"$gte": self.arguments[0]}}, {"num": {"$lt": self.arguments[1]}}]},
            {"total": 0},
            """
                        function(obj, prev) {
                            prev.total += 1;
                            }
            """,
            )


class Query11Mongo(Query):
    def __init__(self):
        super(Query11Mongo, self).__init__("Join Query 11")

    def db_command(self):
        map = Code("""
            function() {
            var output ={neststr:this.nested_obj.str, str1:this.str1, num:this.num}
                emit(this._id, output)
            }
        """)
        reduce = Code("""
            function(key, values)

        """)
        data.map_reduce(

        )
        #implement a mapreduce job?
        pass


class Query12Mongo(Query):
    def __init__(self):
        super(Query12Mongo, self).__init__("Data Addition Query 12")

    def db_command(self):
        #make a subprocess call to mongoimport
        extra_file_name = FILES_DIR + MONGO_EXTRA_FILENAME
        load_data = subprocess.Popen(["mongoimport", "--db", "argocompdb", "--collection", "sampledata", "--file", extra_file_name], stdout=subprocess.PIPE)
        load_data.communicate()


class Query13Mongo(Query):
    def __init__(self):
        super(Query13Mongo, self).__init__("Deep nest Query 13")

    def prepare(self):
        seed = random.randint(0, DATA_SIZE - 1)
        self.arguments = [nobench_gendata.encode_string(seed)]

    def db_command(self):
        return data.find({"deep_nested_obj.level_2.level_3.level_4.level_5.level_6.level_7.level_8.deep_str_single": self.arguments[0]})


class Query14Mongo(Query):
    def __init__(self):
        super(Query14Mongo, self).__init__("Deep aggregation Query 14")

    def prepare(self):
        seed = random.randint(0, 9)
        self.arguments = [nobench_gendata.encode_string(seed)]

    def db_command(self):
        return data.find({"deep_nested_obj.level_2.level_3.level_4.level_5.level_6.level_7.level_8.deep_str_agg": self.arguments[0]})


class InitialLoadMongo(Query):
    def __init__(self):
        super(InitialLoadMongo, self).__init__("Initial Data Load")

    def db_command(self):
        #make a subprocess call to mongoimport
        file_name = FILES_DIR + MONGO_FILENAME
        load_data = subprocess.Popen(["mongoimport", "--db", "argocompdb", "--collection", "sampledata", "--file", file_name], stdout=subprocess.PIPE)
        load_data.communicate()
