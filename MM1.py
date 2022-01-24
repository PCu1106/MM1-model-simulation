# %%
import random
from math import log, sqrt
import numpy as np
import matplotlib.pyplot as plt


def exp_rv(lam):
    U = random.uniform(0, 1)
    return -log(U)/lam


def MM1(lam, ave_ser):  # 回傳平均等待時間
    T = 100  # total time
    # ave_arr = 100  # 平均的抵達區間時間
    ts = 0  # 基準時間
    ta = [0]  # 所有人的抵達時間
    td = list()  # 所有人的離開時間
    while True:
        A = exp_rv(lam)  # 創造出exp分布的抵達區間
        ts += A  # 時間推移
        if(ts >= T):  # 超過截止時間
            break
        ta.append(ts)
    # print("所有人的抵達時間", ta)
    ts = 0  # 基準時間歸零
    # 存取所有離開時間，有幾次抵達就有幾次離開
    for i in range(len(ta)):
        S = exp_rv(1/ave_ser)  # 創造出exp分布的服務時間
        ts += S  # 時間推移
        td.append(ts)
        if i+1 < len(ta):  # 還沒結束，就要設定下一個時間基準點
            if td[i] < ta[i+1]:  # 如果我離開了，下一個人還沒來
                ts = ta[i+1]  # 下次服務時間基準點就是下一個人抵達的時間
            else:  # 如果我離開了，下一個人已經在等or剛好到
                ts = td[i]  # 下次服務時間基準點就是我離開的時間
    # print("所有人的離開時間", td)
    time_wait = 0  # 紀錄所有人等待時間總和
    for i in range(len(ta)-1):
        if td[i] > ta[i+1]:  # 我離開的時候下一人早已到達
            time_wait += td[i]-ta[i+1]  # 個人等待時間
    # print("平均等待時間為:", time_wait/len(ta), "秒")
    time_idle = 0  # 紀錄服務端閒置時間
    for i in range(1, len(ta)):
        if ta[i] > td[i-1]:  # 上一人已離開下一人未到達
            time_idle += ta[i]-td[i-1]
    # print("服務端使用率為:", (T-time_idle)/T)

    return time_wait/len(ta)


def CI_95(x_list):  # 輸入模擬多次的結果陣列，回傳信賴區間
    x_list = np.array(x_list)
    mean = np.mean(x_list)
    std = np.std(x_list)
    return mean, (1.96*std)/sqrt(len(x_list))


lam_list = np.arange(0, 1, 0.01)
color = ['blue', 'red', 'green']  # 三條線的顏色
n = [10, 50, 250]  # 分別模擬10次、50次、250次，看看信賴區間的變化

for sim_turn in range(len(n)):  # 改變模擬次數，一次做一張圖，以觀察信賴區間
    for lines in range(3):  # 要顯示三條線
        av_ser = lines*3+2  # 每條線代表的意思
        av_waiting_time = []
        ci_list = []
        for i in range(len(lam_list)):  # 移動x軸
            MM1_result = []
            for j in range(n[sim_turn]):  # 一個x值就要模擬好幾次MM1，取得95%信賴區間
                MM1_result.append(MM1(lam_list[i], av_ser))
            mean, ci = CI_95(MM1_result)
            av_waiting_time.append(mean)  # 存y軸資料
            ci_list.append(ci)  # 存當時y的信賴區間
        plt.plot(lam_list, av_waiting_time,
                 label='average service time='+str(av_ser), color=color[lines])
        av_waiting_time = np.array(av_waiting_time)
        plt.fill_between(lam_list, av_waiting_time - ci_list, av_waiting_time +
                         ci_list, color=(229/256, 204/256, 249/256), alpha=0.9)  # 畫上信賴區間
    plt.legend(loc='upper left')  # 圖例
    plt.xlabel('lambda')
    plt.ylabel('average waiting time')
    plt.title('MM1(ending time=1000)(simulation turns='+str(n[sim_turn])+')')
    plt.show()

# %%
