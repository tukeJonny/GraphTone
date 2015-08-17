import matplotlib.pyplot as plt
from scipy import optimize
from math import *
import pylab

sampleNum = 1000

calcRad = lambda angle: pi * angle / 180.0
a = 1
b = 1
c = 10
d = 0.005

""" test data """
x = [calcRad(r) for r in range(1, sampleNum)]

y = [a * pylab.sin(b*calcRad(r)+c) + d for r in range(1, sampleNum)]
""" test data """

def myfit(p, x):
	#print "p is " + str(p)
	#print "x is " + str(x)
	return(p[0]*pylab.sin(p[1]*x+p[2])+p[3])

def mydiff(p, x, y):
    return(y-myfit(p,x))

p0 = [1.0,1.0,1.0,1.0]
result = optimize.leastsq(mydiff, p0, args=(x,y),full_output=True)
#print "result is " + str(result)
pr = result[0]
#print "ans:::"
print "result: " + str(pr)
print "answer: [ %.7f   %.7f	 %.7f  %.7f]\n" % (a, b, c, d) 

#Plot
plt.figure(figsize=(8,5))
plt.plot(x,y,'bo', label='Exp.')
plt.plot(x,myfit(pr,x),'k-', label='fitted curb', linewidth=10, alpha=0.3)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend(loc='best',fancybox=True, shadow=True)
plt.grid(True)
plt.show()