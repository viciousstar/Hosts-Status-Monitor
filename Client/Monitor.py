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
import threading

class Monitor():
	inte = 5
	port = 10001
	host = "192.168.1.112"

	def  send_sta(self):
	# send stastics including cpu, mermery, io, and hostname by dict
		s = socket.socket()
		s.connect((self.host, self.port))
		while(True):
			cpu_percent = psutil.cpu_percent(interval = self.inte)	#interval = time.sleep(interval)
			mer_percent = psutil.virtual_memory().percent
			io_radio = psutil.disk_io_counters()
			io_radio_read, io_radio_write = io_radio.read_bytes, io_radio.write_bytes
			hostname = psutil.Popen("hostname", stdout = PIPE).communicate()[0].rstrip()  #remove the end '\n'
			monitor = {"hostname": hostname, "cpu": cpu_percent, "mem": mer_percent, "ior": io_radio_read, "iow": io_radio_write}
			monitor_json = json.dumps(monitor)
			s.sendall(monitor_json)
			print "Send: " + monitor_json
			print "The speed is " + str(self.inte)


	def  rec_sta(self):
	#listen to change speed of catching  stastics speed
		s = socket.socket()
		s.connect((self.host, self.port))
		while True:
			state = s.recv(1024)
			if state == "watching":
				self.inte = 1
				print "The changing speed is"  + str(self.inte)
			else:
				self.inte = 5

	def  __init__(self, host, port):
		self.host = host
		self.port = port
		print "Connect to " + str(host) + ": " + str(port)
		t1 = threading.Thread(target = self.rec_sta)
		t1.start()
		t2 = threading.Thread(target = self.send_sta)
		t2.start()


if  __name__ == "__main__":
	monitor  = Monitor("localhost", 10001)

