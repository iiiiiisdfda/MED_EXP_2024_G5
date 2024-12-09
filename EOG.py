import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from scipy import ndimage, interpolate
import matplotlib.ticker as ticker
import pywt

fs=500  # sample rate

# dataset 1: 10sets, 2: 5sets
dataset = "1l_3"
if dataset[0] == '1':
    set = 10
elif dataset[0] == '2':
    set = 5

# threshold voltage
vert_threshold = 0.0195
hor_threshold = 0.05
max_threshold = 0.17

# def highpass_filter(data, cutoff=0.01, fs=fs, order=2):
#     nyquist = 0.5 * fs
#     normal_cutoff = cutoff / nyquist
#     b, a = butter(order, normal_cutoff, btype='high', analog=False)
#     filtered_data = filtfilt(b, a, data)
#     return filtered_data
 
def lowpass_filter(data, cutoff=30, fs=fs, order=2):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

def format_func(value, tick_number):
    return int(value / 500)

#############################################################################################
# read file
path = r"C:\Users\eich\Desktop\MED_EXP_2024_G5\data"+dataset+".csv"
data=pd.read_csv(path)

hor = data.columns[0]
hor = data[hor]
v = data.columns[1]
v = data[v]

##############################################################################################
# 濾垂直方向
lp_filtered_signal = lowpass_filter(v)
# 移除pulse
pulse = ndimage.median_filter(lp_filtered_signal, 350)

##############################################################################################
# 移除baseline
# 小波包分解
wavelet = 'db1'
max_level = 10
wp = pywt.WaveletPacket(pulse, wavelet, mode='symmetric', maxlevel=max_level)

low_freq_node = wp['a' * max_level]
baseline_drift_reconstructed = low_freq_node.reconstruct(update=False)

# 插值
low_freq_length = len(pulse)
x = np.linspace(0,len(baseline_drift_reconstructed)-1, len(baseline_drift_reconstructed))
f1 = interpolate.interp1d(x, baseline_drift_reconstructed, kind='quadratic')
x_new = np.linspace(0, len(x)-1, low_freq_length)
scale = (np.mean(pulse[-500:-1]) - pulse[0])/(baseline_drift_reconstructed[-1] - baseline_drift_reconstructed[0])
baseline = f1(x_new)*scale
result = v - baseline

lp_filtered_signal = lowpass_filter(result)
vert = ndimage.median_filter(lp_filtered_signal, 220)
#######################################################################################################################
period=5

green_hor_avg=np.array([])
green_vert_avg=np.array([])
red_hor_avg=np.array([])
red_vert_avg=np.array([])
red_hor_max=np.array([])
red_vert_max=np.array([])

#休息取1.0~2.8
#移動取3.2~4.8
for i in range(set):
    hor_sum=0
    vert_sum=0
    hor_max=0
    vert_max=0
    for j in range(500+i*period*fs,1400+i*period*fs):
        hor_sum=hor_sum+hor[j]
        vert_sum=vert_sum+vert[j]
    green_hor_avg=np.append(green_hor_avg,hor_sum/900)
    green_vert_avg=np.append(green_vert_avg,vert_sum/900)
    hor_sum=0
    vert_sum=0

    for j in range(1600+i*period*fs,2400+i*period*fs):
        hor_sum=hor_sum+hor[j]
        vert_sum=vert_sum+vert[j]
    red_hor_avg=np.append(red_hor_avg,hor_sum/800)
    red_vert_avg=np.append(red_vert_avg,vert_sum/800)

    for j in range(1600+i*period*fs,2400+i*period*fs):
        if np.abs(red_hor_avg[i]-hor[j])>hor_max:
            hor_max=np.abs(red_hor_avg[i]-hor[j])
        if np.abs(red_vert_avg[i]-vert[j])>vert_max:
            vert_max=np.abs(red_vert_avg[i]-vert[j])
    red_hor_max=np.append(red_hor_max,hor_max)
    red_vert_max=np.append(red_vert_max,vert_max)
#print(green_hor_avg)
#print(green_vert_avg)
#print(red_hor_avg)
#print(red_vert_avg)
#print(red_hor_max)
#print(red_vert_max)


