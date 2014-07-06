# -*- coding:utf-8 -*-
'''
Author:Liu
'''
from BaseHTTPServer import BaseHTTPRequestHandler
import cgi 
import config
import urlparse
import psutil
from subprocess import PIPE
import  json 


import thread 
import SocketServer
# import save 
class MyTCPHandler(SocketServer.BaseRequestHandler):
    '''for receive data'''
    def handle(self):           
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # save.save(self.data)
        self.request.sendall('watching')


def receiver():  
    '''receive data as a function in a thread'''
    HOST, PORT = "localhost", 10001
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    print "A SocketServer is listen on " + HOST + ' : ' +str(PORT)
    server.serve_forever()
     
 


class GetPostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
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

        for field in form.keys():
            field_item = form[field] 
            self.wfile.write('\t%s=%s\n' % (field, form[field].value)) 
        return

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        # message_parts = [  
        #         'CLIENT VALUES:',    
        #         'client_address=%s (%s)' % (self.client_address,
        #                                     self.address_string()),  #返回客户端的地址和端口
        #         'command=%s' % self.command,  #返回操作的命令，这里比然是'get'
        #         'path=%s' % self.path,  #返回请求的路径
        #         'real path=%s' % parsed_path.path, #返回通过urlparse格式化的路径
        #         'query=%s' % parsed_path.query, #返回urlparse格式化的查询语句的键值
        #         'request_version=%s' % self.request_version, #返回请求的http协议版本号
        #         '',
        #         'SERVER VALUES:', #服务器段信息
        #         'server_version=%s' % self.server_version, #返回服务器端http的信息
        #         'sys_version=%s' % self.sys_version, #返回服务器端使用的python版本
        #         'protocol_version=%s' % self.protocol_version,  #返回服务器端使用的http协议版本
        #         '',
        #         'HEADERS RECEIVED:',
        #         ]
        #for name, value in sorted(self.headers.items()):  #返回項添加头信息，包含用户的user-agent信息，主机信息等
        #    message_parts.append('%s=%s' % (name, value.rstrip()))
        #message_parts.append('')
        #message = '\r\n'.join(message_parts)
        
        self.send_response(200)  #返回给客户端结果，这里的响应码是200 OK，并包含一些其他信
        self.end_headers() #结束头信息

        #...file
        if self.path=='/':
            mainpage(self)
        elif 'graphic' in self.path:
            name=self.path.split('/')[3]
            print name
            graphic(self,name)
        elif 'info' in self.path:
            info(self)   
        elif 'ajaxget' in self.path:
            ajaxget(self)  

        else:
            fileHandle = open ( self.path.lstrip('/') )
            for content in fileHandle:
                self.wfile.write(content)
            fileHandle.close()
        return

def mainpage(obj):
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
    fileHandle = open ( './view/info.html' )
    for content in fileHandle:
        obj.wfile.write(content)
    fileHandle.close()

    fileHandle = open ( './view/footer.html' )
    for content in fileHandle:
        obj.wfile.write(content)
    fileHandle.close()
    return

def ajaxget(obj):
    cpu_percent = psutil.cpu_percent(interval = 1)
    mer_percent = psutil.virtual_memory().percent
    io_radio = psutil.disk_io_counters()
    io_radio_read, io_radio_write = io_radio.read_bytes, io_radio.write_bytes
    info='{"name1":{CPU:20,iow:3000000000,ior:2000000000,rem:40}}'
    info='{"localhost":{CPU:'+str(cpu_percent)+',iow:'+str(io_radio_write)+',ior:'+str(io_radio_read)+',rem:'+str(mer_percent)+'},'+info.lstrip('{')
    obj.wfile.write(info)
    return

def graphic(obj,name):
    #getdaydata(name)
    obj.wfile.write('{cpu:{"1.1":[10,50],"1.2":[20,30],"1.3":[30,40],"1.4":[40,80],"1.5":[50,70],"1.6":[60,40],"1.7":[70,20]},mem:{"1.1":[10,10],"1.2":[20,30],"1.3":[30,40],"1.5":[40,70],"1.6":[50,40]},ior:{"1.1":[10,50],"1.2":[20,30],"1.3":[30,40],"1.4":[40,30],"1.5":[50,40]},iow:{"1.1":[10,50],"1.2":[20,30],"1.3":[30,40]}}')
    return

def getname():
    return ['name1','n3','n4']


if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('localhost', config.PORT), GetPostHandler) 
    thread.start_new_thread(receiver, ())  
    print 'Starting server at %d, use <Ctrl-C> to stop' %config.PORT
    server.serve_forever()  #保存程序一直运行
