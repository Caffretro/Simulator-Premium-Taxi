# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 19:20:13 2018

@author: kejintao

input information:
1. demand patterns (on minutes)
2. demand databases
3. drivers' working schedule (online/offline time)

** All the inputs are obtained from env, thus we do not need to alter parameters here
"""

from dataclasses import replace
from lib2to3.pgen2 import driver
import numpy as np
import pandas as pd
from copy import deepcopy
import random
from config import *
from path import *
import pickle
import sys


class SimulatorPattern(object):
    def __init__(self, **kwargs):
        # read parameters
        self.simulator_mode = kwargs.pop('simulator_mode', 'simulator_mode')
        self.request_file_name = kwargs['request_file_name']
        self.driver_file_name = kwargs['driver_file_name']
        self.sample_driver_size = kwargs['sample_driver_size']

        if self.simulator_mode == 'toy_mode':

            # load and sample orders

            self.request_all = pickle.load(open(data_path + self.request_file_name + '.pickle', 'rb'))
            # data = pickle.load(open(data_path + self.request_file_name + '.pickle', 'rb'))
            # sampled_dict = {}
            # order_sample_size = 989300
            # start_num = 1
            # # end_num = 663694 # total num of 1 month's orders
            # end_num = 1211996 # total num of 2 months' orders
            # random.seed(42)
            # sampled_integers = random.sample(range(start_num, end_num + 1), order_sample_size)

            # # Iterate over the keys and sample each key's values
            # for key, values in data.items():
            #     # Select half of the values
            #     sampled_values = []
            #     for value in values:
            #         if value[0] in sampled_integers:
            #             sampled_values.append(value)
            #     # Add the sampled values to the new dictionary
            #     sampled_dict[key] = sampled_values
            # self.request_all = sampled_dict
            

            # load and sample drivers
            

            # Notice: since we are using full data to test sensitivity, no need to sample
            self.driver_info = pickle.load(open(load_path + self.driver_file_name + '.pickle', 'rb'))


            # self.driver_info = self.driver_info.sample(n=env_params['driver_num'],replace=False)
            all_drivers = pd.unique(self.driver_info['driver_id'])
            random.seed(42)
            driver_sample_size = self.sample_driver_size # 9402 for full data
            drivers_to_keep = random.sample(list(all_drivers), driver_sample_size)
            print("keeping", len(drivers_to_keep), "unique driver_id")

            # since this is baseline model, no need to check test or train
            self.driver_info = self.driver_info[self.driver_info['driver_id'].isin(drivers_to_keep)]
            
            # self.driver_info = self.driver_info.sample(n=env_params['driver_num'])
            # print(self.driver_info)
