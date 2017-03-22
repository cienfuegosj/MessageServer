# Messaging Client
# @author: Matt Jadud
import socket
import sys
import time
import atexit

MSGLEN = 1

class Loggedin(Exception):
	pass
class Registered(Exception):
	pass

def printInstructions():
	
	print("---------Welcome to Message Server--------")
	print("These are your options:")
	print("LOGOUT")
	print("MESSAGE")
	print("STORE")
	print("COUNT")
	print("DELMSG")
	print("GETMSG")
	print("DUMP")
	print("-------------------------------------------")
	print("Click Ctrl-C to stop sending messages.")
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
	
	if msg == "REGISTER":
		length = sock.send(bytes(" ".join([msg, username, password, email]) + "\0"))
		print ("SENT MSG: '{0}'".format(msg))
		print ("CHARACTERS SENT: [{0}]".format(length))
		return sock
	else:
		length = sock.send(bytes(" ".join([msg, username, password]) + "\0"))
		print ("SENT MSG: '{0}'".format(msg))
		print ("CHARACTERS SENT: [{0}]".format(length))
		return sock
	
def recv (sock):
	response = receive_message(sock)
	
	if response == "LOGIN SUCCESS":
		print("RESPONSE: [{0}]".format(response))
		raise Loggedin(1)
	elif response == "LOGIN FAILED":
		print("RESPONSE: [{0}]".format(response))
		raise Loggedin(0)
	elif response == "REGISTER SUCCESS":
		print("RESPONSE: [{0}]".format(response))
		raise Registered(1)
	elif response == "REGISTER FAILED":
		print("RESPONSE: [{0}]".format(response))
		raise Registered(0)
		
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
	
	global username
	global password
	global email
		
	atexit.register(exit_handler)
	host = sys.argv[1]
	port = int(sys.argv[2])
	
	# Registration or Login
	
	regornah = int(raw_input("Enter 0 if you have an account. Enter 1 if you need to register: "))
	if regornah == 0:
		while True:
			username = raw_input("Please enter your username: ")
			password = raw_input("Please enter your password: ")
			try:
				send_recv("LOGIN")
			except KeyboardInterrupt:
				sys.exit()
			except Loggedin as e:
					if e.message == 0:
						continue
					else:
						break
	else:
		username = raw_input("Create a new username: ")
		email = raw_input("Enter your e-mail: ")
		password = raw_input("Create a new password: ")
		while True:
			try:
				send_recv("REGISTER")
			except KeyboardInterrupt:
				sys.exit()
			except Registered:
				break
		while True:
			try:
				send_recv("LOGIN")
			except KeyboardInterrupt:
				sys.exit()
			except Loggedin:
				break

	printInstructions()
	
	while True:
		try:
			selection = raw_input(">>> ")
			send_recv(selection)
		except KeyboardInterrupt:
			sys.exit()
		except Loggedin as e:
			continue