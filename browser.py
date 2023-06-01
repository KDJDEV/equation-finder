from scipy.optimize import fsolve
import numpy as np
import math
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("error")
from pyodide.ffi import create_proxy
from js import document

def formatZero(number): #prevents zero from showing up as -0.0, because that bugs me
    if number == 0.0:
        return 0.0
    else:
        return number

def updateGraph(p):
    p = sorted(p, key=lambda x: x[0]) #sort by x value
    derivativeDecreasing = False
    if (p[0][1] > p[1][1]):
        derivativeDecreasing = True
        if ((p[0][1] - p[1][1])/(p[1][0] - p[0][0]) > (p[1][1] - p[2][1])/(p[2][0] - p[1][0])):
            derivativeDecreasing = True
            
    plt.clf()
    def functionWithRootOfA(a):
        if (not derivativeDecreasing):
            return (p[1][1]-p[0][1])/(np.exp(p[1][0]*a)-np.exp(p[0][0]*a))-(p[2][1]-p[0][1])/(np.exp(p[2][0]*a)-np.exp(p[0][0]*a))
        else:
            return (p[0][1]-p[1][1])/(np.exp(p[1][0]*a)-np.exp(p[0][0]*a))-(p[0][1]-p[2][1])/(np.exp(p[2][0]*a)-np.exp(p[0][0]*a))
       
    a = None
    try:
        a = fsolve(functionWithRootOfA, 1)[0]
    except:
        a = None
        print(f"Unable to find function for the given points:\n ({p[0][0]}, {p[0][1]}), ({p[1][0]}, {p[1][1]}), ({p[2][0]}, {p[2][1]})")
    if a != None:
        b = None
        c = None
        if (not derivativeDecreasing):
            b = (1/a)*np.log((p[1][1]-p[0][1])/(np.exp(p[1][0]*a)-np.exp(p[0][0]*a)))
            c = p[0][1]-np.exp(a*(p[0][0]+b))
        else:
            b = (1/a)*np.log((p[0][1]-p[1][1])/(np.exp(p[1][0]*a)-np.exp(p[0][0]*a)))
            c = p[0][1]+np.exp(a*(p[0][0]+b))

        def function(x):
            if (not derivativeDecreasing):
                return math.e ** (a * (x + b)) + c
            else:
                return -math.e ** (a * (x + b)) + c
        
        def findPointExtrema(points, index):
            max = -math.inf
            min = math.inf
            for point in points:
                if (point[index] < min):
                    min = point[index]
                if (point[index] > max):
                    max = point[index]
            return (min, max)

        x = np.linspace(findPointExtrema(p, 0)[0]-1, findPointExtrema(p, 0)[1]+1, 100)
        y = function(x)
        plt.plot(x, y)

        for point in p:
            plt.plot(point[0], point[1], 'ro', label='Points')

        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f"Plot of approximately e^({str(formatZero(round(a, 4)))}(x + {str(formatZero(round(b, 4)))})) + {str(formatZero(round(c, 4)))}")
        plt.grid(True)
        Element("plot").write(plt)

def inputChanged(e):
    p = [(float(document.getElementById("point1x").innerHTML), float(document.getElementById("point1y").innerHTML)), (float(document.getElementById("point2x").innerHTML), float(document.getElementById("point2y").innerHTML)), (float(document.getElementById("point3x").innerHTML), float(document.getElementById("point3y").innerHTML))]
    updateGraph(p)
inputChanged(None)

Element("point1x").element.addEventListener("input", create_proxy(inputChanged))
Element("point1y").element.addEventListener("input", create_proxy(inputChanged))
Element("point2x").element.addEventListener("input", create_proxy(inputChanged))
Element("point2y").element.addEventListener("input", create_proxy(inputChanged))
Element("point3x").element.addEventListener("input", create_proxy(inputChanged))
Element("point3y").element.addEventListener("input", create_proxy(inputChanged))