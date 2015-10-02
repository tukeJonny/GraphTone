#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
request Ex.
http://localhost:8080?expression="y=x^2"&image=true&sound=true
'''

import threading
import urlparse
import zipfile
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn



class Handler(BaseHTTPRequestHandler):
    '''
    self.message
    self.imageBool
    self.imageBool
    '''

    def judge_param(self,param,value):
        if(param == "expression"):
            '''
            数式から画像、音声を生成する処理を行う
            '''
        if(param == "image"):
            if(value):
                self.imageBool = True

        if(param == "sound"):
            if(value):
                self.imageBool = True

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
        self.send_response(200)
        self.end_headers()
        self.read_file()
        self.wfile.write(self.message)
        return 


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server = ThreadedHTTPServer(('localhost', 8080), Handler)
    print 'Starting server, use <Ctrl-C> to stop\n'
    server.serve_forever()