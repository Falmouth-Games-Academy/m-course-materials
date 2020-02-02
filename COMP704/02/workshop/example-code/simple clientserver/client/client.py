import http

#Create a HTTP connection to the server. Have a look at the server.py comments for host name and port below
hostName = "localhost"
hostPort = 8000
conn = http.client.HTTPConnection(hostName,hostPort)

#Setup headers for POST message types. This should map with the server code
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}


#
#	Here's the actual run-time application
#

#GET request
print("GET request")

#send a GET request with an address that can be used for anything
conn.request("GET", "index")

#pick up the response to that resquest
response = conn.getresponse()

#read the data out of the response
data = response.read()

#print the data as a decoded string
print("GET response: " + data.decode() )


#POST request
print("POST request")

#send a POST request with another address and specific data (as bytes) along with the headers object
data_to_post = "this is a test from the client"
conn.request("POST", "add_score", data_to_post.encode(), headers)

#pick up the response to that resquest
response = conn.getresponse()

#read the data out of the response
data = response.read()

#print the data as a decoded string
print("POST response: " + data.decode() )