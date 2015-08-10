__author__ = 'Ahmed'

def _add_extra(file_name):
    file_name = file_name.split('.')
    file_name[0] += '_extra'
    return '.'.join(file_name)

ARGO_FILENAME = "nobench_data_argo.json"
GENERIC_FILENAME = "nobench_data.json"
MONGO_FILENAME = "nobench_data_mongo.json"

ARGO_EXTRA_FILENAME = _add_extra(ARGO_FILENAME)
GENERIC_EXTRA_FILENAME = _add_extra(GENERIC_FILENAME)
MONGO_EXTRA_FILENAME = _add_extra(MONGO_FILENAME)

RESULTS_FILENAME = "results.csv"
DATA_SIZE = 100
ARGO_PICKLE_FILENAME = 'rec_strings_argo'
MONGO_PICKLE_FILENAME = "rec_strings_mongo"
DEEPLY_NESTED = True
FAT_OBJECTS = True
