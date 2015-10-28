#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib3
import os

'''
Google Text to Speech API
"http://translate.google.com/translate_tts?ie=UTF-8&q=" + text + "&tl=js"
'''
class Say:
	'''
	#API登録しないといけない、めんどくさいからやめる。
	def get_announce(self,text):
		url = "http://translate.google.com/translate_tts?ie=UTF-8&q='" + text + "'&tl=js"
		user_agent={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
		#print url
		http = urllib3.PoolManager(10,headers=user_agent)
		r = http.request('GET', url)
		
			
		f = open('./say.wav', 'w')
		f.write(r.data)
		print r.data
		f.close
	'''
	def say(self,text):
		command = "say -v Kyoko -o say.wav --file-format=WAVE --data-format=LEI16@44100 '" + text + "'"
		print command
		os.system(command)


if __name__ == '__main__':
	say = Say()
	say.say("Hello")
