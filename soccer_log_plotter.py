#!/usr/bin/python

import matplotlib.pyplot as plt

log = open("soccer.log", 'r')
fig = plt.figure()
sub = fig.add_subplot(1, 1, 1)
x = []
y = []

labels = ["scan 1, scan 2, ball, goal, kick"]
colors = ["black", "grey", "blue", "yellow", "green", "red"]

for entry in log.readlines():
    a, b = entry.split()
    x.append(float(a))
    y.append(float(b))

plt.scatter(x, y, color=colors)
log.close()
plt.show()
