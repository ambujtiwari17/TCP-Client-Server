import socket
import time
import string

hostname = '127.0.0.1'
port = 45300

clientsList= []

udpServerSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpServerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udpServerSock.bind((hostname,port))
udpServerSock.setblocking(0)
#udpServerSock.listen(10)

#socketList.append(udpServerSock)

stop = False
print "Chat server running now on port " + str(port)

while not stop:
	try:
		data, address = udpServerSock.recvfrom(2048)
		if "quit" in str(data):
			stop = True
		if address not in clientsList:
			clientsList.append(address)

		print "Time: " + time.ctime(time.time()) + " " + str(data)
		for client in clientsList:
			udpServerSock.sendto(data, client) 
	except:
		pass

udpServerSock.close()
