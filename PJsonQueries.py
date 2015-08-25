import json
import logging
import math
import pickle
import random
import subprocess

from bench_utils import get_random_data_slice
from nobench_gendata import encode_string
from Query import Query
from Global import pjson_db
from Settings import (
    FILES_DIR,
    PJSON_FILENAME,
    PJSON_EXTRA_FILENAME,
    PJSON_PICKLE_FILENAME,
    DATA_SIZE,
    PSQL_USER,
)

__author__ = 'Ahmed'

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


try:
    with open(PJSON_PICKLE_FILENAME, 'rb') as infile:
        recommended_strings = pickle.load(infile)
except Exception as e:
    log.error("Couldn't find pickle file!! (exception: {0})".format(str(e)))
    recommended_strings = []


class Query1PJson(Query):
    def __init__(self):
        super(Query1PJson, self).__init__("Projection Query 1")

    def db_command(self):
        cur = pjson_db.cursor()
        cur.execute("SELECT data -> 'str1' AS str1, data -> 'num' AS num FROM pjson_main;")
        return cur


class Query2PJson(Query):
    def __init__(self):
        super(Query2PJson, self).__init__("Projection Query 2")

    def db_command(self):
        cur = pjson_db.cursor()
        cur.execute("SELECT data #> '{nested_obj,str}' AS nested_str, data #> '{nested_obj,num}' AS nested_num FROM pjson_main;")
        return cur


class Query3PJson(Query):
    def __init__(self):
        super(Query3PJson, self).__init__("Projection Query 3")

    def db_command(self):
        cur = pjson_db.cursor()
        cur.execute("SELECT data -> 'sparse_110' AS sparse_110, data -> 'sparse_119' AS sparse_119 FROM pjson_main WHERE data ?& array['sparse_110', 'sparse_119'];")
        return cur


class Query4PJson(Query):
    def __init__(self):
        super(Query4PJson, self).__init__("Projection Query 4")

    def db_command(self):
        cur = pjson_db.cursor()
        cur.execute("SELECT data -> 'sparse_305' AS sparse_305, data -> 'sparse_991' AS sparse_991 FROM pjson_main WHERE data ?| array['sparse_305', 'sparse_991'];")
        return cur


class Query5PJson(Query):
    def __init__(self):
        super(Query5PJson, self).__init__("Selection Query 5")

    def prepare(self):
        seed = random.randint(0, DATA_SIZE - 1)
        self.arguments = [encode_string(seed)]

    def db_command(self):
        cur = pjson_db.cursor()
        cur.execute(
            "SELECT * FROM pjson_main WHERE data ->> 'str1' = '{}';".format(self.arguments[0])
        )
        return cur


class Query6PJson(Query):
    def __init__(self):
        super(Query6PJson, self).__init__("Selection Query 6")

    def prepare(self):
        #getting 0.1 percent of data
        self.arguments = get_random_data_slice(DATA_SIZE, 0.001)

    def db_command(self):
        cur = pjson_db.cursor()
        cur.execute(
            "SELECT * FROM pjson_main WHERE CAST(data->>'num' AS integer) >= {}"
            " AND CAST(data->>'num' AS integer) < {};".format(
                self.arguments[0], self.arguments[1]
            )
        )
        return cur


class Query7PJson(Query):
    def __init__(self):
        super(Query7PJson, self).__init__("Selection Query 7")

    def prepare(self):
        #getting 0.1 percent of data
        self.arguments = get_random_data_slice(DATA_SIZE, 0.001)

    def db_command(self):
        cur = pjson_db.cursor()
        cur.execute(
            "SELECT * FROM pjson_main WHERE data->>'dyn1' >= '{}' AND data->>'dyn1' < '{}';".format(
                self.arguments[0], self.arguments[1]
            )
        )
        return cur


class Query8PJson(Query):
    def __init__(self):
        super(Query8PJson, self).__init__("Selection Query 8")

    def prepare(self):
        global recommended_strings
        random.seed()
        random.shuffle(recommended_strings)
        self.arguments.append(recommended_strings[0])

    def db_command(self):
        search_term = self.arguments[0]
        jsonb_query = "SELECT * from pjson_main WHERE data @> '{0}';".format(
            json.dumps({'nested_arr': [search_term]})
        )
        cur = pjson_db.cursor()
        cur.execute(jsonb_query)
        return cur
        #jsonb = "SELECT * from pjson_main WHERE data @> '{"nested_arr": ["interested"]}';"

class Query9PJson(Query):
    def __init__(self):
        super(Query9PJson, self).__init__("Selection Query 9")

    def prepare(self):
        cur = pjson_db.cursor()
        cur.execute("SELECT data->>'sparse_500' from pjson_main WHERE data ? 'sparse_500';")
        for index, result in enumerate(cur):
            if index == 5:
                self.arguments.append(result[0])


    def db_command(self):
        jsonb_query = "SELECT * FROM pjson_main WHERE data ->> 'sparse_500' = '{0}';".format(
            self.arguments[0])
        cur = pjson_db.cursor()
        cur.execute(jsonb_query)
        return cur


