import os
import logging

import BlogMongoQueries as MongoQueries
import BlogPJsonQueries as PJsonQueries
from bench_utils import TestSuite
from BlogSettings import (
    RESULTS_FILENAME,
    DATA_SIZE,
    NUM_BENCH_ITERATIONS,
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

###
# Wipe out JSON Documents generated by nobench_data_gen
###
def remove_blog_docs():
    pass


if __name__ == "__main__":
#    q1m = MongoQueries.Query1Mongo()
#    q2m = MongoQueries.Query2Mongo()
#    q3m = MongoQueries.Query3Mongo()
#    q4m = MongoQueries.Query4Mongo()
#    q5m = MongoQueries.Query5Mongo()
#    q6m = MongoQueries.Query6Mongo()
#    q7m = MongoQueries.Query7Mongo()
#    q8m = MongoQueries.Query8Mongo()
#    q9m = MongoQueries.Query9Mongo()
#    q10m = MongoQueries.Query10Mongo()
#    q11m = MongoQueries.Query11Mongo()
#    q12m = MongoQueries.Query12Mongo()
#    q13m = MongoQueries.Query13Mongo()
#    q14m = MongoQueries.Query14Mongo()
#    mongo_loader = MongoQueries.InitialLoadMongo()
#    mongo_dropper = MongoQueries.DropCollectionMongo()
#    mongo_queries = [q1m, q2m, q3m, q4m, q5m, q6m, q7m, q8m, q9m, q10m, q11m, q12m, q13m, q14m]
#    mongo_include_indexes = range(0, 14)
#    mongo_skip_indexes = []
#    mongo_test_suite = TestSuite(
#        tag='Mongo',
#        loader=mongo_loader,
#        cleaner=mongo_dropper,
#        queries_array=mongo_queries,
#        include_indexes=mongo_include_indexes,
#        skip_indexes=mongo_skip_indexes,
#        obj_count=DATA_SIZE,
#    )

    q1p = PJsonQueries.Query1PJson()
    q2p = PJsonQueries.Query2PJson()
    pjson_loader = PJsonQueries.InitialLoadPJson()
    pjson_dropper = PJsonQueries.DropCollectionPJson()
    pjson_queries = [q1p, q2p]
    pjson_include_indexes = range(0, 2)
    pjson_skip_indexes = []
    pjson_test_suite = TestSuite(
        tag='PJsonBlog',
        loader=pjson_loader,
        cleaner=pjson_dropper,
        queries_array=pjson_queries,
        include_indexes=pjson_include_indexes,
        skip_indexes=pjson_skip_indexes,
        obj_count=DATA_SIZE,
    )

    run_mongo_bench = False
    run_pjson_bench = True

    #################################
    #Actual testing area begins here.
    #################################
#    if run_mongo_bench:
#        load_mongo_data = True
#        log.info("Beginning Mongo Benchmark.")
#        if load_mongo_data:
#            log.info("Cleaning out MongoDB.")
#            mongo_test_suite.clean()
#            log.info("Loading new data into MongoDB.")
#            mongo_test_suite.load_data()
#        log.info("Running Mongo Benchmark Queries.")
#        mongo_test_suite.run_bench_queries(NUM_BENCH_ITERATIONS)
#        log.info("Mongo testing suite complete. ")


    if run_pjson_bench:
        load_pjson_data = True
        log.info("Beginning PJson Benchmark.")
        if load_pjson_data:
            log.info("Cleaning out PostgreSQL JSONB.")
            pjson_test_suite.clean()
            log.info("Loading new data into PostgreSQL JSONB.")
            pjson_test_suite.load_data()
        log.info("Running PJson Benchmark Queries.")
        pjson_test_suite.run_bench_queries(NUM_BENCH_ITERATIONS)
        log.info("PJson testing suite complete. ")
