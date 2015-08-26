import csv
from random import randint
from math import ceil

from Settings import RESULTS_FILENAME, DATA_SIZE

def get_random_data_slice(data_size, slice_percentage):
    slice_size = int(ceil(data_size * slice_percentage))
    slice_start = randint(0, data_size - slice_size)
    print ("found slice from {0} to {1}".format(slice_start, slice_start + slice_size))
    return [slice_start, slice_start + slice_size]


class ResultsFileHandler:
    def __init__(self, filename):
        self.filename = filename

    def write_header(self, system, data_size):
        with open(self.filename, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',)
            writer.writerow(['System', system])
            writer.writerow(['Data_Size', data_size])

    def write_row(self, results_list):
        with open(self.filename, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',)
            writer.writerow(results_list)


class TestSuite:
    def __init__(
        self,
        tag,
        loader,
        cleaner,
        queries_array,
        include_indexes=range(0,12),
        skip_indexes=[],
        obj_count=DATA_SIZE,
    ):
        self.obj_count = obj_count
        self.loader = loader
        self.cleaner = cleaner
        self.tag = tag

        query_indexes = [i for i in include_indexes if i not in skip_indexes]
        if max(query_indexes) > len(queries_array):
            raise IndexError('Requested index greater than number of queries')

        self.queries = [queries_array[i] for i in query_indexes]
        self.query_numbers = [i+1 for i in query_indexes]

        # CSV results file writer
        split_filename = RESULTS_FILENAME.split(".")
        results_filename = "{prefix}_{data_size}_{system}.{extension}".format(
            prefix=split_filename[0],
            data_size=str(self.obj_count),
            system=self.tag,
            extension=split_filename[1],
        )
        self.results = ResultsFileHandler(results_filename)

        self.results.write_header(self.tag, str(self.obj_count))

    def load_data(self):
        load_time = self.loader.execute()
        self.results.write_row(['Load_time', str(load_time)])

    def clean(self):
        self.cleaner.execute()

    def run_bench_queries(self, num_iterations=1):
        queries_header = ['Q'+str(i) for i in self.query_numbers]
        self.results.write_row(queries_header)

        for iteration in xrange(num_iterations):
            results = []
            for query in self.queries:
                results.append(query.execute())
            self.results.write_row(results)
