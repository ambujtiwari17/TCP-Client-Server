import socket
import time
import threading
import sys

threadLock = threading.Lock()
exit = False

def receiveMsg(name, sock):
	while not exit:
		try:
			threadLock.acquire()
			while True:
				data, addr = sock.recvfrom(2048)
				print str(data)
		except:
			pass
		finally:
			threadLock.release()

host = '127.0.0.1'
port = 0

server = ('127.0.0.1', 45300)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

#s.getsockname[0]
recvThread = threading.Thread(target=receiveMsg, args=("RecThread", s))
recvThread.start()

alias = raw_input("Name: ")
#message = raw_input(alias + "->")
message=''
while message !='q':
	
	threadLock.acquire()
	message = raw_input(alias + "-> ")
	threadLock.release()
	if message != '':
		s.sendto(alias + " says " + message, server)
	'''threadLock.acquire()
	message = raw_input(alias + "-> ")
	threadLock.release()'''
	time.sleep(0.5)

if message == 'q':
	#print alias + " has now exited"
	s.sendto(alias + " has now exited", server)	
	print alias + " has now exited"

shut = True
recvThread.join()
s.close()
