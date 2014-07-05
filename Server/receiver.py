import SocketServer
import save
class MyTCPHandler(SocketServer.BaseRequestHandler):

	def handle(self):	        
	    self.data = self.request.recv(1024).strip()
	    print "{} wrote:".format(self.client_address[0])
	    print self.data
	    save.save(self.data)
	    self.request.sendall('watching')


if __name__ == "__main__":
	HOST, PORT = "localhost", 10000
	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	print "A SocketServer is listen on " + HOST + ' : ' +str(PORT)
	server.serve_forever()
