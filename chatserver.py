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
#		print address[1] 
		if address not in clientsList:
			clientsList.append(address)
			#print address + " joined the chat"
		for client in clientsList:
			if client[1] != address[1]:
				udpServerSock.sendto(data, client) 
		print "Time: " + time.ctime(time.time()) + " " + str(data)
		if "q" in str(data):
			stop = True
			for clients in clientsList:
				if client[1] != address[1]:
					udpServerSock.sendto(data.split()[0] + " has exit the room", client)	
				clientList.remove(address)
				
#		if address not in clientsList:
#			clientsList.append(address)

	#	print "Time: " + time.ctime(time.time()) + " " + str(data)
		#for client in clientsList:
		#	udpServerSock.sendto(data, client) 
	except:
		pass

udpServerSock.close()
