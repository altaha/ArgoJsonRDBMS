import json
import logging
import math
import random
import subprocess

from bench_utils import get_random_data_slice
from Query import Query
from BlogGlobal import pjson_db
from BlogSettings import (
    DATA_SIZE,
    FILES_DIR,
    PJSON_FILENAME,
    PSQL_USER,
)

__author__ = 'Ahmed'

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class Query1PJson(Query):
    def __init__(self):
        super(Query1PJson, self).__init__("Selection Query 1")

    def prepare(self):
        # getting 10 percent of data
        self.arguments = get_random_data_slice(DATA_SIZE, 0.1)

    def db_command(self):
        cur = pjson_db.cursor()
        cur.execute(
            "SELECT * FROM pjson_blog WHERE CAST(data->>'user_id' AS integer) >= {}"
            " AND CAST(data->>'user_id' AS integer) < {};".format(
                self.arguments[0], self.arguments[1]
            )
        )
        return cur


class Query2PJson(Query):
    def __init__(self):
        super(Query2PJson, self).__init__("Selection Query 2")

    def prepare(self):
        # getting 10 percent of data
        self.arguments = get_random_data_slice(DATA_SIZE, 0.1)

    def db_command(self):
        jsonb_query = (
            "Drop TABLE IF EXISTS temptable;"
            " SELECT jsonb_array_elements(jsonb_array_elements("
            "data -> 'authored') -> 'comments')"
            " AS comments INTO temptable FROM pjson_blog;"
            " SELECT * FROM temptable WHERE CAST(comments->>'user_id' AS integer) >= {0}"
            " AND CAST(comments->>'user_id' AS integer) < {1};".format(
                self.arguments[0], self.arguments[1]
            )
        )
        cur = pjson_db.cursor()
        cur.execute(jsonb_query)
        return cur


class DropCollectionPJson(Query):
    def __init__(self):
        super(DropCollectionPJson, self).__init__("Dropping Data from PJson Blog")

    def db_command(self):
        pjson_drop_cmd = "DROP TABLE pjson_blog; DROP TABLE temptable;"
        drop_pjson = subprocess.Popen(["psql", "-w", "-U", PSQL_USER, "-d", "pjson", "-c", pjson_drop_cmd],
                                    stdout=subprocess.PIPE)
        drop_pjson.communicate()


class InitialLoadPJson(Query):
    def __init__(self):
        super(InitialLoadPJson, self).__init__("Loading Initial Data into PJson")

    def db_command(self):
        pjson_load_cmd = "CREATE TABLE pjson_blog(data jsonb);"
        pjson_load_cmd += "COPY pjson_blog FROM '{0}';".format(
                FILES_DIR + PJSON_FILENAME)
        pjson_load_cmd += "CREATE INDEX on pjson_blog USING GIN (data);"

        load_pjson = subprocess.Popen(["psql", "-w", "-U", PSQL_USER, "-d", "pjson", "-c", pjson_load_cmd],
                                    stdout=subprocess.PIPE)
        load_pjson.communicate()
