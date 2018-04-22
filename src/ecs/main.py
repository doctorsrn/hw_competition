# -*- coding: utf-8 -*-
# Author: lizhenyang_2008@163.com
# Date: 2017/8/10

import matplotlib.pyplot as plt
import numpy as np
#from sklearn import datasets, linear_model
#from sklearn.svm import SVR
import random
from LeastSquare import LeastSquare

import os
# clustering
#from sklearn.cluster import KMeans

infile = 'test.csv'
#
# preprocess data
def importData():
    print('-------reading data from file:', infile)
    xs = []
    ys = []
    with open(infile, 'r') as inf:
        lines = inf.readlines()
        print('delete header:', lines[0])
        del lines[0]
        for line in lines:
            line = line.strip().split()
            if len(line) != 2:
                print(line)
                raise EnvironmentError
            xs.append(float(line[0]))
            ys.append(int(float(line[1])))
    assert(len(xs) == len(ys))
    print('-------finished:')
    print('length of xs:', len(xs))
    print('length of ys:', len(ys))
    return np.array(xs).reshape(-1, 1), np.array(ys)

def main():
    xs, ys = importData()
    x = xs
    y = ys

    x = [1,2,3,4,5,6,7,8,9]
    y = [3,4,2,6,8,9,10,14,17]
    lqObj = LeastSquare(x,y)

    xa = x
    ya = y
    yya = lqObj.predict(xa)
    yDer = lqObj.predictYderivative(xa)

    fig, ax1 = plt.subplots()
    lns1 = ax1.plot(xa, ya, label = 'accumulation data', color='m', linestyle='', marker='.')
    lns2 = ax1.plot(xa, yya, 'c-', label = 'predict function')
    ax2 = ax1.twinx()
    lns3 = ax2.plot(xa, yDer, 'g-', label = 'derivative function')

    lns = lns1 + lns2 + lns3

    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc = 0)

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
