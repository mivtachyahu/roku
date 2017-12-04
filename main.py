#!/usr/bin/env python
import ssdp
import sys,tty,termios
import httplib, urlparse
from flask import Flask, g, render_template, redirect, request
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


def getRokus():
    return ssdp.discover("roku:ecp")[0].location

rokuURL = getRokus()
print rokuURL
rokuLocation = urlparse.urlparse(rokuURL)
rokuHost = rokuLocation.netloc
print "Host:" + rokuHost

conn = httplib.HTTPConnection(rokuHost)
conn.request("GET", "/query/device-info")
if conn.getresponse().status == 200:
    print "Connected to Roku"
conn.close()

headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

def make_request(path):
    requestString = "/keypress/" + path
    conn.request("POST", requestString, "", headers)
    conn.getresponse()
    conn.close()

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/<string:path>')
def get_path(path):
    make_request(path)
    return redirect('/')

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(8080)
print "Listening on port 8080"
IOLoop.instance().start()


#while True:
#    keyPress = raw_input(">")
#    if keyPress == 'quit':
#        print 'Quitting'
#        conn.close()
#        exit()
#    else:
#	requestString = "/keypress/" + keyPress
#        conn.request("POST", requestString, "", headers)
#	conn.getresponse()
#        conn.close()
