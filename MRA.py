# Messaging Request Admin
import json
import os.path
class MRA:

        def __init__(self):
                if os.path.isfile('messages.json'):
                        with open('messages.json') as json_data:
                                d = json.load(json_data)
                else:
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
		
