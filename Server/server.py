# -*- coding:utf-8 -*-
'''
Author : Liu Yang
Date : July 6
'''
from BaseHTTPServer import BaseHTTPRequestHandler
import cgi 
import config
import urlparse
import psutil
from subprocess import PIPE
import json 
import thread
import SocketServer
import save
import load
import socket
allhostips=[]

class MyTCPHandler(SocketServer.BaseRequestHandler):
    '''for receive data'''
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        da=json.loads(self.data)
        save.save(da)
        if not self.client_address[0] in allhostips:
            allhostips.append(self.client_address[0])
            print 'a new ip \'' +self.client_address[0]+'\' is add to the list!'


def receiver():  
    '''receive data as a function in a thread'''
    HOST, PORT = config.RECEIVERHOST, config.RECEIVERPORT
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    print "A SocketServer is listen on " + HOST + ' : ' +str(PORT)
    server.serve_forever()
     
 


class GetPostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        '''POST default methord'''
        form = cgi.FieldStorage(
        fp=self.rfile,
        headers=self.headers,
        environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        self.send_response(200)
        self.end_headers() 
        self.wfile.write('Client: %s\n' % str(self.client_address)) 
        self.wfile.write('User-agent: %s\n' % str(self.headers['user-agent'])) 
        self.wfile.write('Path: %s\n' % self.path)
        self.wfile.write('Form data:\n')
        self.wfile.write('You are willing to give a POST request to Hosts-Status-Monitor but it is not allowed ') 
        return

    def do_GET(self):
        '''Answer for GET request'''

        parsed_path = urlparse.urlparse(self.path)
        self.send_response(200)  #返回给客户端结果，这里的响应码是200 OK，并包含一些其他信
        self.end_headers() #结束头信息

        #A router for some webpage 
        if self.path=='/':
            #(for showing on explore)show main page
            mainpage(self)
        elif 'graphic' in self.path:
            #(for ajax get)show one host's history info in two ways : 'day' and 'hour'
            
            
            if 'hour' in self.path:
                print self.path
                name=self.path.split('/')[2]
                print name
                graphichour(self,name)
            else:
                print self.path
                name=self.path.split('/')[3]
                print name
                graphic(self,name)
        elif 'info' in self.path:
            #(for showing on explore) show one host's history infomation
            info(self)
        elif 'ajaxget' in self.path:
            ajaxget(self)  
        #FILE system for GET request 'css' 'js' file or something
        else:
            fileHandle = open ( self.path.lstrip('/') )
            for content in fileHandle:
                self.wfile.write(content)
            fileHandle.close()

        #if someone watching
        for ip in allhostips:
            s = socket.socket()
            s.connect((ip, 20000))
            s.sendall('watching')
            s.close()
        return

def mainpage(obj):
    '''(for showing on explore) all host's data for now '''
    fileHandle = open ( './view/index.html' )
    for content in fileHandle:
        obj.wfile.write(content)
    fileHandle.close()
    fileHandle = open ( './view/localhost.html' )
    for content in fileHandle:
        obj.wfile.write(content)
    fileHandle.close()
    for name in getname():
        fileHandle = open ( './view/simple.html' )
        for content in fileHandle:
            #auto load pages
            content=content.replace('CPUID',name+'cpu')
            content=content.replace('IORID',name+'ior')
            content=content.replace('IOWID',name+'iow')
            content=content.replace('MEMID',name+'mem')
            content=content.replace('NAME',name)
            obj.wfile.write(content)
        fileHandle.close()

    fileHandle = open ( './view/footer.html' )
    for content in fileHandle:
        obj.wfile.write(content)
    fileHandle.close()
    return

def info(obj):
    '''(for showing on explore) one host's complex data in history '''
    fileHandle = open ( './view/info.html' )
    name=obj.path.split('/')[2]
    for content in fileHandle:
        name=obj.path.split('/')[2]
        content=content.replace('../tool','../../tool')
        content=content.replace('NAME',name)
        if 'hour' in obj.path:
            content=content.replace('graphic','graphichour')
        obj.wfile.write(content)
    fileHandle.close()

    fileHandle = open ( './view/footer.html' )
    for content in fileHandle:
        obj.wfile.write(content)
    fileHandle.close()
    return

def ajaxget(obj):
    ''' return all HOST status for now'''
    cpu_percent = psutil.cpu_percent(interval = 1)
    mer_percent = psutil.virtual_memory().percent
    io_radio = psutil.disk_io_counters()
    io_radio_read, io_radio_write = io_radio.read_bytes, io_radio.write_bytes
    info=json.dumps(load.allinfo())
    print info
    info='{"localhost":{cpu:'+str(cpu_percent)+',iow:'+str(io_radio_write)+',ior:'+str(io_radio_read)+',mem:'+str(mer_percent)+'},'+info.lstrip('{')
    obj.wfile.write(info)
    return

def graphic(obj,name):

    '''return one host data for 10 days'''
    #testing data
    #obj.wfile.write('{cpu:{"1.1":[10,50],"1.2":[20,30],"1.3":[30,40],"1.4":[40,80],"1.5":[50,70],"1.6":[60,40],"1.7":[70,20]},mem:{"1.1":[10,10],"1.2":[20,30],"1.3":[30,40],"1.5":[40,70],"1.6":[50,40]},ior:{"1.1":[10,50],"1.2":[20,30],"1.3":[30,40],"1.4":[40,30],"1.5":[50,40]},iow:{"1.1":[10,50],"1.2":[20,30],"1.3":[30,40]}}')
    data=load.getdaydata(name)
    print '!!!'+str(data)+'!!!'
    obj.wfile.write(data)
    return

def getname():
    ''' return all host names'''
    return load.getallname()


def graphichour(obj,name):
    '''return one host data for 10 hours'''
    #obj.wfile.write('{cpu:{"1":[10,50],".2":[20,30],".3":[30,40],".4":[40,80],".5":[50,70],".6":[60,40],".7":[70,20]},mem:{".1":[10,10],"1.2":[20,30],"1.3":[30,40],"1.5":[40,70],"1.6":[50,40]},ior:{"1.1":[10,50],"1.2":[20,30],"1.3":[30,40],"1.4":[40,30],"1.5":[50,40]},iow:{"1.1":[10,50],"1.2":[20,30],"1.3":[30,40]}}')
    data=load.gethourdata(name)
    print '!!!'+str(data)+'!!!'
    obj.wfile.write(data)
    return

if __name__ == '__main__':
    '''function main() , '''
    from BaseHTTPServer import HTTPServer
    server = HTTPServer((config.HOST, config.PORT), GetPostHandler) 
    thread.start_new_thread(receiver, ()) 
    print 'Starting server at %d, use <Ctrl-C> to stop' %config.PORT
    server.serve_forever()  #保存程序一直运行
