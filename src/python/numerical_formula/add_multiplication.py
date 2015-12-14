#!/usr/bin/env python
# -*- coding: utf-8 -*-
trigon_log = ["S","C","T","L"]
operand = ["+","-","*","/"]
left_parenthesis = "("
right_parenthesis = ")"
dot = "."

'''
num 				0
trigon_log	 		1
operand 			2
left_parenthesis 	3
right_parenthesis 	4
dot					5
variable			6
'''

def to_string(list):
	return "".join(list)


def string_list(exp):
	string_list = list(str(exp))
	return string_list

#string型
def convertor(exp):
	exp = exp.replace("sin","S")
	exp = exp.replace("cos","C")
	exp = exp.replace("tan","T")
	exp = exp.replace("log","L")
	return exp

#string型
def re_convertor(exp):
	exp = exp.replace("S","sin")
	exp = exp.replace("C","cos")
	exp = exp.replace("T","tan")
	exp = exp.replace("L","log")
	return exp



def discrimination(c):
	#print char
	if(c.isdigit()):
		return 0
	elif(c in trigon_log):
		return 1
	elif(c in operand):
		return 2
	elif(c == left_parenthesis):
		return 3
	elif(c == right_parenthesis):
		return 4	
	elif(c == dot):
		return 5
	else:
		return 6

def add_multiplication(exp_type,exp_list):
	diff = 0
	for i in xrange(len(exp_type)):
		#print str(i) + ":" +str(exp_list)

		if((i+1+diff) == len(exp_type)):
			break
		#num
		if(exp_type[i+diff] == 0):

			#trigon_log || left_parenthesis || variable
			if(exp_type[i+1+diff] in [1,3,6]):
				print str(exp_list[i+diff]) + "->"
				print str(exp_list[i+1+diff])
				exp_type.insert(i+1+diff,2)
				exp_list.insert(i+1+diff,"*")
				diff += 1

			else:
				None

		#right_parenthesis
		elif(exp_type[i+diff] == 4):

			#num || trigon_log || left_parenthesis || variable
			if(exp_type[i+1+diff] in [0,1,3,6]):
				print str(exp_list[i+diff]) + "->"
				print str(exp_list[i+1+diff])
				exp_type.insert(i+1+diff,2)
				exp_list.insert(i+1+diff,"*")
				diff += 1
		else :
			None
	return exp_list

def main(exp):
	exp = convertor(exp)
	exp_list = string_list(exp)
	#print exp_list
	exp_type = []
	for ele in exp_list:
		exp_type.append(discrimination(ele))
	#print type_list
	new_exp = add_multiplication(exp_type,exp_list)
	new_exp = to_string(new_exp)
	new_exp = re_convertor(new_exp)
	return new_exp


if __name__ == '__main__':
	exp = "2.0x+log(3.1x)+sin(2x^2)"
	main(exp)

