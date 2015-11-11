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
import threading
import urlparse
import zipfile
import time
import socket
import sys
import os
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
#make image
from matplotlib import*
import matplotlib.pyplot as plt
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
#make sound
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) )
from make_sound import *
from numerical_formula import *



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
        xPosArray, yPosArray = parseExpression.getCoordinate(self.exp, int(self.beg), int(self.end))
        print "x = " + str(xPosArray)
        print "y = " + str(yPosArray)
        gensound.genSound(yPosArray)

    def make_image(self):
        print "make image..."
        ext_modules = [
            Extension( "makeimage", ["makeimage.pyx"] ),
            #Extension( "parseExpression", ["parseExpression.pyx"])
        ]

        setup(
            name = "make image",
            cmdclass = { "build_ext" : build_ext },
            ext_modules = ext_modules,
        )
        
        plt.title(self.exp)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()
        plt.plot(self.xPosArray, self.yPosArray, 'o')
        plt.savefig('output.png', format='png', dpi=300)

    def make_response(self):
        print "making response..."
        if(self.exp and self.range):
            self.make_sound() 
            self.make_image()

    def read_file(self):
        print "read zip file..."
        message_parts=[""]
        f = open('./send.zip', 'r')
        for line in f:
            message_parts.append(line)
        self.message = "".join(message_parts)

    def zip(self):
        print "make zip file..."
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