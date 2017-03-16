# Messaging Server
import socket
import sys
from Server import ThreadedServer 

if __name__ == "__main__":
	# Check if the user provided all of the 
  # arguments. The script name counts
  # as one of the elements, so we need at 
  # least three, not fewer.
  if len(sys.argv) < 3:
    print ("Usage: ")
    print (" python server.py <host> <port>")
    print (" e.g. python server.py localhost 8888")
    print 
    sys.exit()

  host = sys.argv[1]
  port = int(sys.argv[2])
  Server = ThreadedServer(host, port)	
  Server.listen()