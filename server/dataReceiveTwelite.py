# coding: UTF-8
from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
import os
import param_server
import dataStoreTwelite

class Handle(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        text = post_body.decode()
        dataStoreTwelite.log(text)

httpd = HTTPServer((param_server.ADDRESS, 8048), Handle)
print("sensor-data receiver started")
httpd.serve_forever()
