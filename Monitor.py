'''
Author: THL
Date: 20140705
Version: python 2.7
Purpose: get [hostname, cpu_percent, mer_percent, io] and transmit them to remote host
Interface:  transmit a list[], and change catching speed acooding to http
'''



import psutil
from subprocess import PIPE
import  json
import socket


inte = 60
while(True):
	cpu_percent = psutil.cpu_percent(interval = inte)
	mer_percent = psutil.virtual_memory().percent
	io_radio = psutil.disk_io_counters()
	io_radio_read, io_radio_write = io_radio.read_bytes, io_radio.write_bytes
	hostname = psutil.Popen("hostname", stdout = PIPE).communicate()[0].rstrip()
	monitor = {"hostname": hostname, "cpu_percent": cpu_percent, "mer_percent": mer_percent, "io_radio_read": io_radio_read, "io_radio_write": io_radio_write}
	monitor_json = json.dumps(monitor)

	port = 9999
	host = "192.168.1.112"
	s = socket.socket()
	s.connect((host, port))
	s.sendall(monitor_json)
	state = s.recv(1024)
	if state == "watching":
		inte = 1
	else:
		inte = 5
	print state
