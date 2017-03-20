import socket, threading, sys, MRA, Session, random

class ThreadedServer(object):
	CONNECTED = []
	SESSIONED = []
	
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.host, self.port))
		self.MessageHandler = MRA.MRA()
		self.unactive_UID = random.sample(range(1, 100000), 50)
		self.active_UID = []
		
		print("Server running on {0}:{1}".format(host, port))
	
	def listen(self):
		self.sock.listen(5)
		while True:
			connection, client_address = self.sock.accept()
			threading.Thread(target=self.handler, args=(connection, client_address)).start()

			
	def handler_firstlayer(self, connection, client_address):
		print("Client address: [{0}]".format(client_address))
		message = ""

		while True:
			char = connection.recv(1)
			if char == b'\0':
				break
			elif char == b'':
				break
			else:
				message += char.decode("utf-8")

		if "LOGIN" in message:
			req, username, password = message.split()
			try:
				self.MessageHandler.Login(username, password)
				connection.send(b'Logged in as {0}.\0'.format(username))
			except ValueError as e:
				connection.send(b'{0}\0'.format(e))
				
		elif "CONNECT" in message:
			UID_int = self.unactive_UID.pop()
			self.active_UID.append(UID_int)
			UID_str = "User{0}".format(UID_int)
			connection.send(b'Temporary User ID: {0}\0'.format(UID_int))
			
		elif "REGISTER" in message:
			req, username, password = message.split()
			if self.MessageHandler.Register(username, password):
				connection.send(b'OK\0')
			else:
				connection.send(b'KO\0')
				
	def handler_secondlayer(self, connection, client_address):
		
		print("Client address: [{0}]".format(client_address))
		message = ""

		while True:
			char = connection.recv(1)
			if char == b'\0':
				break
			elif char == b'':
				break
			else:
				message += char.decode("utf-8")
				
		if "MESSAGE" in message:
			req = message.split()[0]
			mensaje = " ".join(message.split()[1:])
			self.MessageHandler.Message(mensaje)
			connection.send(b'OK\0')


		elif "STORE" in message:
			req, username = message.split()
			if self.MessageHandler.Count(username) != -1:
				connection.send(b'{0}\0'.format(self.MessageHandler.Count(username)))
			else:
				connection.send(b'0\0')
				
		elif "DELMSG" in message:
			req, username = message.split()
			if self.MessageHandler.DelMsg(username):
				connection.send(b'OK\0')
			else:
				connection.send(b'KO\0')
				
		elif "GETMSG" in message:
			req, username = message.split()
			message = self.MessageHandler.GetMsg(username)
			if message != -1:
				connection.send(b'Message: {0}\0'.format(message))
			else:
				connection.send(b'KO\0')
				
		elif "DUMP" in message:
			self.MessageHandler.Dump()
			connection.send(b'OK\0')
			
		elif "LOGOUT" in message:
			connection.close()
		else:
			connection.send(b'Incorrect Syntax\0')
			
	def stop_server(self):
		return self.sock.close()
				