from pymongo import MongoClient
from argo import demo_init
import psycopg2
__author__ = 'Gary'

#INIT MONGO Connection
mongo_client = MongoClient()
print "connected to mongo"
mongo_db = mongo_client.argocompdb
print "grabbed mongo collection"
data = mongo_db.sampledata

#INIT PSQL Argo Connection
argo_db = demo_init.get_db()
print "connected to argo..."

#INIT PSQL Direct Connection
psql_db = psycopg2.connect("dbname=argo user=tadgh password=coin0nioc")
