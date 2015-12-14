#-*- coding: utf-8 -*-
from math import sin, cos, tan, log, radians
import re

import numpy
from sympy import*

import add_multiplication as am


split_operator = lambda formula: re.split(r'(?<!\()[+ \-]', formula)


#演算子の取り出し
def extract_operator(formula):
	print "[*] Extracting operator..."
	res = []
	operator = ['+', '-', '*', '/']
	for r in formula:
		if r in operator:
			res.append(r)
	return res

def convertMultiple(sections, target):
	p = re.compile("^\d+$") #数値が連続しているだけのやつ？

	for r,sec in enumerate(sections):
		spl = sec.split(target) #xで切り分ける
		spl_0_len = len(spl[0]) #xで切り分けた左側の文字数
		if spl_0_len <= 0 or p.match(sec):
			continue
		
		before_x = spl[0][spl_0_len-1] #xの直前の文字		
		
		if spl_0_len and before_x.isdigit(): #xの直前が数値ならば、*を追加
			print "[*] Changing..."
			sections[r] = str(spl[0]) + "*" + target
		else:                                #そうでなければ、そのまま連結
			sections[r] = str(spl[0]) + target
		if len(spl) > 1: #xの右側がちゃんとあるかチェック(配列外参照を防ぐため)
			sections[r] = sections[r] + spl[1]
		#sin, cos, tan, logのチェック
		sections[r] = re.sub(r'(\d+)sin', r'\1*sin', sections[r])
		sections[r] = re.sub(r'(\d+)cos', r'\1*cos', sections[r])
		sections[r] = re.sub(r'(\d+)tan', r'\1*tan', sections[r])
		sections[r] = re.sub(r'(\d+)log', r'\1*log', sections[r])

		print "Converted " + sections[r] + "!!\r\n"

	return sections

#関数に値xを代入した、結果の値を返す
def function(obj, val):
	x=Symbol('x')
	try:
		ret = float(obj.subs([(x, val)]))
	except TypeError as err:
		print str(err)
		return ret
	return ret

def convertExpression(expression):
	print "expression="
	print expression
	"""
	formula = expression.split('=')[1] #右辺の取り出し
	#冪上を括弧で囲む
	formula = re.sub(r'\^([^+ \- \* \/]+)', r'^(\1)', formula)

	#リスト化
	operators = extract_operator(formula) #演算子のリストに変換
	sections = split_operator(formula) #項のリストに変換
	print "Sections = " + str(sections)

	#演算子の補足
	sections = convertMultiple(sections, 'x') #2x -> 2*x


	converted_formula = ""
	TriFunPattern = re.compile('(sin|cos|tan)')
	for r, sec in enumerate(sections):
		print "[*]sec is " + str(sec) + "..."
		#ラジアン変換処理を加味した文字列を足し入れる
		if re.match(TriFunPattern, sec[0:3]) != None:
			converted_formula += re.sub(r'(sin|cos|tan)([^\^]+)', r'\1(radians\2)', sec)  #version2 ()でくくっていないので、計算順序がおかしいかもしれない
		else:
			converted_formula += sec
		if r == len(sections)-1:
			continue
		converted_formula += operators[r]
		print "[+] Converting " + converted_formula + "..."

	converted_formula = converted_formula.replace("^", "**") #冪乗記号の変換
	converted_formula = re.sub(r'(x\*\*)([0-9 ( )]+)', r'(\1(\2))'  , converted_formula)

	print "Converted " + converted_formula + "!!"

	return converted_formula
	"""
	x = Symbol('x')
	if "=" in str(expression):
		expression = expression.split('=')[1] #右辺の取り出し
	expression = am.main(expression) #適切に乗算演算子を付加
	expression = expression.replace('^', '**').replace('***', '**') #冪乗表現を変更

	converted_formula = sympify(expression) #Sympyオブジェクト化
	return converted_formula

def sym2str(sympyobj):
	ret = str(sympyobj).replace('**', '^')
	return "y=%s"%ret

def getCoordinate(exp, begin, end):
	conv_exp = convertExpression(exp)
	print function(conv_exp, 5)
	xPosArray = [x for x in range(begin, end+1)]
	x = Symbol('x')
	print "xPosArray = %s"%str(xPosArray)
	try:
		yPosArray = [float(function(conv_exp, pos)) for pos in xPosArray]
	except TypeError as err:
		print str(err)
		yPosArray = [function(conv_exp, pos) for pos in xPosArray]
	print "yPosArray = %s"%str(yPosArray)
	return (xPosArray, yPosArray)

def main():
	exp = raw_input("Please input: ")
	print convertExpression(exp)


if __name__ == "__main__":
	main()

































