#-*- coding: utf-8 -*-
#音声読み上げさせる情報群
#軸 (保留)

#未達成課題
#極値を持つかどうかの判定
#関数の分類

from sympy import*
import re

class SAYINFO():
	def __init__(self, expression, xPosArray, yPosArray):
		#式定義
		self.exp = sympify(expression)
		x = Symbol('x')
		#微分
		self.df = diff(self.exp, x)
		#x軸との交点
		self.intersect = solve(Eq(self.df, 0))

		self.quad = calcQuadrant()
		self.updown = calcUpDown()
		self.intercept = calcIntercept()
		self.extremum = calcExtremum()
		self.function = classifyFunction()

	#何象限に属すか
	def calcQuadrant(self, xPosArray, yPosArray):
		quadrant = (False, False, False, False)
		for r in range(len(xPosArray)):
			x = xPosArray[0]
			y = yPosArray[0]
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
		#expressionを微分した式のx軸との交点を求める
		for r in range(1, len(self.intersect)+1):
			Dir.append(Dir[0]*((-1)**r))
		return Dir

	#x, y切片
	def calcIntercept(self, express):
		expression = sympify(express)
		x = Symbol('x')
		#x切片
		xI = expression.subs([(x, 0)])
		#eval(exp.replace('x', 0))
		#y切片
		yI = solve(Eq(expression, 0))
		return (xI, yI)

	#極値判定
	#２階導関数f''(x)に対し、f'(a) = 0となるようなaについて
	#f''(a)を求めた時、
	#負である場合は極大値を持ち
	#正である場合は極小値を持つ
	# => f''(a) = 0となってしまった場合、極値を持たないこととなる
	def hasExtremum(self):
		#２階導関数を求める
		ddf = diff(self.df, x)
		for r in self.intersect:
			#２階導関数に導関数のx軸との交点のx座標値を代入し、その値が0にならないか調べる
			if ddf.subs([(x, r)]) is 0:
				return False #0であれば、極値を持たない
		return True

	#極値
	def calcExtremum(self, express):
		if hasExtremum():
			extremum = [express.subs([(x, r)]) for r in self.intersect]
			#eval(exp.replace('x', r))
			return extremum
		else:
			return [] #極値は無い

	#関数分類
	def classifyFunction(self, express):
		ThreeFunc = re.compile(r'x\*\*3')
		TwoFunc = re.compile(r'x\*\*2')
		LogFunc = re.compile(r'log\(.*x.*\)')
		TriFunc = re.compile(r'(sin|cos|tan)\(.*x.*\)')
		ExpoFunc = re.compile(r'\d\*\*x')
		OneFunc = re.compile(r'x')

		if ThreeFunc.search(express):
			return u"３次関数"
		elif TwoFunc.search(express):
			return u"２次関数"
		elif LogFunc.search(express):
			return u"対数関数"
		elif TriFunc.search(express):
			return u"三角関数"
		elif ExpoFunc.search(express):
			return u"指数関数"
		elif OneFunc.search(express):
			return u"１次関数"
		return None

	def getSayStr():
		text = ""
		return text

def main():
	express = "((x)**(2))"
	xPosArray = [x for x in range(-5, 6)]
	yPosArray = [eval(express.replace('x', str(x))) for x in range(-5, 6)]
	sayinfo = SAYINFO()
	text = sayinfo.getSayStr(express, xPosArray, yPosArray)


if __name__ == '__main__':
	main()
