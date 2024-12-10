import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from queue import Queue
# import time   # 模擬即時狀況

fs=500  # sample rate

# dataset 1: 10sets, 2: 5sets
dataset = "1a"
if dataset[0] == '1':
    set = 10
elif dataset[0] == '2':
    set = 5

# threshold voltage
# vert_threshold = 0.0195
hor_threshold = 0.07
# max_threshold = 0.17

def format_func(value, tick_number):
    return int(value / 500)

def position(right, left):
    if left:
        return 1
    elif right:
        return 3
    else:
        return 2
    
def word(state):
    if state == 1:
        return 'left'
    elif state == 3:
        return 'right'
    else:
        return 'mid'
        
def pos_state(state):
    right, left = False, False
    if state == 1:
        left = True
    elif state == 3:
        right = True
    return right, left

#############################################################################################
# read file
path = r"C:\Users\rhodi\Downloads\gametest"+dataset+".csv"
data=pd.read_csv(path)

hor = data.columns[0]
hor = data[hor]
v = data.columns[1]
v = data[v]
l = np.size(v)
#######################################################################################################################
windowsize = 40
t = 0
dt = 1/fs
lapse = 0.2
q_h = Queue(maxsize=windowsize)

right, left= False, False
state = 0
change_end = 0

# 模擬即時分析，一筆一筆讀資料
for i in range (l):
    t = t + dt
    cur_h = hor[i]
    if q_h.full():
        head = q_h.get()
        # 判定左右
        if ((cur_h - head) >= hor_threshold):
            if left:
                left = False
            else:
                right = True
        elif ((cur_h - head) <= -hor_threshold):
            if right:
                right = False
            else:
                left = True

        pre_state = state
        state = position(right, left)
        if (state != pre_state):
            if (t >= change_end):
                change_end = t + lapse
                s = word(state)
                print(f'At t = {t}s state = {s}')
            else:
                state = pre_state
    right, left = pos_state(state)
    q_h.put(cur_h)
    # time.sleep(dt)  # 模擬即時狀況

####################################################################################################
# plot
plt.figure(figsize=(10,10),dpi=100)
plt.subplot(2,1,1)
plt.plot(hor,linestyle='-',label='horizontal_raw') 
plt.legend()
plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(format_func))

plt.subplot(2,1,2)
plt.plot(v,linestyle='-',label='vertical_raw') 
plt.legend()
plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(format_func))

plt.tight_layout()
plt.show()
plt.close()