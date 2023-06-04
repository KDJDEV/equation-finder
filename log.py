from scipy.optimize import fsolve
import numpy as np
import math
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("error")

def formatZero(number): #prevents zero from showing up as -0.0, because that bugs me
    if number == 0.0:
        return 0.0
    else:
        return number

def updateGraph(p):
    p = sorted(p, key=lambda x: x[0]) #sort by x value
    guessForB = 0
        
    plt.clf()
    def functionWithRootOfB(b):
        return (np.log(p[1][0]+b)-np.log(p[0][0]+b))/(np.log(p[2][0]+b)-np.log(p[0][0]+b))-(p[1][1]-p[0][1])/(p[2][1]-p[0][1])
    
    b = None
    try:
        b = fsolve(functionWithRootOfB, guessForB)[0]
    except:
        b = None
        print(f"Unable to find function for the given points:\n ({p[0][0]}, {p[0][1]}), ({p[1][0]}, {p[1][1]}), ({p[2][0]}, {p[2][1]})")
    if b != None:
        a = (p[1][1]-p[0][1])/(np.log(p[1][0]+b)-np.log(p[0][0]+b))
        c = p[0][1]-a*np.log(p[0][0]+b)


        def function(x):
            return a*np.log(x+b)+c
        
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
        plt.title(f"Plot of approximately {str(formatZero(round(a, 4)))}ln(x + {str(formatZero(round(b, 4)))}) + {str(formatZero(round(c, 4)))}")
        plt.grid(True)
        plt.show()

updateGraph([(1, 0), (2, 0.693), (3, 1.1)])