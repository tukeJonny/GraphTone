#-*- coding: utf-8 -*-
import math
import re

split_operator = lambda formula: re.split('(?<!\()[+ \- \* \/]', formula)

#演算子の取り出し
def extract_operator(formula):
	res = []
	operator = ['+', '-', '*', '/']
	for r in formula:
		if r in operator:
			res.append(r)
	return res

#2x -> 2*x
def convertMultiple(sections):
	print "args is " + str(sections)
	p = re.compile("^\d+$") #数値が連続しているだけのやつ？

	for r,sec in enumerate(sections):
		print "[*] Processing " + sec + "..."
		spl = sec.split('x') #xで切り分ける
		print "[*] Converted string to array: " + str(spl)
		spl_0_len = len(spl[0]) #xで切り分けた左側の文字数
		print "[*] spl_0_len is " + str(spl_0_len)
		if spl_0_len <= 0 or p.match(sec):
			continue
		print "No continue operate."

		before_x = spl[0][spl_0_len-1] #xの直前の文字		
		print "[*] before_x is " + before_x

		if spl_0_len and before_x.isdigit(): #xの直前が数値ならば、*を追加
			print "[*] Changing..."
			sections[r] = str(spl[0]) + "*x"
		else:                                #そうでなければ、そのまま連結
			sections[r] = str(spl[0]) + "x"
		if len(spl) > 1: #xの右側がちゃんとあるかチェック(配列外参照を防ぐため)
			sections[r] = sections[r] + spl[1]
		print "Converted " + sections[r] + "!!\r\n"

	return sections

#関数に値xを代入した、結果の値を返す
def function(formula, x):
	inserted_formula = formula.replace("x", str(x))
	return eval(inserted_formula)


expression = raw_input("数式: ")
formula = expression.split('=')[1] #右辺の取り出し

#リスト化
operators = extract_operator(formula) #演算子のリストに変換
sections = split_operator(formula) #項のリストに変換

#演算子の補足
sections = convertMultiple(sections) #2x -> 2*x

converted_formula = ""
for r, sec in enumerate(sections):
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
converted_formula = re.sub(r'(sin|cos|tan|log)(.+)(.+)', r'math.\1(math.radians(\2))\3', converted_formula)
converted_formula = re.sub(r'(x\*\*)(\d+)', r'(\1\2)'  , converted_formula)

print "Converted " + converted_formula + "!!"

print "if x = 45, value is " + str(function(converted_formula, 45)) #f(x) = converted_formula とした時の f(45)

#ラジアン変換しなければいけない -> 解決?










