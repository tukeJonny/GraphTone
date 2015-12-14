#-*- coding: utf-8 -*-
#音声読み上げさせる情報群

import sys
import subprocess
from math import*

from sympy import*
import matplotlib.pyplot  as plt

sys.path.append('../numerical_formula')
from parseExpression import*

import re

#式によっては、計算後の解が値ではなく式で表されることがある
#これでは、ユーザが混乱するため、敢えて小数点精度を落とすことである程度判りやすくする。
#現時点で、複素数が残ってしまう問題がまだある
fpPrecise = 10
xyrange = 1000

radianize = lambda val: val / 180.0 * pi

class SAYINFO():
	def __init__(self, expression, xPosArray, yPosArray):
		#self.noradian_str = lambda expression: re.sub(r'radians(\(.*\))', r'\1', expression)
		#式定義
		self.expression = convertExpression(expression)
		#self.exp = sympify(expression)
		self.x = Symbol('x')
		#微分
		self.df = diff(self.expression, self.x)
		#x軸との交点
		self.intersect = solve(Eq(self.df, 0))
		print "intersect has calculated now: " + str(self.intersect)

		self.quad = self.calcQuadrant(xPosArray, yPosArray)
		self.updown = self.calcUpDown(yPosArray[0], yPosArray[1])
		self.intercept = self.calcIntercept(self.expression)
		self.extremum = self.calcExtremum(self.expression)
		self.function = self.classifyFunction(self.expression)

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
	#微分して判断しているため、実際の上下の数と異なっている問題あり
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
		#expression = sympify(self.noradian_str(express))
		
		#x切片
		xI = solve(Eq(express, 0))
		#eval(exp.replace('x', 0))
		#y切片
		val = 0
		#if(self.classifyFunction(self.expression) == "三角関数"):
		#		val = radianize(val)
		yI = express.subs([(self.x, val)])
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
			val = r
			if(self.classifyFunction(self.expression) == "三角関数"):
				val = radianize(r)
			#２階導関数に導関数のx軸との交点のx座標値を代入し、その値が0にならないか調べる
			if ddf.subs([(self.x, val)]) == 0:
				return False #0であれば、極値を持たない
		return True

	#極値
	def calcExtremum(self, express):
		#express = sympify(self.noradian_str(express))
		#express = express
		if self.hasExtremum() and self.intersect is not False:
			extremum = []
			#[express.subs([(self.x, r)]) for r in self.intersect]
			for r in self.intersect:
				val = r
				if self.classifyFunction(self.expression) == "三角関数":
					val = radianize(r)
				extremum.append(express.subs([(self.x, val)]))
			#eval(exp.replace('x', r))
			return extremum
		else:
			return [] #極値は無い

	#関数分類
	def classifyFunction(self, express):
		#express = str(sympify(self.noradian_str(express)))
		express = str(express)
		ThreeFunc = re.compile(r'x\*\*3')
		TwoFunc = re.compile(r'x\*\*2')
		LogFunc = re.compile(r'log\(.*x.*\)')
		TriFunc = re.compile(r'(sin|cos|tan)\(.*x.*\)')
		ExpoFunc = re.compile(r'\d+\*\*x')
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



	def makeSayStr(self):
		text = ""
		#********** 関数種別 **********
		text += "このグラフは%sです。" % self.getFunction()
		#********** 式 **********
		text += "このグラフの式わ%sです。" % re.sub(r'([x0-9 \+ \- \/]+)\^([x0-9 \+ \- \/]+)', r'\1の\2乗', sym2str(self.expression)).replace('=', 'いこうる')

		#********** 象限 **********
		quad = self.getQuad()
		for idx, b in enumerate(quad):
			if b == True:
				text += "第%d"%(idx+1)
		text += "象限を通ります。"
		#********** 増減 **********
		text += "このグラフわ"
		for ud in self.getUpDown():
			if ud >= 0:
				text += "上がって"
			else:
				text += "下がって"
		text += "いきます。"
		#********** 切片 **********
		intercept = self.getIntercept()
		text += "x切片わ%sy切片わ%sです。"%(str(intercept[0]), intercept[1])
		#********** 極値 **********
		#text += "極値: " + str(self.getExtremum()) if self.hasExtremum() else "持たない"
		if self.hasExtremum():
			text += "極ちわ%sです。" % str(self.getExtremum()).replace('[', '').replace(']', '')
		else:
			text += "極ちわありません。"
		subprocess.check_output("say -v Kyoko -o say.wav --file-format=WAVE --data-format=LEI16@44100 '%s'"%text, shell=True)
		subprocess.check_output('echo "y" | ffmpeg -i %s -ab 128 %s'%("say.wav", "say.mp3"), shell=True) #mp3に変換
		return text

def main():
	global fpPrecise
	global xyrange

	#express = convertExpression(raw_input("Please input expression: "))
	express = raw_input("Please input expression: ")
	print "Express is %s"%express
	xPosArray = [x for x in range(-xyrange, xyrange+1)]
	yPosArray = [eval(express.replace('x', "(" + str(x) + ")")) for x in range(-xyrange, xyrange+1)]
	sayinfo = SAYINFO(express, xPosArray, yPosArray)
	#text = sayinfo.makeSayStr(express, xPosArray, yPosArray)
	"""
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
	"""
	saystr = sayinfo.makeSayStr()
	print saystr
	plt.grid()
	plt.plot(xPosArray, yPosArray)
	plt.show()
	subprocess.check_output("say -v Kyoko \"%s\""%saystr, shell=True)
	

if __name__ == '__main__':
	main()
