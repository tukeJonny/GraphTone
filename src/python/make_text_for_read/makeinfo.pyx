#-*- coding: utf-8 -*-
#音声読み上げさせる情報群
#軸 (保留)

#未達成課題
#極値を持つかどうかの判定
#関数の分類

from sympy import*
import re
import sys
sys.path.append('../numerical_formula')
from parseExpression import*
import matplotlib.pyplot  as plt


class SAYINFO():
	def __init__(self, expression, xPosArray, yPosArray):
		#式定義
		self.exp = sympify(expression)
		self.x = Symbol('x')
		#微分
		self.df = diff(self.exp, self.x)
		#x軸との交点
		self.intersect = solve(Eq(self.df, 0))
		print "intersect has calculated now: " + str(self.intersect)

		self.quad = self.calcQuadrant(xPosArray, yPosArray)
		self.updown = self.calcUpDown(yPosArray[0], yPosArray[1])
		self.intercept = self.calcIntercept(expression)
		self.extremum = self.calcExtremum(expression)
		self.function = self.classifyFunction(expression)

	#何象限に属すか
	def calcQuadrant(self, xPosArray, yPosArray):
		quadrant = [False, False, False, False]
		for r in range(len(xPosArray)):
			x = xPosArray[r]
			y = yPosArray[r]
			if x > 0 and y > 0:
				quadrant[0] = True
			elif x < 0 and y > 0:
				quadrant[1] = True
			elif x < 0 and y < 0:
				quadrant[2] = True
			elif x > 0 and y < 0:
				quadrant[3] = True
		return quadrant

	#増減
	#1  ... 増加
	#-1 ... 減少
	def calcUpDown(self, y1, y2):
		Dir = []
		diffy = y2-y1
		#最初、増えているか、減っているか
		Dir.append(-1 if diffy < 0 else 1)
		#極値を持たないなら、増減の変化が起き得ない
		#また、導関数=0の解が得られないなら増減が起きないことがわかる
		if self.hasExtremum() and self.intersect is not False:
			#expressionを微分した式のx軸との交点で
			for r in range(1, len(self.intersect)+1):
				Dir.append(Dir[0]*((-1)**r))
		return Dir

	#x, y切片
	def calcIntercept(self, express):
		expression = sympify(express)
		#x切片
		xI = solve(Eq(expression, 0))
		#eval(exp.replace('x', 0))
		#y切片
		yI = expression.subs([(self.x, 0)])
		return (xI, yI)

	#極値判定
	#２階導関数f''(x)に対し、f'(a) = 0となるようなaについて
	#f''(a)を求めた時、
	#負である場合は極大値を持ち
	#正である場合は極小値を持つ
	# => f''(a) = 0となってしまった場合、極値を持たないこととなる
	def hasExtremum(self):
		#微分した式 = 0が解けない場合、極値を持たない
		if not self.intersect:
			return False
		#２階導関数を求める
		ddf = diff(self.df, self.x)
		for r in self.intersect:
			#２階導関数に導関数のx軸との交点のx座標値を代入し、その値が0にならないか調べる
			if ddf.subs([(self.x, r)]) == 0:
				return False #0であれば、極値を持たない
		return True

	#極値
	def calcExtremum(self, express):
		express = sympify(express)
		if self.hasExtremum() and self.intersect is not False:
			extremum = [express.subs([(self.x, r)]) for r in self.intersect]
			#eval(exp.replace('x', r))
			return extremum
		else:
			return [] #極値は無い

	#関数分類
	def classifyFunction(self, express):
		express = str(sympify(express))
		ThreeFunc = re.compile(r'x\*\*3')
		TwoFunc = re.compile(r'x\*\*2')
		LogFunc = re.compile(r'log\(.*x.*\)')
		TriFunc = re.compile(r'(sin|cos|tan)\(.*x.*\)')
		ExpoFunc = re.compile(r'\d\*\*x')
		OneFunc = re.compile(r'x')

		if ThreeFunc.search(express):
			return "３次関数"
		elif TwoFunc.search(express):
			return "２次関数"
		elif LogFunc.search(express):
			return "対数関数"
		elif TriFunc.search(express):
			return "三角関数"
		elif ExpoFunc.search(express):
			return "指数関数"
		elif OneFunc.search(express):
			return "１次関数"
		return None

	def getQuad(self):
		return self.quad

	def getUpDown(self):
		return self.updown

	def getIntercept(self):
		return self.intercept

	def getExtremum(self):
		return self.extremum

	def getFunction(self):
		return self.function

	def getSayStr():
		text = ""
		return text

def main():
	express = convertExpression(raw_input("Please input expression: "))
	xPosArray = [x for x in range(-5, 6)]
	yPosArray = [eval(express.replace('x', "(" + str(x) + ")")) for x in range(-5, 6)]
	sayinfo = SAYINFO(express, xPosArray, yPosArray)
	#text = sayinfo.getSayStr(express, xPosArray, yPosArray)
	print "Generated Arrays..."
	print "xPos = " + str(xPosArray)
	print "yPos = " + str(yPosArray)
	print ""
	print "象限: " + str(sayinfo.getQuad())
	print "増減: " + str(sayinfo.getUpDown())
	intercept = sayinfo.getIntercept()
	print "x切片 = " + str(intercept[0]) + "\ny切片 = " + str(intercept[1])
	print "極値: " + str(sayinfo.getExtremum()) if sayinfo.hasExtremum() else "持たない"
	print "これは、" + sayinfo.getFunction() + "です。"
	plt.grid()
	plt.plot(xPosArray, yPosArray)
	plt.show()


if __name__ == '__main__':
	main()
