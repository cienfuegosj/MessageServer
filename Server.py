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
			req, username, password, email = request.split()
			if self.MessageHandler.Register(username, password, email):
				conn.send(b'REGISTER SUCCESS\0')
			else:
				conn.send(b'REGISTER FAILED\0')
				
		elif "LOGIN" in request:
			req, username, password = request.split()
			try:
				self.MessageHandler.Login(username, password)
				conn.send(b'LOGIN SUCCESS\0')
			except:
				conn.send(b'LOGIN FAILED\0')
				
		elif "LOGOUT" in request:
			req, username, password = request.split()
			try:
				self.MessageHandler.Logout(username, password)
				conn.send(b'LOGOUT SUCCESS\0')
			except:
				conn.send(b'LOGOUT FAILED\0')
				
		elif "MESSAGE" in request:
			try:
				length_req = len(request.split())
				username, password = request.split()[length_req - 2:]
				message = " ".join(request.split()[1:length_req - 2])
				self.MessageHandler.Message(username, password, message)
				conn.send(b'OK\0')
			except:
				conn.send(b'KO\0')
			
		elif "STORE" in request:
			req,username, password = request.split()
			if self.MessageHandler.Store(username, password):
				conn.send(b'OK\0')
			else:
				conn.send(b'KO\0')
				
		elif "COUNT" in request:
			req,username, password = request.split()
			if self.MessageHandler.Count(username, password) != -1:
				conn.send(b'{0}\0'.format(self.MessageHandler.Count(username, password)))
			else:
				conn.send(b'0\0')
				
		elif "DELMSG" in request:
			req,username, password = request.split(" ")
			if self.MessageHandler.DelMsg(username, password):
				conn.send(b'OK\0')
			else:
				conn.send(b'KO\0')
				
		elif "GETMSG" in request:
			req, username, password = request.split(" ")
			message = self.MessageHandler.GetMsg(username, password)
			if message != -1:
				conn.send(b'Message : {0}\0'.format(message))
			else:
				conn.send(b'KO\0')
				
		elif "DUMP" in request:
			try:
				req, username, password = request.split()
				self.MessageHandler.Dump(username, password)
				conn.send(b'OK\0')
			except:
				conn.send(b'KO\0')
		else:
			conn.send(b'Invalid Syntax\0')