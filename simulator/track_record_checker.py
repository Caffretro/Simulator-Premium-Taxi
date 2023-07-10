import numpy as np
import pickle
import pandas as pd

def check_track_records():
    data = pickle.load(open('./output20/rg_rg_cruise=True/records_driver_num_100.pickle', 'rb'))
    print(data)

if __name__ == '__main__':
    check_track_records()