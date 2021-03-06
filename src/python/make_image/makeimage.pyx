#-*- coding: utf-8 -*-

from matplotlib import*
import matplotlib.pyplot as plt

def makePng(exp, xPosArray, yPosArray, linewidth=15):
    plt.title(exp)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.plot(xPosArray, yPosArray, linewidth=linewidth)
    plt.savefig('output.png', format='png', dpi=300)
    plt.clf()