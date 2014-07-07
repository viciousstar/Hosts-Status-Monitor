'''
Author: THL
Date: 20140705
Version: python 2.7
Purpose: get [hostname, cpu_percent, mer_percent, io] and transmit them to remote host
Interface:  transmit a dict, and change catching speed acooding to http
'''

import psutil
from subprocess import PIPE
import  json
import socket
import time
import threading
import SocketServer


inte = 3
class MyTCPHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		global inte
		self.data = self.request.recv(1024)
		print self.data
		if self.data ==  "watching":
			inte = 1
		else:
			inte = 5

def  send_sta(host, port):
	# send stastics including cpu, mermery, io, and hostname by dict	
	global inte 	
	while(True):
		time.sleep(5)
		s1 = socket.socket()
		s1.connect((host, port))
		cpu_percent = psutil.cpu_percent(interval = inte)	#interval = time.sleep(interval)
		mer_percent = psutil.virtual_memory().percent
		io_radio = psutil.disk_io_counters()
		io_radio_read, io_radio_write = io_radio.read_bytes, io_radio.write_bytes
		hostname = psutil.Popen("hostname", stdout = PIPE).communicate()[0].rstrip()  #remove the end '\n'
		monitor = {"Id": hostname, "cpu": cpu_percent, "mem": mer_percent, "ior": io_radio_read, "iow": io_radio_write}
		monitor_json = json.dumps(monitor)
		s1.sendall(monitor_json)
		print "Send: " + monitor_json
		print "The speed is " + str(inte)


def  rec_sta(host, port):
	#listen to change speed of catching  stastics speed
	global inte 	
	host = "0.0.0.0"
	port =  20000			
	server = SocketServer.TCPServer((host, port), MyTCPHandler)
	print "A SocketServer is listen on " + host + ' : ' +str(port)
	server.serve_forever()
		
def  Monitor(host, port):
	host = host
	port = port
	print "Connect to " + str(host) + ": " + str(port)		
	t2 = threading.Thread(target = send_sta, args = (host, port))
	t2.start()
	t1 = threading.Thread(target = rec_sta, args = (host, port))
	t1.start()

def get_ip():
	inet = psutil.Popen("ifconfig wlan0 | g")

if  __name__ == "__main__":
	Monitor("192.168.1.112", 10001)

