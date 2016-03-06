import socket, select, re
 
#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :

                socket.close()
                CONNECTION_LIST.remove(socket)

def getSocket( idd):
  return CONNECTION_LIST[idd]

#function to send message to specific client using client id
def single_client (sock , message , idd):
  socket = getSocket ( idd )
  if socket :
    socket.send(message)
  else:
    print "Message not sent"
 
if __name__ == "__main__":
     
    # List to keep track of socket attributes
    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    PORT = 6575
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
    id2 = {}
    idd = 1
    while 1:
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client %s connected , id assigned is %d" % (addr[0] , idd)
                #print sock.getpeername()
		#id2[key] = idd  
		#print id2
		id2[addr[1]] = idd
		
                broadcast_data(sockfd, "New client entered with id = %d\n" %idd)
                idd += 1
             
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if str.startswith(data , "-umsgto"):
                      #print "got single client message request"
                      eid = re.findall("[0-9]+" , data)
                      #print eid
                      eid = eid[0]
                      print "single client message sent with id = %d" %int(eid)
		      key = sock.getpeername()[1]
                      single_client( sock , "Unicast message received :: Client #" + str(id2[key]) + " -> " + data[8:] , int(eid))
                   
		    elif data:
			#print (str(id2))            
		       if str.startswith(data, "-bmsg"):
			  key = sock.getpeername()[1]          			
			  st = 'Broadcast message received :: Client #' + str(id2[key]) +  ' -> '  
                          broadcast_data(sock, st + data[5:])    
                              
                       if data == "exit\n":
		          broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                          print "Client (%s, %s) is offline" % addr
                          sock.close()
                          CONNECTION_LIST.remove(sock)
                      #continue
     	        except:
		     print "Connection problem. Disconnecting socket..."
		     #sock.close()
		     CONNECTION_LIST.remove(sock)
		     continue
    server_socket.close()
