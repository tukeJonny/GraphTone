# coding: utf-8
from numpy import*
from numpy.linalg import*

""" 4つの座標から、３次関数を導き出す """
def cubicFunc(x1, y1, x2, y2, x3, y3, x4, y4):
	coefficient_matrix = array( #係数行列
		[[x1*x1*x1, x1*x1, x1, 1],
		[x2*x2*x2, x2*x2, x2, 1],
		[x3*x3*x3, x3*x3, x3, 1],
		[x4*x4*x4, x4*x4, x4, 1],]
		)

	ans_matrix = array( #右辺
		[y1, y2, y3, y4]
		)

	ans = solve(coefficient_matrix, ans_matrix)
	
	print "\n\ny = " + str(ans[0]) + "x^3 + " + str(ans[1]) + "x^2 + " + str(ans[2]) + "x + " + str(ans[3]) + "\n"

""" 3つの座標から、２次関数を導き出す """
def quadraticFunc(x1, y1, x2, y2, x3, y3):
	coefficient_matrix = array( #係数行列
		[[x1*x1, x1, 1],
		[x2*x2, x2, 1],
		[x3*x3, x3, 1],]
		)

	ans_matrix = array( #右辺
		[y1, y2, y3]
		)

	ans = solve(coefficient_matrix, ans_matrix)

	print "\n\ny = " + str(ans[0]) + "x^2 + " + str(ans[1]) + "x + " + str(ans[2])  + "\n"

""" 2つの座標から、１次関数を導き出す """
def linearFunc(x1, y1, x2, y2):
	coefficient_matrix = array( #係数行列
		[[x1, 1],
		[x2, 1],]
		)

	ans_matrix = array( #右辺
		[y1, y2]
		)

	ans = solve(coefficient_matrix, ans_matrix)

	print "\n\ny = " + str(ans[0]) + "x + " + str(ans[1])  + "\n"

""" main関数 """
def main():
	print "?次関数: "
	mode = raw_input()
	print "\n座標を入力してください。"
	print "形式: x1,y1,x2,y2,x3,y3,...xn,yn"
	coor = raw_input()
	arg = coor.split(',')
	arg = map(int, arg)
	if(mode == "1"):
		linearFunc(arg[0], arg[1], arg[2], arg[3])
	elif(mode == "2"):
		quadraticFunc(arg[0], arg[1], arg[2], arg[3], arg[4], arg[5])
	elif(mode == "3"):
		cubicFunc(arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], arg[6], arg[7])
	else:
		print "Error: Invalid Input..."

if __name__ == '__main__':
	main()