import pickle
import random
import subprocess

from bson import Code
import math

from Query import Query
from Global import data, mongo_db, MONGO_FILENAME, MONGO_EXTRA_FILENAME, DATA_SIZE, MONGO_PICKLE_FILENAME
import nobench_gendata



__author__ = 'Gary'
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

try:
    with open(MONGO_PICKLE_FILENAME, "rb") as infile:
        recommended_strings = pickle.load(infile)
except Exception as e:
    log.error("Couldn't find pickle file!!", str(e))
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
        halfway_index = DATA_SIZE / 2
        results = data.find({}, {"str1": 1, "_id": 0})
        for index, result in enumerate(results):

            if index == halfway_index:
                self.arguments.append(result['str1'])

    def db_command(self):
        return data.find({"str1": "{}".format(self.arguments[0])})


class Query6Mongo(Query):
    def __init__(self):
        super(Query6Mongo, self).__init__("Selection Query 6")

    def prepare(self):
        data_slice_size = math.ceil(DATA_SIZE * 0.001)
        rand_num = random.randint(1, DATA_SIZE)
        #Changing the parameters of the query based on the trial size.
        self.arguments.append(rand_num)
        self.arguments.append(rand_num + data_slice_size)

    def db_command(self):
        #Select 0.1% of data. 1000 rows in this case.
        return data.find({"$and": [{"num": {"$gte": self.arguments[0]}}, {"num": {"$lt": self.arguments[1]}}]})


class Query7Mongo(Query):
    def __init__(self):
        super(Query7Mongo, self).__init__("Selection Query 7")

    def prepare(self):
        data_slice_size = math.ceil(DATA_SIZE * 0.001)
        rand_num = random.randint(1, DATA_SIZE)
        #Changing the parameters of the query based on the trial size.
        self.arguments.append(rand_num)
        self.arguments.append(rand_num + data_slice_size)

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
        data_slice_size = math.ceil(DATA_SIZE * 0.1)
        rand_num = random.randint(1, DATA_SIZE)
        #Changing the parameters of the query based on the trial size.
        self.arguments.append(rand_num)
        self.arguments.append(rand_num + data_slice_size)
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
        load_data = subprocess.Popen(["mongoimport.exe", "--db", "argocompdb", "--collection", "sampledata", "--file", "D:\\Dropbox\\Argo Vs Mongo Project\\nobench\\nobench_data_mongo_extra"], stdout=subprocess.PIPE)
        load_data.communicate()


class Query13Mongo(Query):
    def __init__(self):
        super(Query13Mongo, self).__init__("Deep nest Query 13")

    def prepare(self):
        halfway_index = DATA_SIZE / 2
        results = data.find({}, {"multiply_nested_obj.level_2.level_3.level_4.level_5.level_6.level_7.level_8.deep_str_single": 1, "_id": 0})
        for index, result in enumerate(results):
            if index == halfway_index:
                self.arguments.append(result['multiply_nested_obj']['level_2']['level_3']['level_4']['level_5']['level_6']['level_7']['level_8']['deep_str_single'])

    def db_command(self):
        return data.find({"multiply_nested_obj.level_2.level_3.level_4.level_5.level_6.level_7.level_8.deep_str_single": self.arguments[0]})

class Query14Mongo(Query):
    def __init__(self):
        super(Query14Mongo, self).__init__("Deep aggregation Query 14")

    def prepare(self):
        halfway_index = DATA_SIZE / 2
        results = data.find({}, {"multiply_nested_obj.level_2.level_3.level_4.level_5.level_6.level_7.level_8.deep_str_agg": 1, "_id": 0})
        for index, result in enumerate(results):
            if index == halfway_index:
                self.arguments.append(result['multiply_nested_obj']['level_2']['level_3']['level_4']['level_5']['level_6']['level_7']['level_8']['deep_str_agg'])

    def db_command(self):
        return data.find({"multiply_nested_obj.level_2.level_3.level_4.level_5.level_6.level_7.level_8.deep_str_agg": self.arguments[0]})

class InitialLoadMongo(Query):
    def __init__(self):
        super(InitialLoadMongo, self).__init__("Initial Data Load")

    def db_command(self):
        #make a subprocess call to mongoimport
        load_data = subprocess.Popen(["mongoimport.exe", "--db", "argocompdb", "--collection", "sampledata", "--file", "D:\\Dropbox\\Argo Vs Mongo Project\\nobench\\nobench_data_mongo"], stdout=subprocess.PIPE)
        load_data.communicate()
