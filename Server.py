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
    self.sock.listen(2)

    while True:
      connection, client_address = self.sock.accept()
      threading.Thread(target=self.handle_request, args=(connection, client_address)).start()
    

  def handle_request(self,connection, client_address):
		
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
			self.handler(message, connection)
		

  def stop_server (self):
    return self.sock.close()

  def handler(self,request, conn):
  	
  	if "REGISTER" in request:
  		req, username = request.split(" ")
  		if self.MessageHandler.Register(username):
  			conn.send(b'OK\0')
  		else:
  			conn.send(b'Duplicate Username\0')
  	elif "MESSAGE" in request:
  		req = request.split(" ")[0]
  		wlen = len(request.split(" "))
  		message = ""
  		for i in range(1, wlen):
  			message += request.split(" ")[i] + " "
  		self.MessageHandler.Message(message)
  		conn.send(b'OK\0')
  	elif "STORE" in request:
  		req,username = request.split(" ")
  		if self.MessageHandler.Store(username):
  			conn.send(b'OK\0')
  		else:
  			conn.send(b'KO\0')
  	elif "COUNT" in request:
  		req,username = request.split(" ")
  		if self.MessageHandler.Count(username) != -1:
  			conn.send(b'{0}\0'.format(self.MessageHandler.Count(username)))
  		else:
  			conn.send(b'0\0')
  	elif "DELMSG" in request:
  		req,username = request.split(" ")
  		if self.MessageHandler.DelMsg(username):
  			conn.send(b'OK\0')
  		else:
  			conn.send(b'KO\0')
  	elif "GETMSG" in request:
  		req, username = request.split(" ")
  		message = self.MessageHandler.GetMsg(username)
  		if message != -1:
  			conn.send(b'Message : {0}\0'.format(message))
  		else:
  			conn.send(b'KO\0')
  	elif "DUMP" in request:
  		self.MessageHandler.Dump()
  		conn.send(b'OK\0')
			