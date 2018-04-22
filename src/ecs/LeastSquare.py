# -*- coding: utf-8 -*-
#import numpy as np
import LinearSolver
class LeastSquare:
    xs = []
    ys = []
    solver = []
    order = 20
    def __init__(self, x, y, defaultOrder = 9):
        self.xs = x
        self.ys = y
        self.order = defaultOrder
        self.solve()
    def predict(self, x):
        order = self.order
        solver = self.solver

        y = []
        for i in range(0, len(x)):
            yline = 0.0
            for j in range(0, order + 1):
                powerx = 1.0
                for k in range(0, j):
                    powerx *= x[i]
                powerx *= solver[j]
                yline += powerx
            y.append(yline)
        return y
    def predictYderivative(self, x):
        order = self.order
        solver = self.solver
        yDer = []
        for i in range(0, len(x)):
            yline = 0.0
            for j in range(1, order + 1):
                powerx = 1.0
                for k in range(0, j - 1):
                    powerx *= x[i]
                powerx *= j
                yline += powerx * solver[j]
            yDer.append(yline)
        return yDer



    def solve(self):
        order = self.order
        xa = self.xs
        ya = self.ys
        matA = []

        # 行列式只有 n + 1 个，行数是系数的个数，不是样本的个数。
        for i in range(0, order + 1): # 计算每一行的行向量
            matAline = []
            for j in range(0, order + 1): # 计算每一个行向量中的元素的值
                sumX = 0.0
                for k in range(0, len(xa)): # 计算每一个样本的幂数
                    # i + j
                    dx = 1
                    for m in range(0, i + j): # 计算幂数
                        dx *= xa[k]
                    sumX += dx
                matAline.append(sumX)
            matA.append(matAline)

        matB = []
        for i in range(0, order + 1):
            dydx = 0.0
            for j in range(0, len(xa)):
                dy = ya[j]
                dx = 1.0
                for k in range(0, i):
                    dx *= xa[j]
                dydx += dy * dx
            matB.append(dydx)
        
#        print matB
#        matB = np.array(matB)
#        print matB
#        self.solver = np.linalg.solve(matA, matB)
        #使用第三方函数求解线性方程组，替代numpy中的函数
#        print matA,matB
#        self.solver = LinearSolver.gauss(matA, matB)
#        self.solver = LinearSolver.jacobi(matA, matB)
        self.solver = LinearSolver.sor(matA, matB)
