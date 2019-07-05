from math import tan

class LineStats():
    __init__(self, x0, y0, theta):
        self.slope = tan(theta)
        self.point = (x0, y0)

    intersect(self, other):
        x1, y1 = self.point
        x2, y2 = other.point

        m1 = self.slope
        m2 = other.slope

        x = (y1 - y2 + m2*x2 - m1*x1)/(m2 - m1)
        y = m1 * (x - x1) + y1
        y_alt = m2 * (x - x2) + y2

        if abs(y - y_alt) > 0.00001:
            print("Math Exploded: y = {0} and {1}")



if __name__ == "__main__":
    line1 = LineStats(0, 0, 45)
