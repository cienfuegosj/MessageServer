# Messaging Server
# @author: Javier Cienfuegos
# @author: Emmanuel Acheampong
import socket
import sys
import atexit
from Server import ThreadedServer 

def exit_handler(Server):
  print("\nStopped Socket Server...")
  Server.stop_server()
  

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
  try:
    Server = ThreadedServer(host, port)	
    atexit.register(exit_handler, Server)
    Server.listen()
  except KeyboardInterrupt:
    exit()
  