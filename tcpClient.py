import socket, select, string, sys
 
def prompt() :
    sys.stdout.write('-> ')
    sys.stdout.flush()
 
#main function
if __name__ == "__main__":
     
     
    host = raw_input("Enter the IP address: ")
    port = 6575
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. Start sending messages\n'
    print 'Instructions for communication: There are two modes of communication offered by the service.\n'
    print '\t1.) Unicast messaging : Two clients connected to the server can have a private conversation. To initiate:'
    print '\tMessage format :  type -umsgto followed by client number to which you would want to send your message to followed by your message.'
    print '\tFor e.g : -umsgto2<message> sends the desired message to client #2'
    print '\t2.) Broadcast messaging : A given client can broadcast its message to all the clients connected to the server. To initiate:'
    print '\tMessage format :  type -bmsg followed by your message.'
    print '\tFor e.g : -bmsg<message> sends the desired message to all connected clients'

    prompt()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
        
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print "\nDisconnected from chat server"
                    sys.exit()
                else :
                    #print data
                    #if str.startswith("/msg"):
			#data
		    sys.stdout.write(data)
                    prompt()
             
            #user entered a message
            else :
                msg = sys.stdin.readline()
                s.send(msg)
                prompt()
                
