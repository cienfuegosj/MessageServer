# Messaging Client
# @author: Matt Jadud
import socket
import sys
import time

MSGLEN = 1

# CONTRACT
# get_message : socket -> string
# Takes a socket and loops until it receives a complete message
# from a client. Returns the string we were sent.
# No error handling whatsoever.
def receive_message (sock):
  chars = []
  try:
    while True:
      char = sock.recv(1)
      if char == b'\0':
        break
      if char == b'':
        break
      else:
        # print("Appending {0}".format(char))
        chars.append(char.decode("utf-8") )
  finally:
    return ''.join(chars)
    
def send (msg):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((host, port))
  length = sock.send(bytes(msg + "\0"))
  print ("SENT MSG: '{0}'".format(msg))
  print ("CHARACTERS SENT: [{0}]".format(length))
  return sock
  
def recv (sock):
  response = receive_message(sock)
  print("RESPONSE: [{0}]".format(response))
  sock.close()  

def send_recv (msg):
  recv(send(msg))
  

if __name__ == "__main__":
  # Check if the user provided all of the 
  # arguments. The script name counts
  # as one of the elements, so we need at 
  # least three, not fewer.
  if len(sys.argv) < 3:
    print ("Usage:")
    print (" python client.py <host> <port>")
    print (" For example:")
    print (" python client.py localhost 8888")
    print 
    sys.exit()

  host = sys.argv[1]
  port = int(sys.argv[2])
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((sys.argv[1], int(sys.argv[2])))

  send_recv("DUMP")
  send_recv("REGISTER cienfuegosj")
  send_recv("DUMP")
  send_recv("MESSAGE Hello from the other side!")
  send_recv("MESSAGE What are you doing fam?")
  send_recv("DUMP")