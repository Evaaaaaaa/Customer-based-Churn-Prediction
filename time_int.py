# encoding:utf-8
import scipy.optimize as so
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from pylab import rcParams
import seaborn as sns

def loadData(address):
    clients = pd.read_csv(address)
    clients.columns = ['mem_num', 'interval_d', 'freq']
    clients['interval_d'] = pd.to_numeric(clients['interval_d'], errors='coerce')
    clients['freq'] = pd.to_numeric(clients['freq'], errors='coerce')
    return clients

def pairPlot(clients):
    c = clients
    nrow = len(c['mem_num'])
    i = 0
    k = 1
    fig = plt.figure()
    while i in range(nrow):
        n = i
        subC = pd.DataFrame({"mem_num":"","freq":"","interval_d":""},index=["0"])

        for j in range(i, nrow):
             if c.iloc[j, 0] == c.iloc[i, 0]:
                n+=1
             else:
                break
        if n>i and n-i>10:
         subC = c[i:n-1]
         plt.subplot(6, 6, k)
         # points
         # plt.scatter(subC['freq'], subC['interval_d'], s=3, c='m')
         # lines
         plt.plot(subC['freq'], subC['interval_d'],'r')
         # p = polyFit(subC)
         # p = curveFit(subC)
         p1, p2 = secFit(subC)
         plt.ylim(0,200)
         k += 1

        i = n
        if k > 36:
            break
    plt.show()


'''
一元二次拟合
没有指数好
'''
def polyFit(data):
    subC = data
    a = np.polyfit(subC['freq'], subC['interval_d'], 2)
    b = np.polyval(a, subC['freq'])
    p = plt.plot(subC['freq'], b, 'b--')
    return p

#  指数拟合
def fund(x, a, b):
         return x ** a + b

# 幂数拟合
# def func(x, a, b, c):
#    return a * np.exp(-b * x) + c

'''
选出a>1的（上升）
没办法选出一直不稳定的
'''
def curveFit(data):
      subC = data
      # plt.plot(subC['freq'], subC['interval_d'], 'b-')
      popt, pcov = so.curve_fit(fund, subC['freq'], subC['interval_d'])
      # popt数组中，三个值分别是待求参数a,b,c
      y2 = [fund(i, popt[0], popt[1]) for i in subC['freq']]
      p = plt.plot(subC['freq'], y2, 'b--')
      return p

'''
分两段一次拟合
先把全部都间隔小的去掉（两端函数a,b都小）
再把后面间隔小或下降的去掉（第二段函数a<0或a, b都小） 
'''
def secFit(data):
    subC = data
    leng = len(subC['freq'])
    cut = int(leng/2)
    subC1 = subC[0:cut+1]
    subC2 = subC[cut:leng]
    a1 = np.polyfit(subC1['freq'], subC1['interval_d'], 1)
    b1 = np.polyval(a1, subC1['freq'])
    p1 = plt.plot(subC1['freq'], b1, 'b--')

    a2 = np.polyfit(subC2['freq'], subC2['interval_d'], 1)
    b2 = np.polyval(a2, subC2['freq'])
    p2 = plt.plot(subC2['freq'], b2, 'b--')


    return p1,p2



def main():
    rcParams['figure.figsize'] = 15, 7
    sns.set_style('whitegrid')

    clients = loadData('/Users/Evangeline0519/PycharmProjects/modeling/whole_life_mem_3.csv')
    p = pairPlot(clients)


'''
另一种方式： 
购买前六次的时间间隔k1， 全部时间间隔k2
k1大于等于k2：处于生命周期的末期
'''

if __name__ == '__main__':
    main()