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
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn



class Handler(BaseHTTPRequestHandler):
    '''
    def __init__(self):
        self.expression = "y=x^2"
        self.imageBool = False
        self.soundBool = False
        self.range = [-5,5]
    '''

    def judge_param(self,param,value):
        if(param == "expression"):
            self.expression = value
            '''
            数式から画像、音声を生成する処理を行う
            '''
        if(param == "image"):
            if(value):
                self.imageBool = True

        if(param == "sound"):
            if(value):
                self.imageBool = True
        if(param == "range"):
            self.range = map(int,value.split(":"))

    def read_file(self):
        message_parts=[""]
        f = open('./send.zip', 'r')
        for line in f:
            message_parts.append(line)
        self.message = "".join(message_parts)

    def zip(self):
        zipFile = zipfile.ZipFile("./send.zip","w",zipfile.ZIP_DEFLATED)
        zipFile.write("./image.png")
        zipFile.write("./sound.mp3")
        zipFile.close()

    def do_GET(self):
        path = urlparse.urlparse(self.path)
        params = urlparse.parse_qsl(self.path)
        for i,param in enumerate(params):
            print param
            if(i == 0):
                self.judge_param(param=str(param[0])[2:],value=param[1])
                    
            else:
                self.judge_param(param=param[0],value=param[1])
        
        #responce
        #time.sleep(10)         #wait check
        self.send_response(200)
        self.end_headers()
        self.zip()
        self.read_file()
        self.wfile.write(self.message)
        return 



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    myIP = socket.gethostbyname(socket.gethostname())
    print "myIP :" + myIP
    server = ThreadedHTTPServer((myIP, 8080), Handler)
    print 'Starting server, use <Ctrl-C> to stop\n'
    server.serve_forever()