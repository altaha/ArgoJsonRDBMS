__author__ = 'Ahmed'

def _add_extra_to_name(file_name):
    file_name = file_name.split('.')
    file_name[0] += '_extra'
    return '.'.join(file_name)

ARGO_FILE_DIR = '/vagrant/ArgoJsonRDBMS/'
MONGO_FILE_DIR = '/vagrant/ArgoJsonRDBMS/'

ARGO_FILENAME = 'nobench_data_argo.json'
GENERIC_FILENAME = 'nobench_data.json'
MONGO_FILENAME = 'nobench_data_mongo.json'

ARGO_EXTRA_FILENAME = _add_extra_to_name(ARGO_FILENAME)
GENERIC_EXTRA_FILENAME = _add_extra_to_name(GENERIC_FILENAME)
MONGO_EXTRA_FILENAME = _add_extra_to_name(MONGO_FILENAME)

PSQL_USER = 'vagrant'
MONGO_USER = 'vagrant'

RESULTS_FILENAME = 'results.csv'
ARGO_PICKLE_FILENAME = 'rec_strings_argo'
MONGO_PICKLE_FILENAME = 'rec_strings_mongo'

DATA_SIZE = 100000
NUM_BENCH_ITERATIONS = 10
DEEPLY_NESTED = True
FAT_OBJECTS = True
