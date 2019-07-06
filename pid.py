from datetime import datetime, timedelta

class PID():
    def __init__(self, p, i, d):
        self.p = p
        self.i = i
        self.d = d
        self.e = 0
        self.integral = 0

    def start():
        self.timestamp = datetime.now()
    
    def correction(error):
        time = datetime.now()
        delta = (time - self.timestamp).total_seconds()
        self.timestamp = time

        self.integral += (delta * error)

        correction = (self.p * error) + (self.i * self.integral) + (self.d * (error - self.e)/delta)

        self.e = error

        return correction
        

