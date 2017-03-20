# Messaging Request Admin

class MRA:

	def __init__(self):
		self.MBX = {} # User Mailbox
		self.IMQ = [] # Incoming Message Queue
		self.Users = {}
		
	def Login(self, username, password):
		if username in self.Users.keys() and password == self.Users[username]:
			return True
		elif username not in self.Users.keys():
			raise ValueError("Username not found in database")
		elif username in self.Users.keys() and password != self.Users[username]:
			raise ValueError("Incorrect password. Try again")
			
	def Register(self, username, password):
		if username in self.MBX.keys():
			return False
		else:
			self.Users[username] = password
			self.MBX[username] = []
			return True
		
	def Message(self, message):
		self.IMQ.append(message)

	def Store(self, username):
		if username in self.MBX.keys() and len(self.IMQ) > 0:
			self.MBX[username].append(self.IMQ.pop())
			return True
		else:
			return False
			
	def Count(self, username):
		if username in self.MBX.keys():
			return len(self.MBX[username])
		else:
			return -1
			
	def DelMsg(self, username):
		if username in self.MBX.keys() and len(self.MBX[username]) > 0:
			del self.MBX[username][0]
			return True
		else:
			return False
			
	def GetMsg(self, username):
		if username in self.MBX.keys() and len(self.MBX[username]) > 0:
			return self.MBX[username][0]
		else:
			return -1
	
	def Dump(self):
		print("Current IMQ: {0}".format(self.IMQ))
		print("Current MBX: {0}".format(self.MBX))
		
