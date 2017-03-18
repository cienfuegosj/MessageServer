# Messaging Request Admin

class MRA:

	def __init__(self):
		self.MBX = {} # User Mailbox
		self.IMQ = [] # Incoming Message Queue
		
	def Register(self, username):
		if username in self.MBX.keys():
			return False
		else:
			self.MBX[username] = []
			return True
		
	def Message(self, message):
		self.IMQ.append(message)
	
	def Store(self, username):
		if username in self.MBX.keys() and len(self.IMQ) != 0:
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
		if username in self.MBX.keys() and len(self.MBX[username]) != 0:
			return self.MBX[username][0]
		else:
			return -1
	
	def Dump(self):
		print("Current IMQ: {0}".format(self.IMQ))
		print("Current MBX: {0}".format(self.MBX))
		
