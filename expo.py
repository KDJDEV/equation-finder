from scipy.optimize import fsolve
import numpy as np
import math
import matplotlib.pyplot as plt
import sys

points = [(1, 2), (3, 5), (4.3, 13)]
"""
Other groups of points I've tested that work:
(1, 2), (3, 5), (4.3, 13)
(1, 2), (2, 4), (3, 8)
(1, 50), (2, 30), (3, 20)
(1, 1), (4, -11), (8, -47)
"""
points = sorted(points, key=lambda x: x[0]) #sort by x value

a = 1
b = 1

def setGuess():
    global a, b
    """
    How this function's decisions affect the result are a bit mysterious. I chose all of the constants based off of initial guesses that just seemed to work well after playing around.
    """
    if (points[0][1] < points[1][1]):
        if (points[2][1] < points[1][1]): #if the last point is less than the second, not possible to make exponential function
            sys.exit('Points cannot form exponential function')
        #function increases
        if ((points[1][1] - points[0][1])/(points[1][0] - points[0][0]) > (points[2][1] - points[1][1])/(points[2][0] - points[1][0])): #at a slower and slower rate
            a = -5
            b = 0
        else: #at a faster and faster rate
            a = 5
    else:
        if (points[2][1] > points[1][1]): #if the last point is greater than the second, not possible to make exponential function
            sys.exit('Points cannot form exponential function')
        #function decreases
        if ((points[0][1] - points[1][1])/(points[1][0] - points[0][0]) > (points[1][1] - points[2][1])/(points[2][0] - points[1][0])): #at a slower and slower rate
            b = -1
            a = 0
        else: #at a faster and faster rate
            a = -5
setGuess()

def equations(x):
    # Define the system of exponential equations
    eq1 = x[0] * np.exp(x[1]*(points[0][0])) + x[2] - points[0][1]
    eq2 = x[0] * np.exp(x[1]*(points[1][0])) + x[2] - points[1][1]
    eq3 = x[0] * np.exp(x[1]*(points[2][0])) + x[2] - points[2][1]
    return [eq1, eq2, eq3]

# Initial guess
x0 = [a, b, 0]
print(x0)

# Solve the system of equations
solution = fsolve(equations, x0, xtol=1e-12, maxfev=999999)
roundedSolution = [round(num, 4) for num in solution]

print(f"Solution: {roundedSolution[0]}e^({roundedSolution[1]}x) + {roundedSolution[2]}")

def function(x):
    return solution[0] * math.e ** (solution[1] * (x)) + solution[2]
def findPointExtrema(points, index):
    max = -math.inf
    min = math.inf
    for point in points:
        if (point[index] < min):
            min = point[index]
        if (point[index] > max):
            max = point[index]
    return (min, max)
        
x = np.linspace(findPointExtrema(points, 0)[0]-1, findPointExtrema(points, 0)[1]+1, 100)  # Choose an appropriate range
y = function(x)
plt.plot(x, y)

for point in points:
    plt.plot(point[0], point[1], 'ro', label='Points')

plt.xlabel('x')
plt.ylabel('y')
plt.title(f"Plot of {roundedSolution[0]}e^({roundedSolution[1]}x) + {roundedSolution[2]}")
plt.grid(True)
plt.show()