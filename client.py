# Messaging Client
# @author: Matt Jadud
import socket
import sys
import time
import atexit

MSGLEN = 1

def printInstructions():
  
  print("---------Welcome to Message Server--------")
  print("These are your options:")
  print("REGISTER <username>")
  print("MESSAGE <message>")
  print("STORE <username>")
  print("COUNT <username>")
  print("DELMSG <username>")
  print("GETMSG <username>")
  print("DUMP")
  print("CLOSE")
  print("-------------------------------------------")
  print("Click Ctrl-C or type CLOSE to stop sending messages.")
  return

def exit_handler():
  print("\nStopped Client")
  
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
    
  atexit.register(exit_handler)
  host = sys.argv[1]
  port = int(sys.argv[2])
  printInstructions()
  
  send_recv("CONNECT")
  
  while True:
    try:
      selection = raw_input(">>> ")
      if selection == "CLOSE":
        send_recv(selection)
        sys.exit()
      send_recv(selection)
    except KeyboardInterrupt:
      sys.exit()