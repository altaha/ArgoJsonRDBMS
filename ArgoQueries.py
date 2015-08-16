import logging
import random
import subprocess
import math
from Query import Query
import pickle
import json2bulksql
import nobench_gendata

__author__ = 'Gary'

from Global import argo_db, psql_db
from Settings import (
    ARGO_FILENAME,
    ARGO_EXTRA_FILENAME,
    ARGO_PICKLE_FILENAME,
    PSQL_USER,
    DATA_SIZE,
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


try:
    with open(ARGO_PICKLE_FILENAME, 'rb') as infile:
        recommended_strings = pickle.load(infile)
except Exception as e:
    log.error("Couldn't find pickle file!!", str(e))
    recommended_strings = []


class PrepFilesArgo(Query):
    def __init__(self, filename):
        super(PrepFilesArgo, self).__init__("Preparing files for Argo consumption")
        self.filename = filename

    def db_command(self):
        json2bulksql.convertFile(self.filename, 0, True, False)


class Query1Argo(Query):
    def __init__(self):
        super(Query1Argo, self).__init__("Projection Query 1")

    def db_command(self):
        return argo_db.execute_sql("SELECT str1, num FROM nobench_main;")


class Query2Argo(Query):
    def __init__(self):
        super(Query2Argo, self).__init__("Projection Query 2")

    def db_command(self):
        return argo_db.execute_sql("SELECT nested_obj.str1, nested_obj.num FROM nobench_main;")


class Query3Argo(Query):
    def __init__(self):
        super(Query3Argo, self).__init__("Projection Query 3")

    def db_command(self):
        return argo_db.execute_sql("SELECT sparse_110, sparse_119 FROM nobench_main;")


class Query4Argo(Query):
    def __init__(self):
        super(Query4Argo, self).__init__("Projection Query 4")

    def db_command(self):
        return argo_db.execute_sql("SELECT sparse_110, sparse_220 FROM nobench_main;")


class Query5Argo(Query):
    def __init__(self):
        super(Query5Argo, self).__init__("Selection Query 5")

    def prepare(self):
        halfway_index = DATA_SIZE / 2
        results = argo_db.execute_sql("SELECT str1 FROM nobench_main")
        for index, result in enumerate(results):

            if index == halfway_index:
                self.arguments.append(result['str1'])

    def db_command(self):
        return argo_db.execute_sql(
            'SELECT * FROM nobench_main WHERE str1 = "{}";'.format(self.arguments[0]))


class Query6Argo(Query):
    def __init__(self):
        super(Query6Argo, self).__init__("Selection Query 6")

    def prepare(self):
        data_slice_size = math.ceil(DATA_SIZE * 0.001)
        rand_num = random.randint(1, DATA_SIZE)
        #Changing the parameters of the query based on the trial size.
        self.arguments.append(rand_num)
        self.arguments.append(rand_num + data_slice_size)

    def db_command(self):
        # return argo_db.execute_sql("SELECT * FROM nobench_main WHERE num BETWEEN 30000 AND 30100;")
        return argo_db.execute_sql("SELECT * FROM nobench_main WHERE num >= {} AND num <= {};".format(self.arguments[0],
                                                                                                      self.arguments[1]))


class Query7Argo(Query):
    def __init__(self):
        super(Query7Argo, self).__init__("Selection Query 7")

    def prepare(self):
        data_slice_size = math.ceil(DATA_SIZE * 0.001)
        rand_num = random.randint(1, DATA_SIZE)
        #Changing the parameters of the query based on the trial size.
        self.arguments.append(rand_num)
        self.arguments.append(rand_num + data_slice_size)

    def db_command(self):
        return argo_db.execute_sql("SELECT * FROM nobench_main WHERE dyn1 >= {} AND dyn1 <= {};".format(self.arguments[0],
                                                                                                        self.arguments[1]))


class Query8Argo(Query):
    def __init__(self):
        super(Query8Argo, self).__init__("Selection Query 8")

    def prepare(self):
        global recommended_strings
        random.seed()
        random.shuffle(recommended_strings)
        self.arguments.append(recommended_strings[0])

    def db_command(self):
        #return argo_db.execute_sql('SELECT * FROM nobench_main WHERE "{}" = ANY nested_arr;'.format(self.arguments[0]))
        cur = psql_db.cursor()
        cur.execute("""SELECT objid FROM argo_nobench_main_str WHERE keystr SIMILAR TO 'nested_arr:[\d]+' AND valstr = %s""", (self.arguments[0],))
        return cur

class Query9Argo(Query):
    def __init__(self):
        super(Query9Argo, self).__init__("Selection Query 9")

    def prepare(self):
        results = argo_db.execute_sql("SELECT sparse_500 FROM nobench_main")
        for index, result in enumerate(results):

            if index == 5:
                self.arguments.append(result['sparse_500'])


    def db_command(self):
        return argo_db.execute_sql('SELECT * FROM nobench_main WHERE sparse_500 = "{}";'.format(self.arguments[0]))


class Query10Argo(Query):
    def __init__(self):
        super(Query10Argo, self).__init__("Aggregation Query 10")

    def prepare(self):
        #getting 10 percent of data
        data_slice_size = math.ceil(DATA_SIZE * 0.1)
        rand_num = random.randint(1, DATA_SIZE)
        #Changing the parameters of the query based on the trial size.
        self.arguments.append(rand_num)
        self.arguments.append(rand_num + data_slice_size)


    def db_command(self):
        cur = psql_db.cursor()
        cur.execute("""DROP TABLE IF EXISTS intermediate;
                       CREATE TEMP TABLE intermediate AS SELECT objid FROM argo_nobench_main_num WHERE keystr = 'num' and valnum BETWEEN %s AND %s;
                       SELECT count(*) FROM argo_nobench_main_num WHERE objid in (SELECT objid FROM intermediate) AND keystr = 'thousandth' GROUP BY valnum""", (self.arguments[0], self.arguments[1]))
        return cur


class Query11Argo(Query):
    def __init__(self):
        super(Query11Argo, self).__init__("Join Query 11")

    def db_command(self):
        return argo_db.execute_sql("""SELECT * FROM nobench_main AS left INNER JOIN
                                nobench_main AS right ON (left.nested_obj.str =
                                right.str1) WHERE left.num BETWEEN XXXXX AND YYYYY;""")


class Query12Argo(Query):
    def __init__(self):
        super(Query12Argo, self).__init__("Data Addition Query 12")

    def db_command(self):

        PrepFilesArgo(ARGO_EXTRA_FILENAME).execute()
        load_bool = subprocess.Popen(["psql", "-w", "-U", PSQL_USER, "-d", "argo", "-c",
                                      "COPY argo_nobench_main_bool(objid, keystr, valbool) FROM 'D:\\Dropbox\\Argo Vs Mongo Project\\nobench\\nobench_data_argo_extra_bool.txt' WITH DELIMITER '|';"],
                                     stdout=subprocess.PIPE)
        load_num = subprocess.Popen(["psql", "-w", "-U", PSQL_USER, "-d", "argo", "-c",
                                     "COPY argo_nobench_main_num(objid, keystr, valnum) FROM 'D:\\Dropbox\\Argo Vs Mongo Project\\nobench\\nobench_data_argo_extra_num.txt' WITH DELIMITER '|';"],
                                    stdout=subprocess.PIPE)
        load_str = subprocess.Popen(["psql", "-w", "-U", PSQL_USER, "-d", "argo", "-c",
                                     "COPY argo_nobench_main_str(objid, keystr, valstr) FROM 'D:\\Dropbox\\Argo Vs Mongo Project\\nobench\\nobench_data_argo_extra_str.txt' WITH DELIMITER '|';"],
                                    stdout=subprocess.PIPE)

        load_bool.communicate()
        load_num.communicate()
        load_str.communicate()


class Query13Argo(Query):
    def __init__(self):
        super(Query13Argo, self).__init__("Deep Select Query 13")

    def prepare(self):
        res = argo_db.execute_sql('SELECT multiply_nested_obj.level_2.level_3.level_4.level_5.level_6.level_7.level_8.deep_str_single FROM nobench_main')
        index = 5
        for i, result in enumerate(res):
            if i == index:
                word = result['multiply_nested_obj']['level_2']['level_3']['level_4']['level_5']['level_6']['level_7']['level_8']['deep_str_single']
                self.arguments.append(word)
                break

    def db_command(self):
        return argo_db.execute_sql('SELECT * FROM  nobench_main WHERE multiply_nested_obj.level_2.level_3.level_4.level_5.level_6.level_7.level_8.deep_str_single = "{}"'.format(self.arguments[0]))


class Query14Argo(Query):
    def __init__(self):
        super(Query14Argo, self).__init__("Deep Select Query 14")

    def prepare(self):
        res = argo_db.execute_sql('SELECT multiply_nested_obj.level_2.level_3.level_4.level_5.level_6.level_7.level_8.deep_str_agg FROM nobench_main')
        index = 5
        for i, result in enumerate(res):
            if i == index:
                word = result['multiply_nested_obj']['level_2']['level_3']['level_4']['level_5']['level_6']['level_7']['level_8']['deep_str_agg']
                self.arguments.append(word)
                break

    def db_command(self):
        return argo_db.execute_sql("""SELECT multiply_nested_obj.level_2.level_3.level_4.level_5.level_6.level_7.level_8.deep_str_agg
                                        FROM nobench_main
                                        WHERE multiply_nested_obj.level_2.level_3.level_4.level_5.level_6.level_7.level_8.deep_str_agg = "{}";""".format(self.arguments[0]))

class DropCollectionArgo(Query):
    def __init__(self):
        super(DropCollectionArgo, self).__init__("Dropping Data from Argo")

    def db_command(self):
        return argo_db.execute_sql("DELETE FROM nobench_main")


class InitialLoadArgo(Query):
    def __init__(self):
        super(InitialLoadArgo, self).__init__("Loading Initial Data into Argo")

    def db_command(self):
        print "Starting..."
        PrepFilesArgo(ARGO_FILENAME).execute()

        load_bool = subprocess.Popen(["psql", "-w", "-U", PSQL_USER, "-d", "argo", "-c",
                                      "COPY argo_nobench_main_bool(objid, keystr, valbool) FROM 'D:\\Dropbox\\Argo Vs Mongo Project\\nobench\\nobench_data_argo_bool.txt' WITH DELIMITER '|';"],
                                     stdout=subprocess.PIPE)
        load_num = subprocess.Popen(["psql", "-w", "-U", PSQL_USER, "-d", "argo", "-c",
                                     "COPY argo_nobench_main_num(objid, keystr, valnum) FROM 'D:\\Dropbox\\Argo Vs Mongo Project\\nobench\\nobench_data_argo_num.txt' WITH DELIMITER '|';"],
                                    stdout=subprocess.PIPE)
        load_str = subprocess.Popen(["psql", "-w", "-U", PSQL_USER, "-d", "argo", "-c",
                                     "COPY argo_nobench_main_str(objid, keystr, valstr) FROM 'D:\\Dropbox\\Argo Vs Mongo Project\\nobench\\nobench_data_argo_str.txt' WITH DELIMITER '|';"],
                                    stdout=subprocess.PIPE)

        load_bool.communicate()
        load_num.communicate()
        load_str.communicate()


def generate_data_argo(items):
    global recommended_strings


    recommended_strings = nobench_gendata.main_non_cli(items, False, ARGO_FILENAME)
    with open(ARGO_PICKLE_FILENAME, 'wb') as outfile:
        pickle.dump(recommended_strings, outfile)
