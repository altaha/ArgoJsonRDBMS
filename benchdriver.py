import os
import csv
import logging
from Settings import RESULTS_FILENAME, DATA_SIZE, NUM_BENCH_ITERATIONS
import ArgoQueries
import MongoQueries

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class OutFileHandler:
    def __init__(self, filename):
        self.filename = filename

    def write_headers(self):
        with open(self.filename, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',)
            writer.writerow(['System', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q12', 'Load'])

    def write_row(self, results_list):
        with open(self.filename, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',)
            writer.writerow(results_list)


class TestSuite:
    def __init__(self, obj_count, cleaner, loader, queries, tag):
        self.obj_count = obj_count
        self.queries = queries
        self.cleaner = cleaner
        self.loader = loader
        self.tag = tag

    def load_data(self):
        return self.loader.execute()

    def clean(self):
        self.cleaner.execute()

    def begin_testing(self):
        results = []
        for query in self.queries:
            result = query.execute()
            results.append(result)
        return [self.tag] + results


###
# Wipe out JSON Documents generated by nobench_data_gen
###
def remove_json_docs():
    import Settings
    files = [Settings.MONGO_FILENAME, Settings.MONGO_EXTRA_FILENAME, Settings.ARGO_EXTRA_FILENAME, Settings.ARGO_FILENAME]

    for filename in files:
        if os.path.exists(filename):
            os.remove(filename)


if __name__ == "__main__":
    q1a = ArgoQueries.Query1Argo()
    q2a = ArgoQueries.Query2Argo()
    q3a = ArgoQueries.Query3Argo()
    q4a = ArgoQueries.Query4Argo()
    q5a = ArgoQueries.Query5Argo()
    q6a = ArgoQueries.Query6Argo()
    q7a = ArgoQueries.Query7Argo()
    q8a = ArgoQueries.Query8Argo()
    q9a = ArgoQueries.Query9Argo()
    q10a = ArgoQueries.Query10Argo()
    q12a = ArgoQueries.Query12Argo()
    q13a = ArgoQueries.Query13Argo()
    q14a = ArgoQueries.Query14Argo()
    argo_dropper = ArgoQueries.DropCollectionArgo()
    argo_loader = ArgoQueries.InitialLoadArgo()
    argo_queries = [q1a, q2a, q3a, q4a, q5a, q6a, q7a, q8a, q9a, q10a, q12a]#, q13a, q14a]
    argo_test_suite = TestSuite(DATA_SIZE, argo_dropper, argo_loader, argo_queries, "Argo")

    q1m = MongoQueries.Query1Mongo()
    q2m = MongoQueries.Query2Mongo()
    q3m = MongoQueries.Query3Mongo()
    q4m = MongoQueries.Query4Mongo()
    q5m = MongoQueries.Query5Mongo()
    q6m = MongoQueries.Query6Mongo()
    q7m = MongoQueries.Query7Mongo()
    q8m = MongoQueries.Query8Mongo()
    q9m = MongoQueries.Query9Mongo()
    q10m = MongoQueries.Query10Mongo()
    q12m = MongoQueries.Query12Mongo()
    q13m = MongoQueries.Query13Mongo()
    q14m = MongoQueries.Query14Mongo()


    mongo_queries = [q1m, q2m, q3m, q4m, q5m, q6m, q7m, q8m, q9m, q10m, q12m]#, q13m, q14m]
    mongo_dropper = MongoQueries.DropCollectionMongo()
    mongo_loader = MongoQueries.InitialLoadMongo()
    mongo_test_suite = TestSuite(DATA_SIZE, mongo_dropper, mongo_loader, mongo_queries, "Mongo")


    #preparing our CSV handler
    split_filename = RESULTS_FILENAME.split(".")
    outfile_mongo = OutFileHandler(split_filename[0] + "_" + str(DATA_SIZE) + "_Mongo" + "." + split_filename[1])

    outfile_mongo.write_headers()

    outfile_argo = OutFileHandler(split_filename[0] + "_" + str(DATA_SIZE) + "_Argo" + "." + split_filename[1])
    outfile_argo.write_headers()

    #################################
    #Actual testing area begins here.
    #################################
    generate_new_data = False
    load_new_data = True
    log.info("Beginning Argo Benchmark.")
    for i in range(NUM_BENCH_ITERATIONS):
        if generate_new_data:
            log.info("Argo Generate new Data flag was true. Attempting to remove JSON docs.")
            remove_json_docs()
            log.info("Generating new data of size: {}.".format(DATA_SIZE))
            ArgoQueries.generate_data_argo(DATA_SIZE)
        if load_new_data:
            log.info("Cleaning out PostgreSQL.")
            argo_test_suite.clean()
            log.info("Loading new data into PostgreSQL.")
            load_time = argo_test_suite.load_data()
        else:
            load_time = 0
        log.info("Argo Benchmark iteration {0}".format(i))
        results = argo_test_suite.begin_testing()
        results.append(load_time)
        outfile_argo.write_row(results)
        log.info("Argo testing suite complete. ")
        generate_new_data = False
        load_new_data = False


    generate_new_data = False
    load_new_data = True
    log.info("Beginning Mongo Benchmark.")
    for i in range(NUM_BENCH_ITERATIONS):
        if generate_new_data:
            log.info("Mongo Generate new Data flag was true. Attempting to remove JSON docs.")
            remove_json_docs()
            log.info("Generating new data of size: {}.".format(DATA_SIZE))
            MongoQueries.generate_data_mongo(DATA_SIZE)
        if load_new_data:
            log.info("Cleaning out MongoDB.")
            mongo_test_suite.clean()
            log.info("Loading new data into MongoDB.")
            load_time = mongo_test_suite.load_data()
        else:
            load_time = 0
        log.info("Mongo Benchmark iteration {0}".format(i))
        results = mongo_test_suite.begin_testing()
        results.append(load_time)
        outfile_mongo.write_row(results)
        log.info("Mongo Testing Complete")
        generate_new_data = False
        load_new_data = False
