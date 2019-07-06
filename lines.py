from math import sin, cos, tan, atan, radians

class Line():
    def __init__(self, **kwargs):
        x1 = kwargs["x"] if "x" in kwargs.keys() else kwargs["x1"] if "x1" in kwargs.keys() else None
        y1 = kwargs["y"] if "y" in kwargs.keys() else kwargs["y1"] if "y1" in kwargs.keys() else None
        x2 = kwargs["x2"] if "x2" in kwargs.keys() else None
        y2 = kwargs["y2"] if "y2" in kwargs.keys() else None
        m = kwargs["m"] if "m" in kwargs.keys() else kwargs["slope"] if "slope" in kwargs.keys() else None
        theta = kwargs["theta"] if "theta" in kwargs.keys() else kwargs["angle"] if "angle" in kwargs.keys() else None
        useRadians = kwargs["useRadians"] is not False if "useRadians" in kwargs.keys() else not kwargs["useDegrees"] is not False if "useDegrees" in kwargs.keys() else True

        if x1 and y1 and x2 and y2:
            dy = y1 - y2
            dx = x1 - x2
            
            if dx == 0:
                dx = 1e-10
            
            m = dy/dx
        
        elif x1 and y1 and theta:
            if useRadians:
                m = tan(theta)
            else:
                m = tan(radians(theta))

        elif x1 and y1 and m:
            pass
        else:
            ValueError("Unrecognized argument list: {0}\nValid argument sets are:\n\t\
                {1}\n\t\
                {2}\n\t\
                {3}\n\t".format(kwargs, "'{x|x1} {y|y1} x2 y2'", "'{x|x1} {y|y1} {m|slope}'", "'{x|x1} {y|y1} {theta|angle} [{useRadians|useDegrees}]'"))
        
        self.point = (x1, y1)
        self.slope = m

            

    def intersect(self, other):
        x1, y1 = self.point
        x2, y2 = other.point

        m1 = self.slope
        m2 = other.slope

        x = (y1 - y2 + m2*x2 - m1*x1)/(m2 - m1)
        y = m1 * (x - x1) + y1
        y_alt = m2 * (x - x2) + y2

        print("Slopes: {0} and {1}".format(m1, m2))
        if m1 > 1e10 and m2 < 1e10:
            y = y_alt
            y_alt = y

        if abs(y - y_alt) > 0.00001:
            print("Math Exploded: y = {0} and {1}".format(y, y_alt))
        
        return round(x, 5), round(y, 5)
    
    def angle(self, useDegrees=False):
        if not useDegrees:
            return atan(self.slope)
        else:
            return degrees(atan(self.slope))
    
    def findPointFrom(self, x, y, distance):
        dx = distance * cos(atan(self.slope))
        dy = distance * sin(atan(self.slope))

        return (x + dx), (y + dy)




if __name__ == "__main__":
    line1 = Line(x=0, y=0, m=1)
    line2 = Line(x=3, y=1, x2=3, y2=10)
    print(line1.intersect(line2))
    print(line2.intersect(line1))

