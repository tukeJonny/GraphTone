#-*- coding: utf-8 -*-
from math import sin, cos, tan, log, radians
import re

import numpy
import pyaudio

split_operator = lambda formula: re.split('(?<!\()[+ \- \* \/]', formula)

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
	#print "args is " + str(sections)
	p = re.compile("^\d+$") #数値が連続しているだけのやつ？

	for r,sec in enumerate(sections):
		#print "[*] Processing " + sec + "..."
		spl = sec.split(target) #xで切り分ける
		#print "[*] Converted string to array: " + str(spl)
		spl_0_len = len(spl[0]) #xで切り分けた左側の文字数
		#print "[*] spl_0_len is " + str(spl_0_len)
		if spl_0_len <= 0 or p.match(sec):
			continue
		#print "No continue operate."

		before_x = spl[0][spl_0_len-1] #xの直前の文字		
		#print "[*] before_x is " + before_x

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
def function(formula, x):
	str_x = str(x)
	if x < 0: #負の値が来た時、括弧でくくってやる
		str_x = "(" + str_x + ")"
	inserted_formula = formula.replace("x", str_x)
	return eval(inserted_formula)


def convertExpression(expression):
	#expression = raw_input("数式: ")
	formula = expression.split('=')[1] #右辺の取り出し
	#冪上を括弧で囲む
	formula = re.sub(r'\^([^+ \- \* \/]+)', r'^(\1)', formula)

	#リスト化
	operators = extract_operator(formula) #演算子のリストに変換
	sections = split_operator(formula) #項のリストに変換

	#演算子の補足
	sections = convertMultiple(sections, 'x') #2x -> 2*x


	converted_formula = ""
	TriFunPattern = re.compile('(sin|cos|tan)')
	for r, sec in enumerate(sections):
		print "[*]sec is " + str(sec) + "..."
		#ラジアン変換処理を加味した文字列を足し入れる
		if re.match(TriFunPattern, sec[0:3]) != None:
			#converted_formula += re.sub(r'(sin|cos|tan)(.+)', r'\1(radians\2)', sec) #ココが冪乗の括弧のくくり方がおかしい原因かも
			converted_formula += re.sub(r'(sin|cos|tan)([^\^]+)', r'\1(radians\2)', sec)  #version2 ()でくくっていないので、計算順序がおかしいかもしれない
			#converted_formula += re.sub(r'(sin|cos|tan)([^\^]+)(\^\d+)?', r'(\1(radians\2)\3)', sec) version3 -> Tracebackが起きる ^2
		else:
			converted_formula += sec
		if r == len(sections)-1:
			continue
		converted_formula += operators[r]
		print "[+] Converting " + converted_formula + "..."

	converted_formula = converted_formula.replace("^", "**") #冪乗記号の変換
	"""
	math_lib_func = ['sin', 'cos', 'tan', 'log']
	for func in math_lib_func:
		addMath = "math." + func
		converted_formula = converted_formula.replace(func, addMath)
	"""
	#print converted_formula
	#converted_formula = re.sub(r'(sin|cos|tan)(.+)(.+)', r'math.\1(math.radians(\2))\3', converted_formula)
	converted_formula = re.sub(r'(x\*\*)([0-9 ( )]+)', r'(\1(\2))'  , converted_formula)

	print "Converted " + converted_formula + "!!"

	return converted_formula
	#print "if x = 45, value is " + str(function(converted_formula, 45)) #f(x) = converted_formula とした時の f(45)

#y=x^4-3x^3+5x^2*cos(2x)/sin(2x)-log(x)+10x+1000 -> (x**((4)))-3*(x**((3)))+5*(x**((2)))*cos(radians(2*x))/sin(radians(2*x))-log(x)+10*x+1000
#y=2x^3-10x^2+10/x*cos(2x)/sin(2x)*log(x) -> 2*(x**((3)))-10*(x**((2)))+10/x*cos(radians(2*x))/sin(radians(2*x))*log(x)
#y=10x^2-1000/x*log(1000x)/sin(2x) ->  10*(x**((2)))-1000/x*log(1000*x)/sin(radians(2*x))
#y=x^2-10x+2^x+100 -> (x**((2)))-10*x+2**(x)+100
#y=x^2-10x+100^10x+100 -> (x**((2)))-10*x+100**(10*x)+100
#y=x^3+sin(2x)^2+cos(2x)^10+100x^2+10x+1 ->  (x**((3)))+sin(radians(2*x))**(2)+cos(radians(2*x))**(10)+100*(x**((2)))+10*x+1

def getCoordinate(exp, begin, end):
	conv_exp = convertExpression(exp)
	print "Expression: " + conv_exp
	print "Converted: " + conv_exp
	xPosArray = [x for x in range(begin, end+1)]
	yPosArray = [function(conv_exp, x) for x in xPosArray]

	#print "xPosArray = " + str(xPosArray) + "\nyPosArray = " + str(yPosArray)
	return (xPosArray, yPosArray)






































