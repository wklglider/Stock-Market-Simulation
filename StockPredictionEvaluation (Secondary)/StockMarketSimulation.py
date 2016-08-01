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
    
    #Run multiple times for evaluation
    Times = 100 #-------------------------------------------------------Modify this value between 100 and 1000
    Records = []
    Color = []
    earnTimes = 0
    lostTimes = 0
    tieTimes = 0
    earnBalance = 0
    lostBalance = 0

    for i in range(Times):
        #Calculate FuturePrice for 200
        Days = 200
        PriceToday = adjClose[listSize-1]
        FuturePrices = []
        rsi6 = [0, 0, 0, 0, 0, 0]
        rsi12 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        profit = 0
        buy = 0
        isHolding = False
        transactionTimes = 0
        sellGap = 0.09  #-------------------------------------------------------Modify this value between 0 and 0.2

        for k in range(Days):
            FuturePrices.append(PriceToday * math.pow(math.e, Drift + StandardDeviation * norm.ppf(random.uniform(0, 1))))
            PriceToday = FuturePrices[k]

            #Bug In and Sell out
            if k > 5:
                increase = decrease = 0
                for j in range(6):
                    diff = FuturePrices[k - j] - FuturePrices[k - j - 1]
                    if diff > 0:
                        increase += diff
                    else:
                        decrease -= diff
                    rsi6_temp = increase / (increase + decrease)
                rsi6.append(rsi6_temp)
            if k > 11:
                increase = decrease = 0
                for j in range(12):
                    diff = FuturePrices[k - j] - FuturePrices[k - j - 1]
                    if diff > 0:
                        increase += diff
                    else:
                        decrease -= diff
                    rsi12_temp = increase / (increase + decrease)
                rsi12.append(rsi12_temp)
            if rsi6[k] < rsi12[k] and rsi12[k - 1] < rsi6[k - 1] and isHolding == False:
                buy = FuturePrices[k]
                isHolding = True
            if rsi6[k] > rsi12[k] and rsi12[k - 1] > rsi6[k - 1] and isHolding and np.abs(buy - FuturePrices[k]) / buy > sellGap :
                profit += FuturePrices[k] - buy
                isHolding = False
                transactionTimes += 1
        
        #Collect balance to Records
        Records.append(profit)
        statusStr = 'None'
        if profit > 0:
            earnTimes += 1
            earnBalance += profit
            statusStr = 'Earn'
            Color.append('g')
        elif profit < 0:
            lostTimes += 1
            lostBalance += np.abs(profit)
            statusStr = 'Lost'
            Color.append('r')
        else:
            tieTimes += 1
            statusStr = 'Tie'
            Color.append('y')
        print('Evaluate time ' + str(i + 1) + ' : ' + statusStr + ' $', '{:.2f}'.format(profit))
        print('  Transaction times: ', transactionTimes)
        print('Earning Times Percentange: {:.2f}%'.format(earnTimes/(earnTimes + lostTimes + tieTimes)*100) 
              + '      Earning Total Balance Percentange: {:.2f}%'.format(earnBalance/(earnBalance + lostBalance)*100 if (earnBalance + lostBalance) != 0 else 0) + '\n')

    print('\n\n')
    print('Earning Times: ', earnTimes)
    print('Lossing Times: ', lostTimes)
    print('Earning Times Percentange: ', '{:.2f}%'.format(earnTimes/Times*100))

    print('Earning Total Balance: ', '{:.2f}'.format(earnBalance))
    print('Lossing Total Balance: ', '{:.2f}'.format(lostBalance))
    print('Earning Total Balance Percentange: ', '{:.2f}%'.format(earnBalance/(earnBalance + lostBalance)*100 if (earnBalance + lostBalance) != 0 else 0))

    #Plot Config
    minY = min(Records) * 0.98
    maxY = max(Records) * 1.02
    currentMin = Records[0]
    currentMax = Records[0]

    #Plot output

    #Record Bar
    plt.subplot(2, 1, 1)
    plt.title('Stock Prediction Evaluation', fontsize=40)
    plt.xlabel('Records', fontsize=20)
    plt.xlim([0,Times])
    plt.ylim([minY, maxY])
    plt.bar(range(Times), Records, 0.6, color=Color)
    plt.plot([], [], 'g', label='Earn', linewidth=4)
    plt.plot([], [], 'r', label='Lost', linewidth=4)
    plt.legend()
    #Annotation
    for j in range(Times):
        floatTextDistance = 40 if Records[j] > 0 else -40
        plt.annotate(
            '$' + '{:.2f}'.format(Records[j]), 
            xy = (j, Records[j]), xytext = (0, floatTextDistance),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = Color[j], alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

    #Times Pie Chart
    plt.subplot(2, 2, 3)
    plt.rcParams['font.size'] = 20.0
    plt.title('Times', fontsize=40)
    labels = 'Earn', 'Lost', 'Tie'
    sizes = [earnTimes, lostTimes, tieTimes]
    colors = ['g', 'r', 'y']
    explode = (0, 0.1, 0.0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)

    #Balance Pie Chart
    plt.subplot(2, 2, 4)
    plt.rcParams['font.size'] = 20.0
    plt.title('Total Balance', fontsize=40)
    labels = 'Earn', 'Lost'
    sizes = [earnBalance, lostBalance]
    colors = ['g', 'r']
    explode = (0, 0.1)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)

    #Show
    plt.show()

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
