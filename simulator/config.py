env_params = {
't_initial' :0,   # 3-9
't_end' : 86400,
'delta_t' : 5,  # s
'vehicle_speed' : 20.6,   # km / h
'repo_speed' :20.6, #目前的设定需要与vehicl speed保持一致
'order_sample_ratio' : 1,
'order_generation_mode' : 'sample_from_base',
'driver_sample_ratio' : 1,
'maximum_wait_time_mean' : 300,
'maximum_wait_time_std' : 0,
"maximum_pickup_time_passenger_can_tolerate_mean":float('inf'),  # s
"maximum_pickup_time_passenger_can_tolerate_std":0, # s
"maximum_price_passenger_can_tolerate_mean":float('inf'), # ￥
"maximum_price_passenger_can_tolerate_std":0,  # ￥
'maximal_pickup_distance' : 1,  # km
'request_interval':5,  #
'cruise_flag' :True,
'delivery_mode':'rg',
'pickup_mode':'rg',
'max_idle_time' : 300,  # 1s and 300s
'cruise_mode': 'random',   # modify
'reposition_flag': False,
'eligible_time_for_reposition' : 300, # s
'reposition_mode': '',
'track_recording_flag' : False,
'driver_far_matching_cancel_prob_file' : 'driver_far_matching_cancel_prob',
# 'request_file_name' : 'input1/hongkong_processed_order_new_road_network_for_10000_drivers_800000', #'toy_requests',
'request_file_name' : 'input1/hongkong_processed_order_new_road_network_60000', #'toy_requests',
'driver_file_name' : 'input1/hongkong_driver_info_allday',
'road_network_file_name' : 'road_network_information.pickle',
'dispatch_method': 'LD', #LD: lagarange decomposition method designed by Peibo Duan
# 'method': 'instant_reward_no_subway',
'simulator_mode' : 'toy_mode',
'experiment_mode' : 'test',
'driver_num':10000, # 9402 note that changing here is useless, go to main's very top part to modify driver_num array
'side':10,
'price_per_km':5,  # ￥ / kmss
'road_information_mode':'load',
'price_increasing_percentage': 0.2,
# 'premium_taxi_mode': True,
'premium_taxi_increasing_coefficient': 1.2, # assume premium taxi is 20% more expensive than normal taxi
'accept_premium_ratio': 0.2, # assume 20% of the drivers are premium taxi
'premium_driver_num': 30,
'north_lat': 22.55,
'south_lat': 22.13,
'east_lng': 114.42,
'west_lng': 113.81, # Hong Kong coordinates
'rl_mode': 'matching',  # reposition and matching
'method': 'instant_reward_no_subway',  #  'sarsa_no_subway' / 'pickup_distance' / 'instant_reward_no_subway'   #  rl for matching
'reposition_method': 'random_cruise',  # A2C, A2C_global_aware, random_cruise, stay  # rl for repositioning
'dayparting': False, # if true, simulator_env will compute information based on time periods in a day, e.g. 'morning', 'afternoon'
}
wait_time_params_dict = {'morning': [2.582, 2.491, 0.026, 1.808, 2.581],
                    'evening': [4.862, 2.485, 0, 1.379, 13.456],
                    'midnight_early': [0, 2.388, 2.972, 2.954, 3.14],
                    'other': [0, 2.017, 2.978, 2.764, 2.973]}

pick_time_params_dict = {'morning': [1.877, 2.018, 2.691, 1.865, 6.683],
                    'evening': [2.673,2.049,2.497,1.736,9.208],
                    'midnight_early': [3.589,2.319,2.185,1.664,9.6],
                    'other': [0,1.886,4.099,3.185,3.636]}

# price_params_dict = {'short': [1.245,0.599,10.629,10.305,0.451],
#                     'short_medium': [0.451,0.219,19.585,58.407,0.18],
#                     'medium_long': [14.411,4.421,11.048,9.228,145],
#                     'long': [15.821,3.409,0,16.221,838.587]}

price_params_dict = {'short': [0.8393972974276114, 24.794554808478033, 6.815738967628449],
                    'short_medium': [-7.201468821915991, 64.4190455714694, 21.876342234268932],
                    'medium_long': [224.0591773703033, 102.0691349634478, 58.902692735890035],
                    'long': [-0.07803413752462217, 266.0959888157933, 53.462130123196246]}

# price_increase_params_dict = {'morning': [0.001,1.181,3.583,4.787,0.001],
#                     'evening': [0,1.21,2.914,5.023,0.013],
#                     'midnight_early': [1.16,0,0,6.366,0],
#                     'other': [0,2.053,0.857,4.666,1.961]}
#  rl for matching
# global variable and parameters for sarsa
START_TIMESTAMP = 10800  # the start timestamp
LEN_TIME_SLICE = 300  # the length of a time slice, 5 minute (300 seconds) in this experiment
LEN_TIME = 6 * 60 * 60 # 3 hours
NUM_EPOCH = 1  # 4001 / 3001
FLAG_LOAD = False
sarsa_params = dict(learning_rate=0.005, discount_rate=0.95)  # parameters in sarsa algorithm
#  rl for matching

# rl for repositioning
# hyperparameters for rl
# NUM_EPOCH = 1301
STOP_EPOCH = 1300
DISCOUNT_FACTOR = 0.95
ACTOR_LR = 0.001
CRITIC_LR = 0.005
ACTOR_STRUCTURE = [64,128] #[16, 32] for A2C, and [64, 128] for A2C global aware
CRITIC_STRUCTURE = [64,128]
# rl for repositioning


#  rl for matching
# parameters for exploration
INIT_EPSILON = 0.9
FINAL_EPSILON = 0
DECAY = 0.997
PRE_STEP = 0
#  rl for matching

#  rl for matching
TRAIN_DATE_LIST = ['2015-05-04','2015-05-05','2015-05-06','2015-05-07','2015-05-08',]

TEST_DATE_LIST = ['2015-05-11']#['2015-05-11', '2015-05-12', '2015-05-13', '2015-05-14', '2015-05-15']
#  rl for matching