class Query10PJson(Query):
    def __init__(self):
        super(Query10PJson, self).__init__("Aggregation Query 10")

    def prepare(self):
        #getting 10 percent of data
        self.arguments = get_random_data_slice(DATA_SIZE, 0.1)

    def db_command(self):
        jsonb_query = (
            "SELECT COUNT(*) FROM pjson_main WHERE CAST(data->>'num' AS integer) >= {}"
            " AND CAST(data->>'num' AS integer) < {}"
            " GROUP BY data->>'thousandth';".format(
                self.arguments[0], self.arguments[1]
            )
        )
        cur = pjson_db.cursor()
        cur.execute(jsonb_query)
        return cur


class Query11PJson(Query):
    def __init__(self):
        super(Query11PJson, self).__init__("Join Query 11")

    def prepare(self):
        #getting 0.1 percent of data
        self.arguments = get_random_data_slice(DATA_SIZE, 0.001)

    def db_command(self):
        jsonb_query = (
            "SELECT a.data FROM pjson_main a INNER JOIN pjson_main b"
            " ON (a.data ->> 'str1' = b.data #>> '{{nested_obj,str}}')"
            " WHERE CAST(a.data->>'num' AS integer) >= {}"
            " AND CAST(a.data->>'num' AS integer) < {};".format(
                self.arguments[0], self.arguments[1]
            )
        )
        cur = pjson_db.cursor()
        cur.execute(jsonb_query)
        return cur


class Query12PJson(Query):
    def __init__(self):
        super(Query12PJson, self).__init__("Data Addition Query 12")

    def db_command(self):
        pjson_load_cmd = "COPY pjson_main FROM '{0}';".format(
                FILES_DIR + PJSON_EXTRA_FILENAME)
        load_pjson = subprocess.Popen(["psql", "-w", "-U", PSQL_USER, "-d", "pjson", "-c", pjson_load_cmd],
                                    stdout=subprocess.PIPE)
        load_pjson.communicate()


class Query13PJson(Query):
    def __init__(self):
        super(Query13PJson, self).__init__("Deep Select Query 13")

    def prepare(self):
        seed = random.randint(0, DATA_SIZE - 1)
        self.arguments = [encode_string(seed)]

    def db_command(self):
        jsonb_query = (
            "SELECT * FROM pjson_main"
            " WHERE data #>> '{{deep_nested_obj,level_2,level_3,level_4"
            ",level_5,level_6,level_7,level_8,deep_str_single}}' = '{0}';".format(
                self.arguments[0]
            )
        )
        cur = pjson_db.cursor()
        cur.execute(jsonb_query)
        return cur


class Query14PJson(Query):
    def __init__(self):
        super(Query14PJson, self).__init__("Deep Select Query 14")

    def prepare(self):
        seed = random.randint(0, 9)
        self.arguments = [encode_string(seed)]

    def db_command(self):
        jsonb_query = (
            "SELECT data #>> '{{deep_nested_obj,level_2,level_3,level_4"
            ",level_5,level_6,level_7,level_8,deep_str_agg}}' FROM pjson_main"
            " WHERE data #>> '{{deep_nested_obj,level_2,level_3,level_4"
            ",level_5,level_6,level_7,level_8,deep_str_agg}}' = '{0}';".format(
                self.arguments[0]
            )
        )
        cur = pjson_db.cursor()
        cur.execute(jsonb_query)
        return cur


class DropCollectionPJson(Query):
    def __init__(self):
        super(DropCollectionPJson, self).__init__("Dropping Data from PJson")

    def db_command(self):
        pjson_drop_cmd = "DROP TABLE pjson_main;"
        drop_pjson = subprocess.Popen(["psql", "-w", "-U", PSQL_USER, "-d", "pjson", "-c", pjson_drop_cmd],
                                    stdout=subprocess.PIPE)
        drop_pjson.communicate()


class InitialLoadPJson(Query):
    def __init__(self):
        super(InitialLoadPJson, self).__init__("Loading Initial Data into PJson")

    def db_command(self):
        pjson_load_cmd = "CREATE TABLE pjson_main(data jsonb);"
        pjson_load_cmd += "COPY pjson_main FROM '{0}';".format(
                FILES_DIR + PJSON_FILENAME)
        pjson_load_cmd += "CREATE INDEX on pjson_main USING GIN (data);"

        load_pjson = subprocess.Popen(["psql", "-w", "-U", PSQL_USER, "-d", "pjson", "-c", pjson_load_cmd],
                                    stdout=subprocess.PIPE)
        load_pjson.communicate()


def generate_data_pjson(items):
    global recommended_strings

    with open(PJSON_PICKLE_FILENAME, 'wb') as outfile:
        pickle.dump(recommended_strings, outfile)
