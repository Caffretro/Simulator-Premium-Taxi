import pandas as pd
import numpy as np
from Broadcasting import dispatch_broadcasting
# 制定列名
columns_name = ['origin_lng', 'origin_lat', 'order_id', 'reward_units', 'origin_grid_id', 'driver_id', 'pick_up_distance']

# 使用numpy生成随机数据，这里我们使用50行和7列（与上述列名相符）
data = np.random.rand(6, 7)
dis_data = np.random.rand(2, 3)
# 创建DataFrame
df = pd.DataFrame(data, columns=columns_name)

# 为了让数据更合理，我们需要调整一些列的数据
df['origin_lng'] = df['origin_lng'] * 180 - 90  # 假设经度在-90到90之间
df['origin_lat'] = df['origin_lat'] * 180 - 90  # 假设纬度在-90到90之间
df['order_id'] = [11,52,11,52,11,52]  # 假设订单ID是六位数的整数
df['reward_units'] = (df['reward_units'] * 100).astype(int)  # 假设奖励单位是百位数的整数
df['origin_grid_id'] = (df['origin_grid_id'] * 1e6).astype(int)  # 假设原始网格ID是六位数的整数
df['driver_id'] = [335,323,465,335,323,465]  # 假设驾驶员ID是六位数的整数
df['pick_up_distance'] = df['pick_up_distance'] * 10  # 假设接驳距离在0到10之间

result = dispatch_broadcasting(order_driver_info=df,dis_array=dis_data)
print(result)