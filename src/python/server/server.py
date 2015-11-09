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

import threading
import urlparse
import zipfile
import time
import socket
import sys
import os
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn



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

    def make_response(self):
        print "exp: "+ str(self.exp) + "range: " + str(self.range)
        if(self.exp and self.range):
            print "make responce"
            xPosArray, yPosArray = parseExpression.getCoordinate(self.exp, int(self.beg), int(self.end))
            print "x = " + str(xPosArray)
            print "y = " + str(yPosArray)
            gensound.genSound(yPosArray)

    def read_file(self):
        message_parts=[""]
        f = open('./send.zip', 'r')
        for line in f:
            message_parts.append(line)
        self.message = "".join(message_parts)

    def zip(self):
        zipFile = zipfile.ZipFile("./send.zip","w",zipfile.ZIP_DEFLATED)
        zipFile.write("./image.png")
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
        self.zip()
        self.read_file()
        #self.wfile.write(self.message)
        return 



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) )
    from make_sound import *
    from numerical_formula import *

    myIP = socket.gethostbyname(socket.gethostname())
    print "myIP :" + myIP
    server = ThreadedHTTPServer((myIP, 8080), Handler)
    print 'Starting server, use <Ctrl-C> to stop\n'
    server.serve_forever()