answer =np.array([])
golden_1a =np.array(["9", "3", "5", "9", "1", "3", "6", "9", "4", "7"])
golden_1b =np.array(["2", "5", "1", "6", "6", "7", "9", "1", "6", "9"])
golden_1c =np.array(["3", "4", "7", "8", "5", "3", "7", "4", "4", "6"])
golden_1d =np.array(["6", "4", "7", "6", "1", "3", "5", "9", "1", "2"])
golden_1e =np.array(["8", "5", "4", "9", "1", "4", "1", "6", "8", "2"])
golden_1f =np.array(["7", "3", "2", "1", "4", "9", "1", "3", "2", "8"])
golden_1g =np.array(["2", "7", "4", "2", "2", "7", "8", "9", "6", "9"])
golden_1h =np.array(["6", "6", "3", "9", "5", "7", "6", "9", "2", "4"])
golden_1i =np.array(["8", "6", "2", "1", "3", "9", "4", "7", "4", "6"])
golden_1j =np.array(["3", "8", "5", "3", "2", "6", "2", "3", "2", "9"])
golden_1k =np.array(["5", "8", "3", "6", "9", "7", "4", "6", "6", "4"])
golden_1l =np.array(["9", "2", "5", "1", "1", "5", "1", "2", "3", "7"])
golden_1m =np.array(["6", "5", "9", "6", "4", "1", "5", "9", "4", "8"])
golden_1n =np.array(["7", "8", "1", "5", "8", "2", "6", "9", "3", "2"])
golden_1o =np.array(["1", "2", "3", "4", "5", "6", "7", "8", "4", "9"])
dictionary = {'1a':golden_1a, '1b':golden_1b, '1c':golden_1c, '1d':golden_1d, '1e':golden_1e, '1f':golden_1f, \
              '1g':golden_1g, '1h':golden_1h, '1i':golden_1i, '1j':golden_1j, '1k':golden_1k, '1l':golden_1l, \
              '1m':golden_1m, '1n':golden_1n, '1o':golden_1o, '2a':golden_1a[:5], '2b':golden_1a[5:], \
              '2c':golden_1b[:5], '2d':golden_1b[5:], '2e':golden_1c[:5], '2f':golden_1c[5:],'2g':golden_1d[:5],\
              '2h':golden_1d[5:], '2i':golden_1e[:5], '2j':golden_1e[5:],}

# calaulate differences
hor_diff = np.array([])
vert_diff = np.array([])
for i in range(set):
    hor_diff = np.append(hor_diff,green_hor_avg[i]-red_hor_avg[i])
    vert_diff = np.append(vert_diff,green_vert_avg[i]-red_vert_avg[i])

# 判定方向
for i in range(set):
    if red_vert_max[i]>max_threshold:
        answer=np.append(answer,"5")
    elif green_vert_avg[i]-red_vert_avg[i]>vert_threshold and green_hor_avg[i]-red_hor_avg[i]>hor_threshold:
        answer=np.append(answer,"1")
    elif green_vert_avg[i]-red_vert_avg[i]>vert_threshold and green_hor_avg[i]-red_hor_avg[i]<hor_threshold and green_hor_avg[i]-red_hor_avg[i]>-hor_threshold:
        answer=np.append(answer,"2")
    elif green_vert_avg[i]-red_vert_avg[i]>vert_threshold and green_hor_avg[i]-red_hor_avg[i]<-hor_threshold:
        answer=np.append(answer,"3")
    elif green_vert_avg[i]-red_vert_avg[i]<vert_threshold and green_vert_avg[i]-red_vert_avg[i]>-vert_threshold and green_hor_avg[i]-red_hor_avg[i]>hor_threshold:
        answer=np.append(answer,"4")
    elif green_vert_avg[i]-red_vert_avg[i]<vert_threshold and green_vert_avg[i]-red_vert_avg[i]>-vert_threshold and green_hor_avg[i]-red_hor_avg[i]<-hor_threshold:
        answer=np.append(answer,"6")
    elif green_vert_avg[i]-red_vert_avg[i]<-vert_threshold and green_hor_avg[i]-red_hor_avg[i]>hor_threshold:
        answer=np.append(answer,"7")
    elif green_vert_avg[i]-red_vert_avg[i]<-vert_threshold and green_hor_avg[i]-red_hor_avg[i]<hor_threshold and green_hor_avg[i]-red_hor_avg[i]>-hor_threshold:
        answer=np.append(answer,"8")
    elif green_vert_avg[i]-red_vert_avg[i]<-vert_threshold and green_hor_avg[i]-red_hor_avg[i]<-hor_threshold:
        answer=np.append(answer,"9")
    else:
        answer=np.append(answer,"0")
print("answer=",answer)
ans = dataset[:2]
print("golden=",dictionary[ans])
print("hor_diff=",hor_diff)
print("vert_diff=",vert_diff)

####################################################################################################
# plot
plt.figure(figsize=(10,10),dpi=100)
plt.subplot(3,1,1)
plt.plot(vert,linestyle='-',label='vertical_filt') 
plt.legend()
plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(format_func))

plt.subplot(3,1,2)
plt.plot(v,linestyle='-',label='vertical_raw')
plt.legend()
# 獲取當前 x 軸刻度並設置新的標籤
plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(format_func))

plt.subplot(3,1,3)
plt.plot(baseline,linestyle='-',label='vertical_filt') 
plt.legend()
plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(format_func))

plt.tight_layout()
plt.show()
plt.close()