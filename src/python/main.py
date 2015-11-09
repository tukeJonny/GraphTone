from make_sound import *
from numerical_formula import *

def main():
	exp = raw_input("Please input: ")
	beg = raw_input("from: ")
	end = raw_input("to: ")
	xPosArray, yPosArray = parseExpression.getCoordinate(exp, int(beg), int(end))
	print "x = " + str(xPosArray)
	print "y = " + str(yPosArray)
	gensound.genSound(yPosArray)

if __name__ == "__main__":
	main()