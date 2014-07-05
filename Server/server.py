# -*- coding:utf-8 -*-
from BaseHTTPServer import BaseHTTPRequestHandler
import cgi 
import config
import urlparse

class GetPostHandler(BaseHTTPRequestHandler):
    def do_POST(self): #还是重写这个方法
        form = cgi.FieldStorage(  #cgi.FieldStorage实例效果类似一个字典，包含键－值和len等内置函数
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

    def do_GET(self):   #重写这个方法
        parsed_path = urlparse.urlparse(self.path)
        # message_parts = [  #建立一个想要返回的列表
        #         'CLIENT VALUES:',    #客户端信息
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
    for i in range[cnt()]
        fileHandle = open ( './view/simple.html' )
        for content in fileHandle:
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
    return

def ajaxget():
    return '{}'

def cnt():
    return 3

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('localhost', config.PORT), GetPostHandler) 
    print 'Starting server at %d, use <Ctrl-C> to stop' %config.PORT
    server.serve_forever()  #保存程序一直运行
