from make_sound import *
from make_image import *
from numerical_formula import *
from matplotlib import*
import matplotlib.pyplot as plt

def main():
	exp = raw_input("Please input: ")
	beg = raw_input("from: ")
	end = raw_input("to: ")
	xPosArray, yPosArray = parseExpression.getCoordinate(exp, int(beg), int(end))
	print "x = " + str(xPosArray)
	print "y = " + str(yPosArray)
	gensound.genSound(yPosArray)
	makeimage.makePng(exp, xPosArray, yPosArray)

if __name__ == "__main__":
	main()