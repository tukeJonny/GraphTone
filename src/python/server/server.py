#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
request Ex.
http://localhost:8080?expression=y=x^2&image=True&sound=True&range=-5:5

--params--
expression="y=x^2"
image: True or False    #first letter is only Uppercase　
sound: True or False    #first letter is only Uppercase
range: "min range : max range"

use "%20" to input space
'''

#server

import sys
import threading
import urlparse
import zipfile
import time
import socket
import os
import subprocess

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn

#make image
sys.path.append('../make_image')
import makeimage
#make sound
sys.path.append('../make_sound')
import gensound
sys.path.append('../numerical_formula')
import parseExpression
sys.path.append('../make_text_for_read')
import makeinfo



class Handler(BaseHTTPRequestHandler):

    #初期化用関数
    def init(self):
        self.imageBool = False
        self.soundBool = False
        self.range = ""
        self.exp = ""

    def judge_param(self,param,value):
        

        if(param == "expression"):
            self.exp = value

        if(param == "image"):
            if(value):
                self.imageBool = True

        if(param == "sound"):
            if(value):
                self.imageBool = True

        if(param == "range"):
            self.range = map(int,value.split(":"))
            self.beg = self.range[0]
            self.end = self.range[1]
            print "range: " + str(self.beg) + "," + str(self.end)

    def make_sound(self):
        print "make sound..."
        self.xPosArray, self.yPosArray = parseExpression.getCoordinate(self.exp, int(self.beg), int(self.end))
        print "x = " + str(self.xPosArray)
        print "y = " + str(self.yPosArray)
        gensound.genSound(self.yPosArray)

    def make_image(self):
        print "make image..."
        makeimage.makePng(self.exp, self.xPosArray, self.yPosArray)

    def make_say_text(self):
        print "make say_text..."
        sayobj = makeinfo.SAYINFO(self.exp, self.xPosArray, self.yPosArray)
        ret = sayobj.makeSayStr()
        return ret

    def make_response(self):
        print "making response..."
        if(self.exp and self.range):
            self.make_sound()
            self.make_say_text()
            self.make_image()

    def read_file(self):
        print "read zip file..."
        message_parts=[""]
        f = open('./send.zip', 'r')
        for line in f:
            message_parts.append(line)
        self.message = "".join(message_parts)

    def join_mp3(self, a, b, output):
        #print "Check here...: %s"%subprocess.check_output("ls -al", shell=True)
        subprocess.check_output("echo \"y\" | ffmpeg -i %s -i %s -filter_complex \"concat=n=2:v=0:a=1\" %s"%(a,b,output), shell=True)

    def zip(self):
        print "make zip file..."
        zipFile = zipfile.ZipFile("./send.zip","w",zipfile.ZIP_DEFLATED)
        zipFile.write("./output.png")
        zipFile.write("./output.mp3")
        zipFile.close()

    def do_GET(self):
        path = urlparse.urlparse(self.path)
        params = urlparse.parse_qsl(self.path)
        self.init()
        for i,param in enumerate(params):
            print param
            #expressionはクエリの"&""がつくので外して渡す。
            if(i == 0):
                self.judge_param(param=str(param[0])[2:],value=param[1])
                    
            else:
                self.judge_param(param=param[0],value=param[1])
        self.make_response()

        #responce
        #time.sleep(10)         #wait check
        self.send_response(200)
        self.end_headers()
        self.join_mp3("say.mp3", "graph.mp3", "output.mp3")
        self.zip()
        self.read_file()
        self.wfile.write(self.message)
        print "All Done"
        return 



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    myIP = socket.gethostbyname(socket.gethostname())
    print "myIP :" + myIP
    server = ThreadedHTTPServer((myIP, 8080), Handler)
    print 'Starting server, use <Ctrl-C> to stop\n'
    server.serve_forever()