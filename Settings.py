__author__ = 'Ahmed'

def _add_extra_to_name(file_name):
    file_name = file_name.split('.')
    file_name[0] += '_extra'
    return '.'.join(file_name)

FILES_DIR = '/home/vagrant/workspace/ArgoBench/ArgoJsonRDBMS/'

ARGO_FILENAME = 'nobench_data_argo.json'
GENERIC_FILENAME = 'nobench_data.json'
MONGO_FILENAME = 'nobench_data_mongo.json'
PJSON_FILENAME = 'nobench_data_mongo.json'

ARGO_EXTRA_FILENAME = _add_extra_to_name(ARGO_FILENAME)
GENERIC_EXTRA_FILENAME = _add_extra_to_name(GENERIC_FILENAME)
MONGO_EXTRA_FILENAME = _add_extra_to_name(MONGO_FILENAME)
PJSON_EXTRA_FILENAME = _add_extra_to_name(PJSON_FILENAME)

PSQL_USER = 'vagrant'
MONGO_USER = 'vagrant'

RESULTS_FILENAME = 'results.csv'
ARGO_PICKLE_FILENAME = 'rec_strings_argo'
MONGO_PICKLE_FILENAME = 'rec_strings_mongo'
PJSON_PICKLE_FILENAME = 'rec_strings_mongo'

#DATA_SIZE = 1000000
#NUM_BENCH_ITERATIONS = 10
DATA_SIZE = 20000
NUM_BENCH_ITERATIONS = 1
DEEPLY_NESTED = True
