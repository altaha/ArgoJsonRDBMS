from random import randint
from math import ceil

def get_random_data_slice(data_size, slice_percentage):
    slice_size = int(ceil(data_size * slice_percentage))
    slice_start = randint(0, data_size - slice_size)
    print ("found slice from {0} to {1}".format(slice_start, slice_start + slice_size))
    return [slice_start, slice_start + slice_size]
