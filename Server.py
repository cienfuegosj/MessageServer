# Backend Server
# @authors: Emmanuel & Javier
import socket, threading, sys, MRA
from pycrc.crc_algorithms import Crc
	
class ThreadedServer(object):
	
	def __init__(self, host, port):
		
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.host, self.port))
		self.MessageHandler = MRA.MRA()
		self.crc = Crc(width=16, poly = 0x8005,
        	reflect_in = True, xor_in = 0x0000,
        	reflect_out = True, xor_out = 0x0000)
        	
		print("Running server on host [{0}] and port [{1}]".format(host, port))

	def listen(self):
		'''
		Activates the listening method of the socket and each client is handled via
		another worker thread such that we can handle messages from other clients. 
		'''
		
		self.sock.listen(2)

		while True:
			connection, client_address = self.sock.accept()
			threading.Thread(target=self.handle_request, args=(connection, client_address)).start()
		
	def generateCRC(self, message):
		'''
		message is a string that contains the entire message that we want to send
		to the client. The code will be attached the message we want to send back to the
		the client. We also use this is to check whether a receiving CRC code is equal to
		our computed CRC code. 
		'''
		
		code = self.crc.bit_by_bit(str(message))
		return hex(code)
		
	def handle_request(self,connection, client_address):
		'''
		connection is the client socket which sent a buffer to the server socket. 
		client_address is the ip address along with a tag that identifies each client request. 
		The message is built by continuously receiving characters until the null or \0 character
		is reached.
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
			self.handler(message, connection)
		

	def stop_server (self):
		#FIXME For all users that are logged in, log them off manually. 
		return self.sock.close()

	def handler(self, request, conn):
		'''
		request is the message being sent by the client socket.
		conn is the connection socket from the client. 
		Each command is analyzed and passed into the message handler. 
		'''
		
		if "REGISTER" in request:
			code, req, username, password, email = request.split()
			
			# Check if CRC code is equal to the computed CRC
			if code == self.generateCRC(" ".join(request.split()[1:])):
				pass
			else:
				conn.send(b'RETRY\0')
				return
			
			if self.MessageHandler.Register(username, password, email):
				conn.send(b'REGISTER SUCCESS\0')
			else:
				conn.send(b'REGISTER FAILED\0')
				
		elif "LOGIN" in request:
			code, req, username, password = request.split()
			
			# Check if CRC code is equal to the computed CRC
			if code == self.generateCRC(" ".join(request.split()[1:])):
				pass
			else:
				conn.send(b'RETRY\0')	
				return
			try:
				self.MessageHandler.Login(username, password)
				conn.send(b'LOGIN SUCCESS\0')
			except:
				conn.send(b'LOGIN FAILED\0')
				
		elif "LOGOUT" in request:
			code, req, username, password = request.split()
			
			# Check if CRC code is equal to the computed CRC
			if code == self.generateCRC(" ".join(request.split()[1:])):
				pass
			else:
				conn.send(b'RETRY\0')
				return
				
			try:
				self.MessageHandler.Logout(username, password)
				conn.send(b'LOGOUT SUCCESS\0')
			except:
				conn.send(b'LOGOUT FAILED\0')
				
		elif "MESSAGE" in request:
			
			length_req = len(request.split())
			code = request.split()[0]
			username, password = request.split()[length_req - 2:]
			message = " ".join(request.split()[2:length_req - 2])
			
			# Check if CRC code is equal to the computed CRC
			if code == self.generateCRC(" ".join(request.split()[1:])):
				pass
			else:
				conn.send(b'RETRY\0')
				return
				
			try:
				self.MessageHandler.Message(username, password, message)
				conn.send(b'OK\0')
			except Exception as e:
				if e.message == 0:
					conn.send(b'KO\0')
				elif e.message == -1:
					conn.send(b'LOGGED OUT\0')
			
		elif "STORE" in request:
			
			code, req,username, password = request.split()
			
			# Check if CRC code is equal to the computed CRC
			if code == self.generateCRC(" ".join(request.split()[1:])):
				pass
			else:
				conn.send(b'RETRY\0')
				return
				
			try:
				if self.MessageHandler.Store(username, password):
					conn.send(b'OK\0')
				else:
					conn.send(b'KO\0')
			except:
				conn.send(b'LOGGED OUT\0')
				
		elif "COUNT" in request:
			
			code, req,username, password = request.split()
			
			# Check if CRC code is equal to the computed CRC
			if code == self.generateCRC(" ".join(request.split()[1:])):
				pass
			else:
				conn.send(b'RETRY\0')
				return
				
			try:
				if self.MessageHandler.Count(username, password) != -1:
					conn.send(b'{0}\0'.format(self.MessageHandler.Count(username, password)))
				else:
					conn.send(b'0\0')
			except:
				conn.send(b'LOGGED OUT\0')
				
		elif "DELMSG" in request:
			
			code, req, username, password = request.split()
			
			# Check if CRC code is equal to the computed CRC
			if code == self.generateCRC(" ".join(request.split()[1:])):
				pass
			else:
				conn.send(b'RETRY\0')
				return
			
			try:
				if self.MessageHandler.DelMsg(username, password):
					conn.send(b'OK\0')
				else:
					conn.send(b'KO\0')
			except:
				conn.send(b'LOGGED OUT\0')
				
		elif "GETMSG" in request:
			
			code, req, username, password = request.split(" ")
			
			# Check if CRC code is equal to the computed CRC
			if code == self.generateCRC(" ".join(request.split()[1:])):
				pass
			else:
				conn.send(b'RETRY\0')
				return
				
			try:
				message = self.MessageHandler.GetMsg(username, password)
				if message != -1:
					conn.send(b'Message : {0}\0'.format(message))
				else:
					conn.send(b'KO\0')
			except:
				conn.send(b'LOGGED OUT\0')
				
		elif "DUMP" in request:
			
			code, req, username, password = request.split()
			
			# Check if CRC code is equal to the computed CRC
			if code == self.generateCRC(" ".join(request.split()[1:])):
				pass
			else:
				conn.send(b'RETRY\0')
				return
				
			try:
				self.MessageHandler.Dump(username, password)
				conn.send(b'OK\0')
			except Exception as e:
				if e.message == 0:
					conn.send(b'KO\0')
				elif e.message == -1:
					conn.send(b'LOGGED OUT\0')
		else:
			conn.send(b'Invalid Syntax\0')