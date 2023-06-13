from js import document, functionType
from pyodide.ffi import create_proxy
import numpy as np
import math
import matplotlib.pyplot as plt

from functions import exp, log, doozy
from utils import getPoints

loadingText = document.getElementById("loadingText")
loadingText.style.display = "none"

def clear():
    Element("output").clear()
    plt.clf()

def updateGraph(p):
    p = sorted(p, key=lambda x: x[0])  # sort by x value

    clear()

    function, eq, roundedEq = (exp(p) if (functionType == "exp") else log(p) if (functionType == "log") else doozy(p))
    if (function == None):
        x1, x2, x3, y1, y2, y3 = getPoints(p)
        Element("output").write(f"Unable to find function for the given points: ({x1}, {y1}), ({x2}, {y2}), ({x3}, {y3})\n")
        return
    
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

    
    titleText = f"Plot of approximately {roundedEq}"
    plt.title(titleText, fontsize=12)
    plt.grid(True)
    Element("plot").write(plt)
    Element("output").write(f"Found function for the given points: ({p[0][0]}, {p[0][1]}), ({p[1][0]}, {p[1][1]}), ({p[2][0]}, {p[2][1]}) \nHere it is with lots of decimals for more precision: \n{eq}\n")


def inputChanged(e):
    try:
        p = [(float(document.getElementById("point1x").innerText.replace("<br>", "").replace("\n", "")), float(document.getElementById("point1y").innerText.replace("<br>", "").replace("\n", ""))), (float(document.getElementById("point2x").innerText.replace("<br>", "").replace("\n", "")), float(document.getElementById("point2y").innerText.replace("<br>", "").replace("\n", ""))), (float(document.getElementById("point3x").innerText.replace("<br>", "").replace("\n", "")), float(document.getElementById("point3y").innerText.replace("<br>", "").replace("\n", "")))]
        updateGraph(p)
    except:
        clear()
        Element("output").write("Input error, please make sure you are only inputting numbers")

Element("findButton").element.addEventListener(
    "click", create_proxy(inputChanged))