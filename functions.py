from scipy.optimize import root
import numpy as np
import warnings
warnings.filterwarnings("error")

from utils import *

def exp(p):
    x1, x2, x3, y1, y2, y3 = getPoints(p)
    
    negativeInFront = False
    guessForA = 1
    if (y1 > y2): #if it is decreasing
        if ((y2 - y1)/(x2 - x1) > (y3 - y2)/(x3 - x2)): #if it is decreasing faster and faster
            negativeInFront = True
        else:
            guessForA = -1
    if (y1 < y2): #if it is increasing
        if ((y2 - y1)/(x2 - x1) > (y3 - y2)/(x3 - x2)): #if it is increasing, but ever more slowly
            guessForA = -1
            negativeInFront = True
    
    def functionWithRootOfA(a):
        if (not negativeInFront):
            return (y2-y1)/(np.exp(x2*a)-np.exp(x1*a))-(y3-y1)/(np.exp(x3*a)-np.exp(x1*a))
        else:
            return (y1-y2)/(np.exp(x2*a)-np.exp(x1*a))-(y1-y3)/(np.exp(x3*a)-np.exp(x1*a))

    def findA():
        try:
            result = root(functionWithRootOfA, guessForA, method="lm")
            resultX = float(result.x)
            if (np.isnan(resultX)):
                raise Exception("failed")
            return resultX
        except:
            return None
    
    a = findA()
    if a != None:
        b = None
        c = None
        if (not negativeInFront):
            b = (1/a)*np.log((y2-y1)/(np.exp(x2*a)-np.exp(x1*a)))
            c = y1-np.exp(a*(x1+b))
        else:
            b = (1/a)*np.log((y1-y2)/(np.exp(x2*a)-np.exp(x1*a)))
            c = y1+np.exp(a*(x1+b))

        def function(x):
            #y=e^(A*(x + B)) + C
            if (not negativeInFront):
                return np.exp(a * (x + b)) + c
            else:
                return -np.exp(a * (x + b)) + c
        
        sign = "-" if negativeInFront else ""
        eq = f"y={sign}e^({longFormatNum(a)}(x + {longFormatNum(b)})) + {longFormatNum(c)}"
        roundedEq = f"y={sign}e^({formatNum(a)}(x + {formatNum(b)})) + {formatNum(c)}"

        return (function, eq, roundedEq)

    return (None, None, None)

def log(p):
    x1, x2, x3, y1, y2, y3 = getPoints(p)
    guessForB = 0
    def functionWithRootOfB(b):
        return (np.log(x2+b)-np.log(x1+b))/(np.log(x3+b)-np.log(x1+b))-(y2-y1)/(y3-y1)

    def findB():
        try:
            result = root(functionWithRootOfB, guessForB, method="lm")
            resultX = float(result.x)
            if (np.isnan(resultX)):
                raise Exception("failed")
            return resultX
        except:
            return None

    b = findB()
    if b != None:
        a = (p[1][1]-p[0][1])/(np.log(p[1][0]+b)-np.log(p[0][0]+b))
        c = p[0][1]-a*np.log(p[0][0]+b)

        def function(x):
            #y=A*ln(x+B) + C
            return a*np.log(x+b)+c
        
        eq = f"y={longFormatNum(a)}ln(x + {longFormatNum(b)}) + {longFormatNum(c)}*x" #This one rounds to 20 decimals for more precision than roundedEq
        roundedEq = f"y={formatNum(a)}ln(x + {formatNum(b)}) + {formatNum(c)}*x"

        return (function, eq, roundedEq)

    return (None, None, None)

def doozy(p):
    x1, x2, x3, y1, y2, y3 = getPoints(p)
    guessForB = 1

    def functionWithRootOfB(b):
        # D denotes denominator and N denotes numerator
        C1N = y2 * ((x1 + 1/b) * np.log(b * x1 + 1) - x1) - \
            y1 * ((x2 + 1/b) * np.log(b * x2 + 1) - x2)
        C1D = x2 * ((x1 + 1/b) * np.log(b * x1 + 1) - x1) - \
            x1 * ((x2 + 1/b) * np.log(b * x2 + 1) - x2)

        C2N = y3 * ((x1 + 1/b) * np.log(b * x1 + 1) - x1) - \
            y1 * ((x3 + 1/b) * np.log(b * x3 + 1) - x3)
        C2D = x3 * ((x1 + 1/b) * np.log(b * x1 + 1) - x1) - \
            x1 * ((x3 + 1/b) * np.log(b * x3 + 1) - x3)

        eq = C1N / C1D - C2N / C2D
        return eq

    def findB():
        try:
            result = root(functionWithRootOfB, guessForB, method="lm")
            resultX = float(result.x)
            if (np.isnan(resultX)):
                raise Exception("failed")
            return resultX
        except:
            return None

    b = findB()
    if b != None:
        termA = ((x1 + 1/b) * np.log(b * x1 + 1) - x1)
        termB = ((x3 + 1/b) * np.log(b * x3 + 1) - x3)
        cN = y3 * termA - y1 * termB
        cD = x3 * termA - x1 * termB
        c = cN / cD
        a = (y1 - c * x1) / ((x1 + 1/b) * np.log(b * x1 + 1) - x1)

        def function(x):
            # y=A*((x+1/B)*ln(B*x+1)-x)+C*x
            return a * ((x + 1/b) * np.log(b * x + 1) - x) + c * x
        
        eq = f"y={longFormatNum(a)}*((x+1/{longFormatNum(b)})*ln({longFormatNum(b)}*x+1)-x)+{longFormatNum(c)}*x" #This one rounds to 20 decimals for more precision than roundedEq
        roundedEq = f"y={formatNum(a)}*((x+1/{formatNum(b)})*ln({formatNum(b)}*x+1)-x)+{formatNum(c)}*x"

        return (function, eq, roundedEq)

    return (None, None, None)