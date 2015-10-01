#-*- coding: utf-8 -*-
from matplotlib import*
import matplotlib.pyplot as plt

formula = lambda x: x**2

x = [r for r in range(-10, 11)]
y = [r for r in map(formula, range(-10, 11))]

plt.title("nyannpasu~")
plt.ylim(-100, 100)
plt.xlim(-10, 10)
plt.plot(x,y)
plt.savefig("output.png")

