def getPoints(p):
    x1 = p[0][0]
    x2 = p[1][0]
    x3 = p[2][0]
    y1 = p[0][1]
    y2 = p[1][1]
    y3 = p[2][1]

    return (x1, x2, x3, y1, y2, y3)

def formatZero(number):  # prevents zero from showing up as -0.0, because that bugs me
    if number == 0.0:
        return 0.0
    else:
        return number

def formatNum(num):
        return str(formatZero(round(num, 4)))

def longFormatNum(num): #This one rounds to 20 decimals for more precision than roundedEq
    return "{:.20f}".format(formatZero(num))