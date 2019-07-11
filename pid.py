from datetime import datetime, timedelta

class PID():
    def __init__(self, p, i, d):
        
        # p,i,d is constant
        self.p = p
        self.i = i
        self.d = d
        self.err = 0
        self.integral = 0 # integral(e) is rolling sum of e * dt

    def start():
        self.timestamp = datetime.now()
    
    def correction(error):
        time = datetime.now()
        delta = (time - self.timestamp).total_seconds()
        self.timestamp = time

        self.integral += (delta * error)

        # correction = Kp * e(t)        + Ki * integral(e)      + Kd * de/dt
        correction = (self.p * error) + (self.i * self.integral) + (self.d * (error - self.e)/delta)

        self.err = error

        return correction
        

