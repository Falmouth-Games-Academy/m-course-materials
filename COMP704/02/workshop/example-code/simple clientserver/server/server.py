#import the server components we need
from http.server import BaseHTTPRequestHandler, HTTPServer

#define the host name and port as variables as they are easier to find
#than digging through the code
#
#For the local loopback, i.e. client and server on the same machine, we can use localhost
#or 127.0.0.1 (home) as the address
#For connections to other machines, we need to use the URL of the host. On pc ipconfig will give you the ip address
#
#The port is the connection that the server will use and is in the range (0-65535). Normally, 8000 is fine, but
#it may not be depending on the port policy of the machine you are using

hostName = "localhost"
hostPort = 8000

#Create our server based on the BaseHTTPRequestHandler class
#
#We have to overload the do_GET and do_POST functions so we can handle them in our class

class MyServer(BaseHTTPRequestHandler):

	def do_GET(self):
		#Handle GET requests - this means that the client wants some data from the server
		print("DO GET:" + self.path);

		#This is boilerplate functional to deal with the HTTP headers
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.send_header('Access-Control-Allow-Origin', '*')
		self.end_headers()

		#This is the actual response data we are sending back
		#Note that we need to send byte data and NOT string, hence the encode()
		response_data = "The server has sent you this reply"
		self.wfile.write(response_data.encode())

	def do_POST(self):
		print("DO POST:" + self.path);
		#Handle POST requests - the client is sending us some data to process on the server

		#This is boilerplaye code to read the correct amount of data as bytes
		content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
		post_data = self.rfile.read(content_length)  # <--- Gets the data itself

		#send a response back to the client to let it know that everything is fine
		self.send_response(200)
		self.end_headers()

		response_data = "The server has sent you this reply"
		self.wfile.write(response_data.encode())

		print( "POST: ", post_data.decode())

#
#	Here's the actual run-time application
#

#create a new instance of our HTTPServer passing in the URL and port of the server
myServer = HTTPServer((hostName, hostPort), MyServer)

#Now we just run forever or until something goes wrong
try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

#Server is complete, make sure it gets shut down
myServer.server_close()
