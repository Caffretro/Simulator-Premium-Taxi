from simulator_env import Simulator
import pickle
import numpy as np
from config import *
from path import *
import time
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")
import os
from utilities import *
from sarsa import SarsaAgent
from matplotlib import pyplot as plt

if __name__ == "__main__":
    driver_num = [750]
    max_distance_num = [1]

    cruise_flag = [True]
    pickup_flag = ['rg']
    delivery_flag = ['rg']

    # track的格式为[{'driver_1' : [[lng, lat, status, time_a], [lng, lat, status, time_b]],
    # 'driver_2' : [[lng, lat, status, time_a], [lng, lat, status, time_b]]},
    # {'driver_1' : [[lng, lat, status, time_a], [lng, lat, status, time_b]]}]
    for pc_flag in pickup_flag:
        for dl_flag in delivery_flag:
            for cr_flag in cruise_flag:
                for single_driver_num in driver_num:
                    for single_max_distance_num in max_distance_num:
                        env_params['pickup_mode'] = pc_flag
                        env_params['delivery_mode'] = dl_flag
                        env_params['cruise_flag'] = cr_flag
                        env_params['driver_num'] = single_driver_num
                        env_params['maximal_pickup_distance'] = single_max_distance_num

                        simulator = Simulator(**env_params)
                        simulator.reset()
                        track_record = []
                        t = time.time()

                        if env_params['rl_mode'] == "matching":
                            if simulator.experiment_mode == 'test':
                                column_list = ['total_reward', 'matched_request_num',
                                               'long_request_num',
                                               'matched_long_request_num', 'matched_medium_request_num',
                                               'medium_request_num',
                                               'matched_short_request_num',
                                               'short_request_num', 'total_request_num',
                                               'waiting_time','pickup_time','occupancy_rate','occupancy_rate_no_pickup',
                                               'matched_long_request_ratio', 'matched_medium_request_ratio',
                                               'matched_short_request_ratio',
                                               'matched_request_ratio']
                                test_num = 1
                                test_interval = 20
                                threshold = 5
                                df = pd.DataFrame(np.zeros([test_num, len(column_list)]), columns=column_list)
                                # df = pickle.load(open(load_path + 'performance_record_test_' + env_params['method'] + '.pickle', 'rb'))
                                remaining_index_array = np.where(df['total_reward'].values == 0)[0]
                                if len(remaining_index_array > 0):
                                    last_stopping_index = remaining_index_array[0]
                                ax,ay = [],[]
                                
                                epoch = 0
                                for num in range(last_stopping_index, test_num):
                                    print('num: ', num)
                                    # simulator = Simulator(**env_params)
                                    agent = {}
                                    if simulator.method in ['sarsa', 'sarsa_no_subway', 'sarsa_travel_time',
                                                            'sarsa_travel_time_no_subway',
                                                            'sarsa_total_travel_time', 'sarsa_total_travel_time_no_subway']:
                                        agent = SarsaAgent(**sarsa_params)
                                        agent.load_parameters(
                                            load_path + 'episode_4000\\sarsa_q_value_table_epoch_4000.pickle')

                                    total_reward = 0
                                    total_reward_premium = 0
                                    total_request_num = 0
                                    long_request_num = 0
                                    medium_request_num = 0
                                    short_request_num = 0
                                    matched_request_num = 0
                                    matched_long_request_num = 0
                                    matched_medium_request_num = 0
                                    matched_short_request_num = 0
                                    occupancy_rate = 0
                                    occupancy_rate_normal = 0
                                    occupancy_rate_premium = 0
                                    occupancy_rate_per_hour = [0] * 24
                                    occupancy_rate_per_hour_normal = [0] * 24
                                    occupancy_rate_per_hour_premium = [0] * 24
                                    occupancy_rate_no_pickup = 0
                                    pickup_time = 0
                                    waiting_time = 0

                                    # load models for broadcasting

                                    for date in TEST_DATE_LIST:
                                        simulator.experiment_date = date
                                        simulator.reset()
                                        start_time = time.time()
                                        # stepwise_time = time.time()
                                        for step in range(simulator.finish_run_step):
                                            # stepwise_time = time.time()
                                            # dispatch_transitions = simulator.rl_step(agent)

                                            # for full-data testing, no need to store dispatch transition, store track instead.
                                            new_tracks = simulator.step(agent)
                                            track_record.append(new_tracks)
                                            
                                            if step % 500 == 0:
                                                print("At step {}".format(step))

                                        end_time = time.time()

                                        total_reward += simulator.total_reward
                                        total_reward_premium += simulator.total_reward_premium
                                        total_request_num += simulator.total_request_num
                                        occupancy_rate += simulator.occupancy_rate
                                        occupancy_rate += simulator.occupancy_rate_normal
                                        occupancy_rate_premium += simulator.occupancy_rate_premium
                                        occupancy_rate_per_hour = simulator.per_hour_occupancy_rate[:]
                                        occupancy_rate_per_hour_normal = simulator.per_hour_occupancy_rate_normal[:]
                                        occupancy_rate_per_hour_premium = simulator.per_hour_occupancy_rate_premium[:]
                                        matched_request_num += simulator.matched_requests_num
                                        long_request_num += simulator.long_requests_num
                                        medium_request_num += simulator.medium_requests_num
                                        short_request_num += simulator.short_requests_num
                                        matched_long_request_num += simulator.matched_long_requests_num
                                        matched_medium_request_num += simulator.matched_medium_requests_num
                                        matched_short_request_num += simulator.matched_short_requests_num
                                        occupancy_rate_no_pickup += simulator.occupancy_rate_no_pickup
                                        pickup_time += simulator.pickup_time / simulator.matched_requests_num
                                        waiting_time += simulator.waiting_time / simulator.matched_requests_num
                                    
                                    
                                    epoch += 1
                                    total_reward = total_reward / len(TEST_DATE_LIST)
                                    ax.append(epoch)
                                    ay.append(total_reward)
                                    print("start_time and end_time:", start_time, end_time)
                                    print("total revenue",total_reward*24)
                                    print("total premium reward",total_reward_premium,
                                          "premium monthly revenue", total_reward_premium * 15 / float(env_params['premium_driver_num']))
                                    print("total normal driver reward", total_reward - total_reward_premium,
                                          "regular monthly revenue", (total_reward - total_reward_premium) * 15 / single_driver_num)
                                    print(f"total matched premium orders: {simulator.matched_premium_order_count}, regular orders: {simulator.matched_regular_order_count}")
                                    total_request_num = total_request_num / len(TEST_DATE_LIST)
                                    occupancy_rate = occupancy_rate / len(TEST_DATE_LIST)
                                    matched_request_num = matched_request_num / len(TEST_DATE_LIST)
                                    long_request_num = long_request_num / len(TEST_DATE_LIST)
                                    medium_request_num = medium_request_num / len(TEST_DATE_LIST)
                                    short_request_num = short_request_num / len(TEST_DATE_LIST)
                                    matched_long_request_num = matched_long_request_num / len(TEST_DATE_LIST)
                                    matched_medium_request_num = matched_medium_request_num / len(TEST_DATE_LIST)
                                    matched_short_request_num = matched_short_request_num / len(TEST_DATE_LIST)
                                    occupancy_rate_no_pickup = occupancy_rate_no_pickup / len(TEST_DATE_LIST)
                                    pickup_time = pickup_time / len(TEST_DATE_LIST)
                                    waiting_time = waiting_time / len(TEST_DATE_LIST)
                                    print("pick",pickup_time)
                                    print("wait",waiting_time)
                                    print("matching ratio",matched_request_num/60000) # FIXME: for now let's just use 60000
                                    print("ocu",occupancy_rate)
                                    print("ocu for normal taxi", occupancy_rate_normal)
                                    print("ocu for premium taxi", occupancy_rate_premium)
                                    print("ocu per hour",occupancy_rate_per_hour) # check ocu per hour
                                    print("ocu per hour for normal taxi",occupancy_rate_per_hour_normal)
                                    print("ocu per hour for premium taxi",occupancy_rate_per_hour_premium)
                                    print("time used", end_time - start_time)
                                    record_array = np.array(
                                        [total_reward, matched_request_num,
                                          long_request_num, matched_long_request_num,
                                         matched_medium_request_num, medium_request_num, matched_short_request_num,
                                         short_request_num, total_request_num,waiting_time,pickup_time,occupancy_rate,occupancy_rate_no_pickup])
                                    # record_array = np.array([total_reward])

                                    if num == 0:
                                        df.iloc[0, :13] = record_array
                                    else:
                                        df.iloc[num, :13] = (df.iloc[(num - 1), :13].values * num + record_array) / (
                                                    num + 1)

                                    if num % 10 == 0:  # save the result every 10
                                        pickle.dump(df, open(
                                            load_path + 'performance_record_test_' + env_params['method'] + '.pickle',
                                            'wb'))

                                    if num >= (test_interval - 1):
                                        profit_array = df.loc[(num - test_interval):num, 'total_reward'].values
                                        # print(profit_array)
                                        error = np.abs(np.max(profit_array) - np.min(profit_array))
                                        print('error: ', error)
                                        if error < threshold:
                                            index = num
                                            print('converged at index ', index)
                                            break
                                plt.plot(ax,ay)
                                plt.plot(ax,ay,'r+')
                                plt.show()

                                df.loc[:(num), 'matched_long_request_ratio'] = df.loc[:(num),
                                                                               'matched_long_request_num'].values / df.loc[
                                                                                                                    :(num),
                                                                                                                    'long_request_num'].values
                                df.loc[:(num), 'matched_medium_request_ratio'] = df.loc[:(num),
                                                                                 'matched_medium_request_num'].values / df.loc[
                                                                                                                        :(
                                                                                                                            num),
                                                                                                                        'medium_request_num'].values
                                df.loc[:(num), 'matched_short_request_ratio'] = df.loc[:(num),
                                                                                'matched_short_request_num'].values / df.loc[
                                                                                                                      :(
                                                                                                                          num),
                                                                                                                      'short_request_num'].values
                                df.loc[:(num), 'matched_request_ratio'] = df.loc[:(num),
                                                                          'matched_request_num'].values / df.loc[:(num),
                                
                                                                                                     'total_request_num'].values
                                print(df.columns) 
                                pickle.dump(df,
                                            open(load_path + 'performance_record_test_' + env_params['method'] + '.pickle',
                                                 'wb'))
                                pickle.dump(track_record, open(load_path + '/records_driver_num_'+str(850)+'.pickle', 'wb'))
                                print(df.iloc[test_num-1, :])

                                # np.savetxt(load_path + "supply_dist_" + simulator.method + ".csv", simulator.driver_spatial_dist, delimiter=",")

                            elif simulator.experiment_mode == 'train':
                                print("training process")
                                epsilons = get_exponential_epsilons(INIT_EPSILON, FINAL_EPSILON, 2500, decay=DECAY,
                                                                    pre_steps=PRE_STEP)
                                epsilons = np.concatenate([epsilons, np.zeros(NUM_EPOCH - 2500)])
                                # epsilons = np.zeros(NUM_EPOCH)
                                total_reward_record = np.zeros(NUM_EPOCH)
                                agent = None
                                if simulator.method in ['sarsa', 'sarsa_no_subway', 'sarsa_travel_time',
                                                        'sarsa_travel_time_no_subway', 'sarsa_total_travel_time',
                                                        'sarsa_total_travel_time_no_subway']:
                                    agent = SarsaAgent(**sarsa_params)
                                    if FLAG_LOAD:
                                        agent.load_parameters(
                                            load_path + 'episode_1800\\sarsa_q_value_table_epoch_1800.pickle')
                                for epoch in range(NUM_EPOCH):
                                    date = TRAIN_DATE_LIST[epoch % len(TRAIN_DATE_LIST)]
                                    simulator.experiment_date = date
                                    simulator.reset()
                                    start_time = time.time()
                                    for step in range(simulator.finish_run_step):
                                        dispatch_transitions = simulator.rl_step(agent, epsilons[epoch])
                                        if agent is not None:
                                            agent.perceive(dispatch_transitions)
                                    end_time = time.time()
                                    total_reward_record[epoch] = simulator.total_reward
                                    # pickle.dump(simulator.order_status_all_time,open("1106a-order.pkl","wb"))
                                    # pickle.dump(simulator.driver_status_all_time,open("1106a-driver.pkl","wb"))
                                    # pickle.dump(simulator.used_driver_status_all_time,open("1106a-used-driver.pkl","wb"))
                                    print('epoch:', epoch)
                                    print('epoch running time: ', end_time - start_time)
                                    print('epoch total reward: ', simulator.total_reward)
                                    print("total orders",simulator.total_request_num)
                                    print("matched orders",simulator.matched_requests_num)
                                    print("step1:order dispatching:",simulator.time_step1)
                                    print("step2:reaction",simulator.time_step2)
                                    print("step3:bootstrap new orders:",simulator.step3)
                                    print("step4:cruise:", simulator.step4)
                                    print("step4_1:track_recording",simulator.step4_1)
                                    print("step5:update state",simulator.step5)                                 
                                    print("step6:offline update",simulator.step6)
                                    print("step7: update time",simulator.step7)
                                    pickle.dump(simulator.record,open("output3/order_record-1103.pickle","wb"))
                                    # if epoch % 200 == 0:  # save the result every 200 epochs
                                    #     agent.save_parameters(epoch)

                                    if epoch % 200 == 0:  # plot and save training curve
                                        # plt.plot(list(range(epoch)), total_reward_record[:epoch])
                                        pickle.dump(total_reward_record, open(load_path + 'training_results_record', 'wb'))

                            # Move track record appending to test's iteration, saving time
                            # Also, since rl_step used to return transition data instead of record data, also modify rl_step's return value

                            # for step in tqdm(range(simulator.finish_run_step)):
                            #     new_tracks = simulator.rl_step()
                            #     track_record.append(new_tracks)

                            match_and_cancel_track_list = simulator.match_and_cancel_track
                            file_path = './output_sentivity/' + pc_flag + "_" + dl_flag + "_" + "cruise="+str(cr_flag)
                            if not os.path.exists(file_path):
                                os.makedirs(file_path)
                            pickle.dump(track_record, open(file_path + '/records_driver_num_'+str(single_driver_num)+'.pickle', 'wb'))
                            pickle.dump(simulator.requests, open(file_path + '/passenger_records_driver_num_'+str(single_driver_num)+'.pickle', 'wb'))

                            pickle.dump(match_and_cancel_track_list,open(file_path+'/match_and_cacel_'+str(single_driver_num)+'.pickle','wb'))
                            file = open(file_path + '/time_statistic.txt', 'a')
                            file.write(str(time.time()-t)+'\n')

                        elif env_params.rl_mode == "reposition":
                            len_time_binary = 9
                            len_grid_binary = 7
                            if simulator.experiment_mode == 'train':
                                epsilons = get_exponential_epsilons(INIT_EPSILON, FINAL_EPSILON, NUM_EPOCH, decay=DECAY,
                                                                    pre_steps=PRE_STEP)
                                total_reward_record = np.zeros(NUM_EPOCH)

                                # parameters
                                # here 8 is the length of binary total time steps
                                # 6 is the the length of binary total grids
                                # 37 is the length of global state vetors, equal to the numeber of grids
                                if simulator.reposition_method == 'A2C':
                                    agent_params = dict(action_dim=5, state_dim=(len_time_binary + len_grid_binary),
                                                        available_directions=df_available_directions,
                                                        load_model=False, discount_factor=DISCOUNT_FACTOR,
                                                        actor_lr=ACTOR_LR, critic_lr=CRITIC_LR,
                                                        actor_structure=ACTOR_STRUCTURE,
                                                        critic_structure=CRITIC_STRUCTURE,
                                                        model_name=simulator.reposition_method)
                                elif simulator.reposition_method == 'A2C_global_aware':
                                    agent_params = dict(action_dim=5, state_dim=(
                                                len_time_binary + len_grid_binary + 2 * side**2),
                                                        available_directions=df_available_directions,
                                                        load_model=False, discount_factor=DISCOUNT_FACTOR,
                                                        actor_lr=ACTOR_LR,
                                                        critic_lr=CRITIC_LR,
                                                        actor_structure=ACTOR_STRUCTURE,
                                                        critic_structure=CRITIC_STRUCTURE,
                                                        model_name=simulator.reposition_method)

                                repo_agent = A2C(**agent_params)
                                for epoch in range(NUM_EPOCH):
                                    start_time = time.time()
                                    date = TRAIN_DATE_LIST[epoch % len(TRAIN_DATE_LIST)]
                                    simulator.experiment_date = date
                                    simulator.reset()
                                    for step in range(simulator.finish_run_step):
                                        grid_array, time_array, idle_drivers_by_grid, waiting_orders_by_grid = simulator.step1()

                                        action_array = np.array([])
                                        if len(grid_array) > 0:
                                            # state transformation
                                            index_grid = \
                                            np.where(grid_array.reshape(grid_array.size, 1) == simulator.zone_id_array)[
                                                1]
                                            index_time = (time_array - simulator.t_initial) // simulator.delta_t
                                            binary_index_grid = s2e(index_grid, total_len=len_grid_binary)
                                            binary_index_time = s2e(index_time, total_len=len_time_binary)
                                            state_array = np.hstack([binary_index_grid, binary_index_time])
                                            if simulator.reposition_method == 'A2C_global_aware':
                                                global_idle_driver_array = np.tile(idle_drivers_by_grid,
                                                                                   [state_array.shape[0], 1])
                                                global_wait_orders_array = np.tile(waiting_orders_by_grid,
                                                                                   [state_array.shape[0], 1])
                                                state_array = np.hstack(
                                                    [state_array, global_idle_driver_array, global_wait_orders_array])

                                            # make actions
                                            action_array = np.zeros(state_array.shape[0])
                                            for i in range(len(action_array)):
                                                action = repo_agent.egreedy_actions(state_array[i], epsilons[epoch],
                                                                                    index_grid[i])
                                                action_array[i] = action

                                        simulator.step2(action_array)

                                    # collect transitions and train the model under the end of an epoch

                                    grid_array = simulator.state_grid_array_done
                                    time_array = simulator.state_time_array_done
                                    action_array = simulator.action_array_done.astype(int)
                                    next_grid_array = simulator.next_state_grid_array_done
                                    next_time_array = simulator.next_state_time_array_done
                                    reward_array = simulator.reward_array_done
                                    done_array = np.zeros(grid_array.shape)

                                    # transform the states and next states
                                    index_grid = \
                                    np.where(grid_array.reshape(grid_array.size, 1) == simulator.zone_id_array)[1]
                                    index_time = (time_array - simulator.t_initial) // simulator.delta_t
                                    binary_index_grid = s2e(index_grid, total_len=len_grid_binary)
                                    binary_index_time = s2e(index_time, total_len=len_time_binary)
                                    state_array = np.hstack([binary_index_grid, binary_index_time])

                                    index_next_grid = np.where(
                                        next_grid_array.reshape(next_grid_array.size, 1) == simulator.zone_id_array)[1]
                                    index_next_time = (next_time_array - simulator.t_initial) // simulator.delta_t
                                    binary_index_next_grid = s2e(index_next_grid, total_len=len_grid_binary)
                                    binary_index_next_time = s2e(index_next_time, total_len=len_time_binary)
                                    next_state_array = np.hstack([binary_index_next_grid, binary_index_next_time])

                                    if simulator.reposition_method == 'A2C_global_aware':
                                        index_time = np.where(
                                            time_array.reshape(time_array.size, 1) == np.array(simulator.global_time))[
                                            1]
                                        global_idle_driver_array = np.array(simulator.global_drivers_num)[index_time, :]
                                        global_wait_orders_array = np.array(simulator.global_orders_num)[index_time, :]
                                        state_array = np.hstack(
                                            [state_array, global_idle_driver_array, global_wait_orders_array])

                                        next_time_array = ((
                                                                       next_time_array - simulator.t_initial) // simulator.delta_t) * simulator.delta_t + simulator.t_initial
                                        index_next_time = np.where(
                                            next_time_array.reshape(next_time_array.size, 1) == np.array(
                                                simulator.global_time))[1]
                                        global_next_idle_driver_array = np.array(simulator.global_drivers_num)[
                                                                        index_next_time, :]
                                        global_next_wait_orders_array = np.array(simulator.global_orders_num)[
                                                                        index_next_time, :]
                                        next_state_array = np.hstack([next_state_array, global_next_idle_driver_array,
                                                                      global_next_wait_orders_array])

                                    transitions = [state_array, action_array, reward_array, next_state_array,
                                                   done_array]
                                    repo_agent.perceive(transitions)

                                    end_time = time.time()

                                    total_reward_record[epoch] = simulator.total_reward
                                    print('epoch:', epoch)
                                    print('epoch running time: ', end_time - start_time)
                                    print('epoch epsilon: ', epsilons[epoch])
                                    # print('epoch total reward: ', simulator.total_reward)
                                    print('num_transitions: ', transitions[1].shape[0])

                                    if epoch % 100 == 0:  # save the result every 100 epochs
                                        repo_agent.save_model(epoch)
                                        pickle.dump(total_reward_record, open(load_path + 'training_results_record_' +
                                                                              env_params[
                                                                                  'reposition_method'] + '.pickle',
                                                                              'wb'))

                                    if epoch == STOP_EPOCH:
                                        repo_agent.save_model(epoch)
                                        pickle.dump(total_reward_record, open(load_path + 'training_results_record_' +
                                                                              env_params[
                                                                                  'reposition_method'] + '.pickle',
                                                                              'wb'))
                                        break


                            elif simulator.experiment_mode == 'test':
                                simulator = Simulator(**env_params)
                                column_list = ['total_reward', 'matched_request_num', 'total_request_num',
                                               'matched_request_ratio']
                                test_num = 6
                                test_interval = 3
                                threshold = 10

                                df = pd.DataFrame(np.zeros([test_num, len(column_list)]), columns=column_list)
                                remaining_index_array = np.where(df['total_reward'].values == 0)[0]
                                if len(remaining_index_array > 0):
                                    last_stopping_index = remaining_index_array[0]

                                if simulator.reposition_method == 'A2C':
                                    agent_params = dict(action_dim=5, state_dim=(len_time_binary + len_grid_binary),
                                                        available_directions=simulator.GS.df_available_directions,
                                                        load_model=True, discount_factor=DISCOUNT_FACTOR,
                                                        actor_lr=ACTOR_LR,
                                                        critic_lr=CRITIC_LR,
                                                        actor_structure=ACTOR_STRUCTURE,
                                                        critic_structure=CRITIC_STRUCTURE,
                                                        model_name=simulator.reposition_method)
                                elif simulator.reposition_method == 'A2C_global_aware':
                                    agent_params = dict(action_dim=5,
                                                        state_dim=(
                                                                    len_time_binary + len_grid_binary + 2 * simulator.GS.num_grid),
                                                        available_directions=simulator.GS.df_available_directions,
                                                        load_model=True, discount_factor=DISCOUNT_FACTOR,
                                                        actor_lr=ACTOR_LR,
                                                        critic_lr=CRITIC_LR,
                                                        actor_structure=ACTOR_STRUCTURE,
                                                        critic_structure=CRITIC_STRUCTURE,
                                                        model_name=simulator.reposition_method)
                                elif simulator.reposition_method == 'random_cruise' or simulator.reposition_method == 'stay':
                                    agent_params = dict(action_dim=5,
                                                        state_dim=(
                                                                    len_time_binary + len_grid_binary + 2 * simulator.GS.num_grid),
                                                        available_directions=simulator.GS.df_available_directions,
                                                        load_model=False, discount_factor=DISCOUNT_FACTOR,
                                                        actor_lr=ACTOR_LR,
                                                        critic_lr=CRITIC_LR,
                                                        actor_structure=ACTOR_STRUCTURE,
                                                        critic_structure=CRITIC_STRUCTURE,
                                                        model_name='')
                                repo_agent = A2C(**agent_params)

                                for num in range(last_stopping_index, test_num):
                                    print('num: ', num)
                                    total_reward = 0
                                    total_request_num = 0
                                    matched_request_num = 0

                                    for date in TEST_DATE_LIST:
                                        print(date)
                                        simulator.experiment_date = date
                                        simulator.reset()
                                        for step in range(simulator.finish_run_step):
                                            # print(step)
                                            grid_array, time_array, idle_drivers_by_grid, waiting_orders_by_grid = simulator.step1()

                                            action_array = np.array([])
                                            if len(grid_array) > 0:
                                                # state transformation
                                                index_grid = np.where(
                                                    grid_array.reshape(grid_array.size, 1) == simulator.zone_id_array)[
                                                    1]
                                                index_time = (time_array - simulator.t_initial) // simulator.delta_t
                                                binary_index_grid = s2e(index_grid, total_len=len_grid_binary)
                                                binary_index_time = s2e(index_time, total_len=len_time_binary)
                                                state_array = np.hstack([binary_index_grid, binary_index_time])
                                                if simulator.reposition_method == 'A2C_global_aware':
                                                    global_idle_driver_array = np.tile(idle_drivers_by_grid,
                                                                                       [state_array.shape[0], 1])
                                                    global_wait_orders_array = np.tile(waiting_orders_by_grid,
                                                                                       [state_array.shape[0], 1])
                                                    state_array = np.hstack([state_array, global_idle_driver_array,
                                                                             global_wait_orders_array])

                                                # make actions
                                                action_array = np.zeros(state_array.shape[0])
                                                for i in range(len(action_array)):
                                                    if simulator.reposition_method == 'A2C' or simulator.reposition_method == 'A2C_global_aware':
                                                        action = repo_agent.egreedy_actions(state_array[i], -1,
                                                                                            index_grid[i])


                                                    elif simulator.reposition_method == 'random_cruise':
                                                        action = repo_agent.egreedy_actions(state_array[i], 2,
                                                                                            index_grid[i])
                                                    elif simulator.reposition_method == 'stay':
                                                        action = 0
                                                    action_array[i] = action

                                            simulator.step2(action_array)

                                        total_reward += simulator.total_reward
                                        total_request_num += simulator.total_request_num
                                        matched_request_num += simulator.matched_requests_num

                                    total_reward = total_reward / len(TEST_DATE_LIST)
                                    total_request_num = total_request_num / len(TEST_DATE_LIST)
                                    matched_request_num = matched_request_num / len(TEST_DATE_LIST)

                                    record_array = np.array([total_reward, matched_request_num, total_request_num])

                                    if num == 0:
                                        df.iloc[0, :3] = record_array
                                    else:
                                        df.iloc[num, :3] = (df.iloc[(num - 1), :3].values * num + record_array) / (
                                                    num + 1)

                                    if num % 1 == 0:  # save the result every 10
                                        pickle.dump(df, open(load_path + 'performance_record_test_' + env_params[
                                            'reposition_method'] + '.pickle', 'wb'))

                                    if num >= (test_interval - 1):
                                        profit_array = df.loc[(num - test_interval):num, 'total_reward'].values
                                        # print(profit_array)
                                        error = np.abs(np.max(profit_array) - np.min(profit_array))
                                        print('error: ', error)
                                        if error < threshold:
                                            index = num
                                            print('converged at index ', index)
                                            break

                                df.loc[:num, 'matched_request_ratio'] = df.loc[:num,
                                                                        'matched_request_num'].values / df.loc[:num,
                                                                                                        'total_request_num'].values
                                pickle.dump(df, open(load_path + 'performance_record_test_' + env_params[
                                    'reposition_method'] + '.pickle', 'wb'))
                                print(df.iloc[num, :])




