#!/usr/bin/env python
# -*- coding: utf-8 -*-
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import urlparse

class Handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        '''
        parsed_path.query #getの?以降のパラメータ(式)が入っている。
        関数(parsed_path.query) #式を引数に音声ファイルを生成する関数
        '''
        message_parts=[""]
        f = open('aa.mp3', 'r')
        for line in f:
            message_parts.append(line)
        message = "".join(message_parts)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server = ThreadedHTTPServer(('localhost', 8080), Handler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()