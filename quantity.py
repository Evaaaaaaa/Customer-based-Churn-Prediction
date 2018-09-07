# encoding:utf-8

import scipy.optimize as so
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pylab import rcParams


def load_data(address):
    clients = pd.read_csv(address)
    clients.columns = ['mem_num', 'freq', 'quantity']
    clients['quantity'] = pd.to_numeric(clients['quantity'], errors='coerce')
    clients['freq'] = pd.to_numeric(clients['freq'], errors='coerce')

    # i = 0
    # while i in range(nrow):
    #     n = i
    #     for j in range(i, nrow):
    #         if clients.iloc[i, 0] == clients.iloc[j, 0]:
    #             clients.iloc[j, 1] = n - i + 1
    #             n += 1
    #         else:
    #             break
    #     if n-i < 2:
    #         clients = clients.drop(clients.index[i], inplace=True)

    return clients


def screen_min(c, min):
    nrow = len(c['mem_num'])
    i = 0
    k = 0
    # fig1 = plt.figure()
    m = pd.DataFrame({"mem_num": "", "freq": "", "quantity": ""}, index=["0"])
    while i in range(nrow):
        n = i
        subc = pd.DataFrame({"mem_num": "", "freq": "", "quantity": ""}, index=["0"])
        for j in range(i, nrow):
            if c.iloc[j, 0] == c.iloc[i, 0]:
                n += 1
            else:
                break

        if n - i > 1:
            subc = c[i:n - 1]
            if subc['quantity'].max() < min:
                m = m.append(subc)
                # plt.subplot(5, 5, k+1)
                # points
                # plt.scatter(subc['freq'], subc['quantity'], s=5, c='b')
                # lines
                # plt.plot(subc['freq'], subc['quantity'], 'b')
                k += 1
        i = n

    prcnt = float(k) / float(2981)
    return m, prcnt


def screen_max(c, max):
    nrow = len(c['mem_num'])
    i = 0
    k = 0
    # fig2 = plt.figure()
    m = pd.DataFrame({"mem_num": "", "freq": "", "quantity": ""}, index=["0"])
    while i in range(nrow):
        n = i
        subc = pd.DataFrame({"mem_num": "", "freq": "", "quantity": ""}, index=["0"])
        for j in range(i, nrow):
            if c.iloc[j, 0] == c.iloc[i, 0]:
                n += 1
            else:
                break

        if n - i > 1:
            subc = c[i:n - 1]
            for j in range(len(subc['quantity'])):
                if subc.iloc[j, 2] > max:
                    # list.append(subc.iloc[0, 0])
                    m = m.append(subc)
                    # plt.subplot(5, 5, k + 1)
                    # points
                    # plt.scatter(subc['freq'], subc['quantity'], s=5, c='b')
                    # lines
                    # plt.plot(subc['freq'], subc['quantity'], 'b')
                    k += 1
                    break
        i = n

    prcnt = float(k) / float(2981)
    return m, prcnt


def screen_freq(c, freq):
    nrow = len(c['mem_num'])
    i = 0
    k = 0
    frqnt = pd.DataFrame({"mem_num": "", "freq": "", "quantity": ""}, index=["0"])
    v = pd.DataFrame({"mem_num": "", "freq": "", "quantity": ""}, index=["0"])
    fluc_m = pd.DataFrame({"mem_num": "", "freq": "", "quantity": ""}, index=["0"])
    fluc_s = pd.DataFrame({"mem_num": "", "freq": "", "quantity": ""}, index=["0"])

    while i in range(nrow):
        n = i
        subc = pd.DataFrame({"mem_num": "", "freq": "", "quantity": ""}, index=["0"])
        for j in range(i, nrow):
            if c.iloc[j, 0] == c.iloc[i, 0]:
                c.iloc[j, 1] = n - i + 1
                n += 1
            else:
                break

        if n - i > freq:
            subc = c[i:n - 1]
            frqnt = frqnt.append(subc)  # frequent set
            vv = subc['quantity'].var()

            if vv > 10:
                v = v.append(subc)  # frequent and fluctuated set 一共23个
                # points
                plt.scatter(subc['freq'], subc['quantity'], s=5, c='b')
                # lines
                plt.plot(subc['freq'], subc['quantity'], 'b')
                # coff = poly_fit(subc)
                #
                # if coff[0] ** 2 >= 0.5:
                #  # 开口大，平缓 8个
                #  fluc_s = fluc_s.append(subc)
                # else:
                # # 开口小，陡峭 15个
                #  fluc_m = fluc_m.append(subc)
                a1,a2 = secFit(subc)





                plt.ylim(0, 30)
                plt.subplot(5, 5, k + 1)
                k += 1
                # if k > 24:
                #     break
        i = n

    prcnt = float(k) / float(2981)
    return v, prcnt, k


'''
一元二次拟合
没有指数好
'''


def poly_fit(d):
    a = np.polyfit(d['freq'], d['quantity'], 1)
    b = np.polyval(a, d['freq'])
    plt.plot(d['freq'], b, 'r--')
    return a


def fund(x, a, b):
    return x ** a + b

def curveFit(data):
    subC = data
    # plt.plot(subC['freq'], subC['interval_d'], 'b-')
    popt, pcov = so.curve_fit(fund, subC['freq'], subC['quantity'])
    # popt数组中，三个值分别是待求参数a,b,c
    y2 = [fund(i, popt[0], popt[1]) for i in subC['freq']]
    plt.plot(subC['freq'], y2, 'r--')
    print y2
    return y2

def secFit(data):
    subC = data
    leng = len(subC['freq'])
    cut = int(leng/2)
    subC1 = subC[0:cut+1]
    subC2 = subC[cut:leng]
    a1 = np.polyfit(subC['freq'], subC['quantity'], 1)
    b1 = np.polyval(a1, subC['freq'])
    p1 = plt.plot(subC['freq'], b1, 'r--')

    a2 = np.polyfit(subC2['freq'], subC2['quantity'], 1)
    b2 = np.polyval(a2, subC2['freq'])
    p2 = plt.plot(subC2['freq'], b2, 'r--')

    return a1,a2


def main():
    rcParams['figure.figsize'] = 15, 7
    sns.set_style('whitegrid')

    clients = load_data('/Users/Evangeline0519/PycharmProjects/modeling/buy_num.csv')

    # 数量没有超过min的用户
    # min_set, min_prcnt = screen_min(clients, 5)
    # print min_set
    # print "min_prcnt  ", min_prcnt

    # 数量超过max的用户
    # 要不要把只买了一次但一次买很多的算进去
    # max_set, max_prcnt = screen_max(clients, 5)
    # print max_set
    # print "max_prcnt  ", max_prcnt

    # 次数超过max且波动大的用户
    freq_set, freq_prcnt, k = screen_freq(clients, 5)
    print ("freq_prcnt ", k, freq_prcnt)

    plt.show()


if __name__ == '__main__':
    main()

'''
分类：
先用方差把波动大的筛选出来
再用二次函数区分平缓或陡峭
陡峭：区分峰值在前期或后期
平缓：如果截距大，说明在较高值波动（在促销日购买，对价格敏感）
     如果截距小，说明在较低值波动
     
or 
先用方差把波动大的筛选出来
整段函数k1，b1，后半段k2，b2
如果k1小 b1小 说明购买数量少
如果b1大 说明购买数量波动大
如果k2大 说明后期购买数量多
'''
