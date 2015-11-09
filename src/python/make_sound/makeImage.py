from matplotlib import*
import matplotlib.pyplot as plt

def makePng(exp, xPosArray, yPosArray):
    plt.title(exp)
    #plt.plot(xPosArray, yPosArray)
    plt.savefig('output.png')