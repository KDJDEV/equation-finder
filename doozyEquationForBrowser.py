from js import document
from pyodide.ffi import create_proxy
from scipy.optimize import fsolve
import numpy as np
import math
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("error")


def formatZero(number):  # prevents zero from showing up as -0.0, because that bugs me
    if number == 0.0:
        return 0.0
    else:
        return number

def updateGraph(p):
    p = sorted(p, key=lambda x: x[0])  # sort by x value
    guessForB = 1

    x1 = p[0][0]
    x2 = p[1][0]
    x3 = p[2][0]
    y1 = p[0][1]
    y2 = p[1][1]
    y3 = p[2][1]

    plt.clf()

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

    b = None
    try:
        b = fsolve(functionWithRootOfB, guessForB)[0]
    except:
        b = None
        print(
            f"Unable to find function for the given points:\n ({p[0][0]}, {p[0][1]}), ({p[1][0]}, {p[1][1]}), ({p[2][0]}, {p[2][1]})")
        
        """
        plot functionWithRootOfB
        x = np.linspace(-100, 1000000000000000000000, num=10000000)
        y = functionWithRootOfB(x)
        plt.plot(x, y)

        plt.xlabel('x')
        plt.ylabel('y')

        plt.grid(True)
        Element("plot").write(plt)
        """
        

    if b != None:
        a = None
        c = None

        termA = ((x1 + 1/b) * np.log(b * x1 + 1) - x1)
        termB = ((x3 + 1/b) * np.log(b * x3 + 1) - x3)
        cN = y3 * termA - y1 * termB
        cD = x3 * termA - x1 * termB
        c = cN / cD
        a = (y1 - c * x1) / ((x1 + 1/b) * np.log(b * x1 + 1) - x1)

        def function(x):
            # y=A*((x+1/B)*ln(B*x+1)-x)+C*x
            return a * ((x + 1/b) * np.log(b * x + 1) - x) + c * x

        def findPointExtrema(points, index):
            max = -math.inf
            min = math.inf
            for point in points:
                if (point[index] < min):
                    min = point[index]
                if (point[index] > max):
                    max = point[index]
            return (min, max)

        x = np.linspace(findPointExtrema(
            p, 0)[0]-1, findPointExtrema(p, 0)[1]+1, 100)
        y = function(x)
        plt.plot(x, y)

        for point in p:
            plt.plot(point[0], point[1], 'ro', label='Points')

        plt.xlabel('x')
        plt.ylabel('y')

        def formatNum(num):
            return str(formatZero(round(num, 4)))
        plt.title(
            f"Plot of approximately y={formatNum(a)}*((x+1/{formatNum(b)})*ln({formatNum(b)}*x+1)-x){formatNum(c)}*x")
        plt.grid(True)
        Element("plot").write(plt)


def inputChanged(e):
    p = [(float(document.getElementById("point1x").innerHTML), float(document.getElementById("point1y").innerHTML)), (float(document.getElementById("point2x").innerHTML), float(document.getElementById("point2y").innerHTML)), (float(document.getElementById("point3x").innerHTML), float(document.getElementById("point3y").innerHTML))]
    updateGraph(p)


inputChanged(None)

Element("point1x").element.addEventListener(
    "input", create_proxy(inputChanged))
Element("point1y").element.addEventListener(
    "input", create_proxy(inputChanged))
Element("point2x").element.addEventListener(
    "input", create_proxy(inputChanged))
Element("point2y").element.addEventListener(
    "input", create_proxy(inputChanged))
Element("point3x").element.addEventListener(
    "input", create_proxy(inputChanged))
Element("point3y").element.addEventListener(
    "input", create_proxy(inputChanged))
