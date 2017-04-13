# Message Request Administrator 
# authors: Emmanuel & Javier
import json, os.path, random, threading, time
import protobuf.User_pb2
from Exceptions import Logger 

class User:
	
		def __init__(self, username, password, ID, email, user=None):
			
			# Intialize the data that will be follow the protocol buffer
			if user == None:
				self.UserData = protobuf.User_pb2.User()
				# Pass in the data needed for the an individual User
		
				self.UserData.username = username
				self.UserData.password = password
				self.UserData.ID = ID
				self.UserData.email = email
				self.UserData.loggedIn = False
				self.UserData.timedOut = False
				self.UserData.t_lastActive = time.time()
				
			else:
				self.UserData = user
				self.UserData.username = username
				self.UserData.password = password
				self.UserData.ID = ID
				self.UserData.email = email
				self.UserData.loggedIn = False
				self.UserData.timedOut = False
				self.UserData.t_lastActive = time.time()
				
		def start(self):
			threading.Thread(target=self.timeOut).start()
				
		def timeOut(self):
			while abs(self.UserData.t_lastActive - time.time()) < 30:
				continue
			self.UserData.timedOut = True
			self.UserData.loggedIn = False

		def timeReset(self):
			self.UserData.t_lastActive = time.time()
			
class MRA:

		def __init__(self):
				if os.path.isfile('messages.json') and \
				os.path.isfile('users.txt'):
						self.Users =  protobuf.User_pb2.Users()
						with open('users.txt') as user_data:
								self.dict_Users = {}
								self.Users.ParseFromString(user_data.read())
								
								for user in self.Users.user:
									p_user = User(user.username, user.password,
											user.ID, user.email)
									self.dict_Users[user.username] = p_user
									
						with open('messages.json') as message_data:
								self.MBX = json.load(message_data)
								self.IMQ = []
											
						with open('__meta__idactivity.json') as meta_data:
								dict_unactive_active = json.load(meta_data)
								self.unactive_UID = dict_unactive_active["unactive"]
								self.active_UID = dict_unactive_active["active"]
								
				else:
						self.MBX = {} # User Mailbox (key = username, value = list of messages)
						self.IMQ = [] # Incoming Message Queue (list of messages inputted by an arbitrary user)
						self.dict_Users = {}
						self.Users = protobuf.User_pb2.Users()
						self.unactive_UID = random.sample(range(1, 1000000), 50)
						self.active_UID = []
						
		def Register(self, username, password, email):
				if username in self.MBX.keys() and username in self.dict_Users.keys():
						return False
				else:
						UID_int = self.unactive_UID.pop()
						self.active_UID.append(UID_int)
						self.addUser(username, password, UID_int, email)
						self.MBX[username] = []
						self.Update()
						return True
						
		def addUser(self, username, password, UID_int, email):
			user = self.Users.user.add()
			c = User(username, password, UID_int, email, user)
			self.dict_Users[username] = c
				
		def Login(self, username, password):
				if username in self.dict_Users.keys() and self.dict_Users[username].UserData.password == password and \
						self.dict_Users[username].UserData.loggedIn == True:
						raise ValueError("Already logged in")
	
				elif username in self.dict_Users.keys() and self.dict_Users[username].UserData.password == password:
						self.dict_Users[username].UserData.loggedIn = True
						self.dict_Users[username].UserData.timedOut = False
						self.dict_Users[username].timeReset()
						self.dict_Users[username].start()
			
				elif username not in self.dict_Users.keys():
						raise ValueError("Invalid Username")
				
				elif username in self.dict_Users.keys() and self.dict_Users[username].UserData.password != u'{0}'.format(password):
						raise ValueError("Invalid Password")
						
				self.Update()

		def Logout(self, username, password):
				if u'{0}'.format(username) in self.dict_Users.keys() and self.dict_Users[username].UserData.password == u'{0}'.format(password):
						self.dict_Users[username].UserData.loggedIn = False
						self.dict_Users[username].UserData.timedOut = False
				elif self.dict_Users[username].UserData.password != password:
						raise ValueError("Invalid Password")
						
				self.Update()

		def Message(self, username, password, message):
			
				# Check whether the client has passed the time limit for an active session
				# Otherwise, reset the time active time and complete the client's command
				
				if not self.dict_Users[username].UserData.timedOut:
					self.dict_Users[username].timeReset()
				else:
					 raise Logger(-1)
				
				if username in self.dict_Users.keys() and self.dict_Users[username].UserData.password == u'{0}'.format(password):
					if self.dict_Users[username].UserData.loggedIn == True:
						self.IMQ.append(message)
					else:
						raise Logger(0)

		def Store(self, username, password):
			
				if not self.dict_Users[username].UserData.timedOut:
					self.dict_Users[username].timeReset()
				else:
					 raise Logger(-1)
			
				if username in self.MBX.keys() and len(self.IMQ) > 0 and \
				username in self.dict_Users.keys() and self.dict_Users[username].UserData.password == password and \
				self.dict_Users[username].UserData.loggedIn == True:
						self.MBX[username].append(self.IMQ.pop())
						self.Update()
						return True
				else:
						return False
			
		def Count(self, username, password):
			
				if not self.dict_Users[username].UserData.timedOut:
					self.dict_Users[username].timeReset()
				else:
					 raise Logger(-1)
			
				if username in self.MBX.keys() and username in self.dict_Users.keys() and \
				self.dict_Users[username].UserData.password == password and \
				self.dict_Users[username].UserData.loggedIn == True:
						return len(self.MBX[username])
				else:
						return -1
						
			
		def DelMsg(self, username, password):
			
				if not self.dict_Users[username].UserData.timedOut:
					self.dict_Users[username].timeReset()
				else:
					 raise Logger(-1)
			
				if username in self.MBX.keys() and len(self.MBX[username]) > 0 and \
				self.dict_Users[username].UserData.password == password and \
				self.dict_Users[username].UserData.loggedIn == True:
						del self.MBX[username][0]
						return True
				else:
						return False
			
		def GetMsg(self, username, password):
			
				if not self.dict_Users[username].UserData.timedOut:
					self.dict_Users[username].timeReset()
				else:
					 raise Logger(-1)
			
				if username in self.MBX.keys() and len(self.MBX[username]) > 0 and \
				self.dict_Users[username].UserData.password == password and \
				self.dict_Users[username].UserData.loggedIn == True:
						return self.MBX[username][0]
				else:
						return -1
		def Dump(self, username, password):
			
				if not self.dict_Users[username].UserData.timedOut:
					self.dict_Users[username].timeReset()
				else:
					 raise Logger(-1)
			
				if self.dict_Users[username].UserData.password == password and \
				self.dict_Users[username].UserData.loggedIn == True:
						print("Current IMQ: {0}".format(self.IMQ))
						print("Current MBX: {0}".format(self.MBX))
				else:
						raise Logger(0)
		def Update(self):
				with open('messages.json', 'w') as outfile:
						json.dump(self.MBX,outfile)
				with open("__meta__idactivity.json", 'w') as outfile:
						json.dump({"unactive": self.unactive_UID, "active": self.active_UID}, outfile)
				with open('users.txt', 'w') as outfile:
						outfile.write(self.Users.SerializeToString())
			