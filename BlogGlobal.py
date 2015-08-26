from pymongo import MongoClient
import psycopg2
__author__ = 'Ahmed'

from Settings import PSQL_USER

#INIT MONGO Connection
mongo_client = MongoClient()
print "connected to mongo"
mongo_db = mongo_client.blogcompdb
print "grabbed mongo collection"
mongo_data = mongo_db.sampledata

#INIT PSQL JSONB Direct Connection
pjson_db = psycopg2.connect(
    'dbname=pjson user={0} password=coin0nioc'.format(PSQL_USER)
)
