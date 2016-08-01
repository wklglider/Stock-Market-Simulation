import pandas as pd
import math
import random
import statistics as st
import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy.fftpack as fftp
import numpy as np
from datetime import datetime, timedelta

def main():
    #Load column data from table 
    adjClose = loadTableData()
    listSize = len(adjClose)

    #Calculate Periodic Daily Return by existing periodic prices
    PeriodicDailyReturn = getPeriodicDailyReturn(adjClose, listSize)

    #Calculate Average, Variance, Standard Deviation, Drift by PeriodicDailyReturn
    Average = st.mean(PeriodicDailyReturn)
    Variance = st.variance(PeriodicDailyReturn,1)
    StandardDeviation = math.sqrt(Variance)
    Drift = Average - (Variance / 2);
    
    #Calculate FuturePrice for 200
    Days = 200
    PriceToday = adjClose[listSize-1]
    FuturePrices = []
    TradingVol = []
    Color = []
    rsi6 = [0, 0, 0, 0, 0, 0]
    rsi12 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    transaction = []
    balance = []
    profit = 0
    buy = 0
    isHolding = False
    sellGap = 0.00  #-------------------------------------------------------Modify this value between 0 and 0.2

    for i in range(Days):
        FuturePrices.append(PriceToday * math.pow(math.e, Drift + StandardDeviation * norm.ppf(random.uniform(0, 1))))
        gap = FuturePrices[i] - PriceToday
        isRise = gap > 0
        TradingVol.append(np.abs(gap))
        Color.append('g' if isRise else 'r')
        PriceToday = FuturePrices[i]
        action = 0

        #Bug In and Sell out
        if i > 5:
            increase = decrease = 0
            for j in range(6):
                diff = FuturePrices[i - j] - FuturePrices[i - j - 1]
                if diff > 0:
                    increase += diff
                else:
                    decrease -= diff
                rsi6_temp = increase / (increase + decrease)
            rsi6.append(rsi6_temp)
        if i > 11:
            increase = decrease = 0
            for j in range(12):
                diff = FuturePrices[i - j] - FuturePrices[i - j - 1]
                if diff > 0:
                    increase += diff
                else:
                    decrease -= diff
                rsi12_temp = increase / (increase + decrease)
            rsi12.append(rsi12_temp)
        if rsi6[i] < rsi12[i] and rsi12[i - 1] < rsi6[i - 1] and isHolding == False:
            buy = FuturePrices[i]
            action = 1
            isHolding = True
        if rsi6[i] > rsi12[i] and rsi12[i - 1] > rsi6[i - 1] and isHolding and np.abs(buy - FuturePrices[i]) / buy > sellGap :
            profit += FuturePrices[i] - buy
            action = -1
            isHolding = False
        transaction.append(action)
        balance.append(profit)

    #Plot Config
    minY = min(FuturePrices) * 0.98
    maxY = max(FuturePrices) * 1.02
    currentMin = FuturePrices[0]
    currentMax = FuturePrices[0]
    maxVol = max(TradingVol)

    #Plot output
    for i in range(Days):
        #Clear Plot
        plt.clf()

        #Plot Setting 

        #Price Line
        plt.subplot(4, 1, 1)
        plt.title('Stock Market Simulation', fontsize=40)
        plt.xlabel('Time Line', fontsize=20)
        plt.ylabel('NASDAQ Future Index', fontsize=20)
        plt.xlim([0,Days])
        plt.ylim([minY, maxY])
        plt.plot(FuturePrices[:i], linewidth=8, color='b')
        plt.plot([], [], 'g', label='Highest Price', linewidth=2)
        plt.plot([], [], 'b', label='Price', linewidth=8)
        plt.plot([], [], 'r', label='Lowest Price', linewidth=2)
        plt.legend()
        plt.annotate
        #Reference Lines
        currentMin = min(currentMin, FuturePrices[i])
        currentMax = max(currentMax, FuturePrices[i])
        plt.axhline(y=FuturePrices[0], linewidth=4, color='k')
        plt.axhline(y=currentMin, color='r')
        plt.axhline(y=currentMax, color='g')
        #Transaction Annotation
        for j in range(i):
            if transaction[j] > 0:
                plt.annotate(
                    'buy', 
                    xy = (j, FuturePrices[j]), xytext = (0, -40),
                    textcoords = 'offset points', ha = 'right', va = 'bottom',
                    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'c', alpha = 0.5),
                    arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
            if transaction[j] < 0:
                plt.annotate(
                    'sell', 
                    xy = (j, FuturePrices[j]), xytext = (0, 40),
                    textcoords = 'offset points', ha = 'right', va = 'bottom',
                    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'm', alpha = 0.5),
                    arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

        ##Bug and Sell
        plt.subplot(4, 1, 2)
        plt.xlabel('Time Line', fontsize=20)
        plt.ylabel('Bug & Sell', fontsize=20)
        plt.xlim([0,Days])
        plt.ylim([0, 1.1])
        plt.plot(rsi6[:i], linewidth=4, color='c')
        plt.plot(rsi12[:i], linewidth=4, color='m')
        plt.plot([], [], 'c', label='6 Days\' Relative Strength Index', linewidth=4)
        plt.plot([], [], 'm', label='12 Days\' Relative Strength Index', linewidth=4)
        plt.legend()
        #Transaction Annotation
        for j in range(i):
            if transaction[j] > 0:
                plt.annotate(
                    'buy', 
                    xy = (j, rsi6[j]), xytext = (0, -40),
                    textcoords = 'offset points', ha = 'right', va = 'bottom',
                    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'c', alpha = 0.5),
                    arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
            if transaction[j] < 0:
                plt.annotate(
                    'sell', 
                    xy = (j, rsi12[j]), xytext = (0, 40),
                    textcoords = 'offset points', ha = 'right', va = 'bottom',
                    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'm', alpha = 0.5),
                    arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

        #Trading Bar
        plt.subplot(4, 1, 3)
        plt.xlabel('Time Line', fontsize=20)
        plt.ylabel('Trading Volume', fontsize=20)
        plt.xlim([0,Days])
        plt.ylim([0, maxVol])
        plt.bar(range(i), TradingVol[:i], 0.6, color=Color[:i])
        plt.plot([], [], 'g', label='Trading Volume in Rise', linewidth=4)
        plt.plot([], [], 'r', label='Trading Volume in Down', linewidth=4)
        plt.legend()

        #Balance Line
        plt.subplot(4, 1, 4)
        plt.xlabel('Time Line', fontsize=20)
        plt.ylabel('Total Balance', fontsize=20)
        plt.xlim([0,Days])
        plt.plot(balance[:i], linewidth=6, color='g')
        plt.plot([], [], 'g', label='Balance', linewidth=6)
        plt.legend()
        #Transaction Annotation
        for j in range(i):
            if transaction[j] < 0:
                plt.annotate(
                    '$' + '{:.2f}'.format(balance[j]), 
                    xy = (j, balance[j]), xytext = (0, 40),
                    textcoords = 'offset points', ha = 'right', va = 'bottom',
                    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'w', alpha = 0.5),
                    arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

        #Draw
        plt.draw()
        plt.pause(0.0001)

    plt.show()
    print('Profit: ', profit)

def loadTableData():
    data = pd.read_csv('table.csv')
    return data['Adj Close']

def getPeriodicDailyReturn(adjClose, listSize):
    PeriodicDailyReturn = []
    for i in range(1, listSize-1):
        temp = adjClose[i] / adjClose[i-1]
        log = math.log(temp, math.e)
        PeriodicDailyReturn.append(log)
    return PeriodicDailyReturn

main()
