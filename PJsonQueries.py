import logging
import random
import subprocess
import math
from Query import Query
import pickle

__author__ = 'Ahmed'

from Global import pjson_db
from Settings import (
    PJSON_FILE_DIR,
    PJSON_FILENAME,
    PJSON_EXTRA_FILENAME,
    PJSON_PICKLE_FILENAME,
    DATA_SIZE,
    PSQL_USER,
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


try:
    with open(PJSON_PICKLE_FILENAME, 'rb') as infile:
        recommended_strings = pickle.load(infile)
except Exception as e:
    log.error("Couldn't find pickle file!! (exception: {0})".format(str(e)))
    recommended_strings = []


class PrepFilesPJson(Query):
    def __init__(self, filename):
        super(PrepFilesPJson, self).__init__("Preparing files for PJson consumption")
        self.filename = filename

    def db_command(self):
        pass


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
        return None
        return pjson_db.execute_sql("SELECT nested_obj.str1, nested_obj.num FROM nobench_main;")


class Query3PJson(Query):
    def __init__(self):
        super(Query3PJson, self).__init__("Projection Query 3")

    def db_command(self):
        return None
        return pjson_db.execute_sql("SELECT sparse_110, sparse_119 FROM nobench_main;")


class Query4PJson(Query):
    def __init__(self):
        super(Query4PJson, self).__init__("Projection Query 4")

    def db_command(self):
        return None
        return pjson_db.execute_sql("SELECT sparse_110, sparse_220 FROM nobench_main;")


class Query5PJson(Query):
    def __init__(self):
        super(Query5PJson, self).__init__("Selection Query 5")

    def prepare(self):
        return None
        halfway_index = DATA_SIZE / 2
        results = pjson_db.execute_sql("SELECT str1 FROM nobench_main")
        for index, result in enumerate(results):

            if index == halfway_index:
                self.arguments.append(result['str1'])

    def db_command(self):
        return None
        return pjson_db.execute_sql(
            'SELECT * FROM nobench_main WHERE str1 = "{}";'.format(self.arguments[0]))


class Query6PJson(Query):
    def __init__(self):
        super(Query6PJson, self).__init__("Selection Query 6")

    def prepare(self):
        return None
        data_slice_size = math.ceil(DATA_SIZE * 0.001)
        rand_num = random.randint(1, DATA_SIZE)
        #Changing the parameters of the query based on the trial size.
        self.arguments.append(rand_num)
        self.arguments.append(rand_num + data_slice_size)

    def db_command(self):
        return None
        # return pjson_db.execute_sql("SELECT * FROM nobench_main WHERE num BETWEEN 30000 AND 30100;")
        return pjson_db.execute_sql("SELECT * FROM nobench_main WHERE num >= {} AND num <= {};".format(self.arguments[0],
                                                                                                      self.arguments[1]))


class Query7PJson(Query):
    def __init__(self):
        super(Query7PJson, self).__init__("Selection Query 7")

    def prepare(self):
        return None
        data_slice_size = math.ceil(DATA_SIZE * 0.001)
        rand_num = random.randint(1, DATA_SIZE)
        #Changing the parameters of the query based on the trial size.
        self.arguments.append(rand_num)
        self.arguments.append(rand_num + data_slice_size)

    def db_command(self):
        return None
        return pjson_db.execute_sql("SELECT * FROM nobench_main WHERE dyn1 >= {} AND dyn1 <= {};".format(self.arguments[0],
                                                                                                        self.arguments[1]))


class Query8PJson(Query):
    def __init__(self):
        super(Query8PJson, self).__init__("Selection Query 8")

    def prepare(self):
        return None
        global recommended_strings
        random.seed()
        random.shuffle(recommended_strings)
        self.arguments.append(recommended_strings[0])

    def db_command(self):
        return None
        cur = pjson_db.cursor()
        cur.execute("""SELECT objid FROM argo_nobench_main_str WHERE keystr SIMILAR TO 'nested_arr:[\d]+' AND valstr = %s""", (self.arguments[0],))
        return cur

class Query9PJson(Query):
    def __init__(self):
        super(Query9PJson, self).__init__("Selection Query 9")

    def prepare(self):
        return None
        results = pjson_db.execute_sql("SELECT sparse_500 FROM nobench_main")
        for index, result in enumerate(results):

            if index == 5:
                self.arguments.append(result['sparse_500'])


    def db_command(self):
        return None
        return pjson_db.execute_sql('SELECT * FROM nobench_main WHERE sparse_500 = "{}";'.format(self.arguments[0]))


class Query10PJson(Query):
    def __init__(self):
        super(Query10PJson, self).__init__("Aggregation Query 10")

    def prepare(self):
        return None
        #getting 10 percent of data
        data_slice_size = math.ceil(DATA_SIZE * 0.1)
        rand_num = random.randint(1, DATA_SIZE)
        #Changing the parameters of the query based on the trial size.
        self.arguments.append(rand_num)
        self.arguments.append(rand_num + data_slice_size)


    def db_command(self):
        return None
        cur = pjson_db.cursor()
        cur.execute("""DROP TABLE IF EXISTS intermediate;
                       CREATE TEMP TABLE intermediate AS SELECT objid FROM argo_nobench_main_num WHERE keystr = 'num' and valnum BETWEEN %s AND %s;
                       SELECT count(*) FROM argo_nobench_main_num WHERE objid in (SELECT objid FROM intermediate) AND keystr = 'thousandth' GROUP BY valnum""", (self.arguments[0], self.arguments[1]))
        return cur


class Query11PJson(Query):
    def __init__(self):
        super(Query11PJson, self).__init__("Join Query 11")

    def db_command(self):
        return None
        return pjson_db.execute_sql("""SELECT * FROM nobench_main AS left INNER JOIN
                                nobench_main AS right ON (left.nested_obj.str =
                                right.str1) WHERE left.num BETWEEN XXXXX AND YYYYY;""")


class Query12PJson(Query):
    def __init__(self):
        super(Query12PJson, self).__init__("Data Addition Query 12")

    def db_command(self):
        return None

        PrepFilesPJson(PJSON_EXTRA_FILENAME).execute()
        bool_copy_cmd = "COPY argo_nobench_main_bool(objid, keystr, valbool) FROM '{0}' WITH DELIMITER '|';".format(
                PJSON_FILE_DIR + 'nobench_data_argo_extra_bool.txt')
        load_bool = subprocess.Popen(["psql", "-w", "-U", PSQL_USER, "-d", "argo", "-c", bool_copy_cmd],
                                     stdout=subprocess.PIPE)

        num_copy_cmd = "COPY argo_nobench_main_num(objid, keystr, valnum) FROM '{0}' WITH DELIMITER '|';".format(
                PJSON_FILE_DIR + 'nobench_data_argo_extra_num.txt')
        load_num = subprocess.Popen(["psql", "-w", "-U", PSQL_USER, "-d", "argo", "-c", num_copy_cmd],
                                    stdout=subprocess.PIPE)

        str_copy_cmd = "COPY argo_nobench_main_str(objid, keystr, valstr) FROM '{0}' WITH DELIMITER '|';".format(
                PJSON_FILE_DIR + 'nobench_data_argo_extra_str.txt')
        load_str = subprocess.Popen(["psql", "-w", "-U", PSQL_USER, "-d", "argo", "-c", str_copy_cmd],
                                    stdout=subprocess.PIPE)

        load_bool.communicate()
        load_num.communicate()
        load_str.communicate()


class Query13PJson(Query):
    def __init__(self):
        super(Query13PJson, self).__init__("Deep Select Query 13")

    def prepare(self):
        return None
        res = pjson_db.execute_sql('SELECT multiply_nested_obj.level_2.level_3.level_4.level_5.level_6.level_7.level_8.deep_str_single FROM nobench_main')
        index = 5
        for i, result in enumerate(res):
            if i == index:
                word = result['multiply_nested_obj']['level_2']['level_3']['level_4']['level_5']['level_6']['level_7']['level_8']['deep_str_single']
                self.arguments.append(word)
                break

    def db_command(self):
        return None
        return pjson_db.execute_sql('SELECT * FROM  nobench_main WHERE multiply_nested_obj.level_2.level_3.level_4.level_5.level_6.level_7.level_8.deep_str_single = "{}"'.format(self.arguments[0]))


class Query14PJson(Query):
    def __init__(self):
        super(Query14PJson, self).__init__("Deep Select Query 14")

    def prepare(self):
        return None
        res = pjson_db.execute_sql('SELECT multiply_nested_obj.level_2.level_3.level_4.level_5.level_6.level_7.level_8.deep_str_agg FROM nobench_main')
        index = 5
        for i, result in enumerate(res):
            if i == index:
                word = result['multiply_nested_obj']['level_2']['level_3']['level_4']['level_5']['level_6']['level_7']['level_8']['deep_str_agg']
                self.arguments.append(word)
                break

    def db_command(self):
        return None
        return pjson_db.execute_sql("""SELECT multiply_nested_obj.level_2.level_3.level_4.level_5.level_6.level_7.level_8.deep_str_agg
                                        FROM nobench_main
                                        WHERE multiply_nested_obj.level_2.level_3.level_4.level_5.level_6.level_7.level_8.deep_str_agg = "{}";""".format(self.arguments[0]))

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
        print "Starting..."
        PrepFilesPJson(PJSON_FILENAME).execute()

        pjson_load_cmd = "CREATE TABLE pjson_main(data jsonb);"
        pjson_load_cmd += "COPY pjson_main FROM '{0}';".format(
                PJSON_FILE_DIR + PJSON_FILENAME)
        pjson_load_cmd += "CREATE INDEX on pjson_main USING GIN (data);"

        load_pjson = subprocess.Popen(["psql", "-w", "-U", PSQL_USER, "-d", "pjson", "-c", pjson_load_cmd],
                                    stdout=subprocess.PIPE)
        load_pjson.communicate()


def generate_data_pjson(items):
    global recommended_strings

    with open(PJSON_PICKLE_FILENAME, 'wb') as outfile:
        pickle.dump(recommended_strings, outfile)
