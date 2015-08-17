#-*- encoding: utf-8 -*-

"""
Usage:
	query_bing_images.py <query>
	query_bing_images.py -h | --help
	query_bing_images.py --version

Option:
	-h --help	show this screen
	--version	show version
"""

from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
from docopt import docopt

def get_soup(url):
	return BeautifulSoup(requests.get(url).text)

def main():
	options = docopt(__doc__, version='1.0')
	query = options['<query>'] #上のoptionsの<query>が添え字になっているところ(コマンドライン引数の１番目)
	print "Query is " + str(query)
	image_type = query
	if "二次関数" in image_type:
		image_type = "Quadratic function"
	elif  "一次関数" in image_type:
		image_type = "Linear function"

	url = "http://www.bing.com/images/search?q=" + query + "&gft=+filterui:color2-bw+filterui:imagesize-large&FORM=R5IR3"

	soup = get_soup(url)
	images = [a['src'] for a in soup.find_all("img", {"src":re.compile("mm.bing.net")})]

	for img in images:
		raw_img = urllib2.urlopen(img).read()
		cntr = len([i for i in os.listdir("images") if image_type in i]) + 1 #同じイメージタイプの画像がいくつあるか

		f = open("images/" + image_type + "_" + str(cntr) + ".jpg", "wb")
		f.write(raw_img)
		f.close()

if __name__ == '__main__':
		main()
