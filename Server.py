import socket
import threading
import sys
import MRA
import Session

class ThreadedServer(object):
  
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind((self.host, self.port))
    self.MessageHandler = MRA.MRA()
    print("Running server on host [{0}] and port [{1}]".format(host, port))

  def listen(self):
    self.sock.listen(5)

    while True:
			'''Get a new connection and save the session'''
      connection, client_address = self.sock.accept()
			sess = Session.Session(connection, client_address)
			'''While the session has not timed out, handle its requests'''
			while !(sess.timedOut()):
      	threading.Thread(target=self.handle_request, args=(connection, client_address)).start()
    
    serversock.stop_server()
  

  def handle_request(self,connection, client_address):
		'''
		handle_requests creates the message using the byte stream sent by the client. 
		'''

    print("Client address: [{0}]".format(client_address))
    message = ""
    try:
  	  while True:
		    char = connection.recv(1)
		    if char == b'\0':
			    break
		    elif char == b'':
			    break
		    else:
			    message += char.decode("utf-8")
    finally:
			# Send it to the handler to handle message
		   if self.handler(message, connection) == False:
					return False

  def stop_server (self):
    return self.sock.close()

  def handler(self,request, conn):

	  if "REGISTER" in request:
		  req,username = request.split(" ")
		  if self.MessageHandler.Register(username):
		    conn.send(b'OK\0')
				return True
     	  	  else:
       		    conn.send(b'Duplicate Username\0')
							return True
		
	  elif "MESSAGE" in request:
		  req = request.split(" ")[0]
		  wlen = len(request.split(" "))
		  message = ""
		  for i in range(1, wlen):
			  message = message + request.split(" ")[i] + " "
		
		  self.MessageHandler.Message(message)
		  conn.send(b'OK\0')
			return True

	
	  elif "STORE" in request:
		  req,username = request.split(" ")
		  if self.MessageHandler.Store(username):
			  conn.send(b'OK\0')
				return True
		  else:
			  conn.send(b'KO\0')
				return True
			
	  elif "COUNT" in request:
		  req,username = request.split(" ")
		  msg_count = self.MessageHandler.Count(username)
		  if msg_count != -1:
			  conn.send(b"COUNTED {0}\0".format(msg_count))
				return True
		  else:
			  conn.send(b'KO\0')
				return True
			
	  elif "DELMSG" in request:
		  req, username = request.split(" ")
		  if self.MessageHandler.DelMsg(username):
			  conn.send(b'OK\0')
				return True
		  else:
			  conn.send(b'KO\0')
				return True

	  elif "GETMSG" in request:
		  req, username = request.split(" ")
		  message = self.MessageHandler.GetMsg(username)
		  if message != -1:
			  conn.send(b'Message: {0}\0'.format(message))
				return True
		  else:
			  conn.send(b'KO\0')
				return True
			
	  elif "DUMP" in request:
		  self.MessageHandler.Dump()
		  conn.send(b'OK\0')
			return True
		elif "CLOSE" in request:
			conn.close()
			return False
