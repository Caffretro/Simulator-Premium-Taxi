import numpy as np
import pandas as pd
from numpy import *
import pickle
import random

RATIO_NOISE = 0.02
driver_behaviour_scalar = pickle.load(open('./driver_behaviour_scaler.pkl', 'rb'))
driver_behaviour_model = pickle.load(open('./Driver_Behaviour.pickle', 'rb'))

def driver_decision(distance, reward, lr_model):
    """

    :param reward: numpyarray, price of order
    :param distance: numpyarray, distance between current order to all drivers
    :param numpyarray: n, price of order
    :return: pandas.DataFrame, the probability of drivers accept the order.
    """
    r_dis, c_dis = distance.shape
    temp_ = np.dstack((distance, reward)).reshape(-1, 2)
    temp_ = driver_behaviour_scalar.transform(temp_)
    result = lr_model.predict_proba(temp_).reshape(r_dis, c_dis, 2)
    result = np.delete(result, 0, axis=2)
    result = np.squeeze(result, axis=2)
    return result



def generate_random_num(length):
    if length < 1:
        res = 0
    else:
        res = random.randint(0, length)
    return res

def dispatch_broadcasting(order_driver_info, dis_array,broadcasting_scale=1):
    """

    :param order_driver_info: the information of drivers and orders
    :param broadcasting_scale: the radius of order broadcasting
    :return: matched driver order pair
    """
    columns_name = ['origin_lng', 'origin_lat', 'order_id', 'reward_units', 'origin_grid_id', 'driver_id',
                    'pick_up_distance']

    order_driver_info = pd.DataFrame(order_driver_info, columns=columns_name)

    id_order = order_driver_info['order_id'].unique()
    id_driver = order_driver_info['driver_id'].unique()

    # num of orders and drivers
    num_order = order_driver_info['order_id'].nunique()
    num_driver = order_driver_info['driver_id'].nunique()
    dis_array = np.array(dis_array, dtype='float32')
    distance_driver_order = dis_array.reshape(num_order, num_driver)
    price_array = np.array(order_driver_info['reward_units'], dtype='float32').reshape(num_order, num_driver)
    radius_array = np.full((num_order, num_driver), broadcasting_scale)
    driver_decision_info = driver_decision(distance_driver_order, price_array, driver_behaviour_model)
    '''
    Choose Driver with probability
    '''
    for i in range(num_order):
        for j in range(num_driver):
            if distance_driver_order[i, j] > radius_array[i, j]:
                driver_decision_info[i, j] = 0  # delete drivers further than broadcasting_scale
                # match_state_array[i, j] = 2

    random.seed(10)
    temp_random = np.random.random((num_order, num_driver))
    driver_pick_flag = (driver_decision_info > temp_random) + 0
    driver_id_list = []
    order_id_list = []
    reward_list = []
    pick_up_distance_list = []
    index = 0
    for row in driver_pick_flag:
        temp_line = np.argwhere(row == 1)
        if len(temp_line) >= 1:
            temp_num = generate_random_num(len(temp_line) - 1)
            row[:] = 0
            row[temp_line[temp_num, 0]] = 1
            driver_pick_flag[index, :] = row
            driver_pick_flag[index + 1:, temp_line[temp_num, 0]] = 0

        index += 1
    matched_pair = np.argwhere(driver_pick_flag == 1)
    matched_dict = {}
    for item in matched_pair:
        matched_dict[id_order[item[0]]] = [id_driver[item[1]], price_array[item[0], item[1]],
                                           distance_driver_order[item[0], item[1]]]
        driver_id_list.append(id_driver[item[1]])
        order_id_list.append(id_order[item[0]])
        reward_list.append(price_array[item[0], item[1]])
        pick_up_distance_list.append(distance_driver_order[item[0], item[1]])
    result = []
    for item in id_order.tolist():
        if item in matched_dict:
            result.append([item, matched_dict[item][0], matched_dict[item][1], matched_dict[item][2]])
    '''
        result may look like this:
        order_id, driver_id, reward, distance
        [
            [1, 'driver_1', 10.0, 0.5],
            [2, 'driver_2', 12.0, 0.5],
        ]
    '''
    return result

