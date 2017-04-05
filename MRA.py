# Messaging Request Admin
import json, os.path, random, threading, time
from Exceptions import Logger 

class User:
	
		def __init__(self, username, password, ID, email):
				self.username = username
				self.password = password
				self.ID = ID
				self.email = email
				self.loggedIn = False		
				self.timedOut = False
				self.t_lastActive = time.time()
				
		def start(self):
			threading.Thread(target=self.timeOut).start()
				
		def timeOut(self):
			while abs(self.t_lastActive - time.time()) < 30:
				continue
			self.timedOut = True
			self.loggedIn = False

		def timeReset(self):
			self.t_lastActive = time.time()
			
class MRA:

		def __init__(self):
				if os.path.isfile('messages.json') and \
				os.path.isfile('users.json'):
						with open('messages.json') as message_data:
								self.MBX = json.load(message_data)
								self.IMQ = []
								
						with open('users.json') as user_data:
								self.Users = {}
								u = json.load(user_data)
								
								# Recreate User objects to restore Users
								for user in u.keys():
									p_user = User(u[user][u'username'], u[user][u'password'], u[user][u'ID'], u[user][u'email'])
									self.Users[u[user][u'username']] = p_user
									
						with open('__meta__idactivity.json') as meta_data:
								dict_unactive_active = json.load(meta_data)
								self.unactive_UID = dict_unactive_active["unactive"]
								self.active_UID = dict_unactive_active["active"]
								
				else:
						self.MBX = {} # User Mailbox
						self.IMQ = [] # Incoming Message Queue
						self.Users = {}
						self.unactive_UID = random.sample(range(1, 1000000), 50)
						self.active_UID = []
						
		def Register(self, username, password, email):
				if username in self.MBX.keys() and username in self.Users.keys():
						return False
				else:
						UID_int = self.unactive_UID.pop()
						self.active_UID.append(UID_int)
						self.Users[username] = User(username, password, UID_int, email)
						self.MBX[username] = []
						self.Update()
						return True
				
		def Login(self, username, password):
				if username in self.Users.keys() and self.Users[username].password == password and \
						self.Users[username].loggedIn == True:
						raise ValueError("Already logged in")
	
				elif username in self.Users.keys() and self.Users[username].password == password:
						self.Users[username].loggedIn = True
						self.Users[username].timedOut = False
						self.Users[username].timeReset()
						self.Users[username].start()
			
				elif username not in self.Users.keys():
						raise ValueError("Invalid Username")
				
				elif username in self.Users.keys() and self.Users[username].password != u'{0}'.format(password):
						raise ValueError("Invalid Password")
						
				self.Update()

		def Logout(self, username, password):
				if u'{0}'.format(username) in self.Users.keys() and self.Users[username].password == u'{0}'.format(password):
						self.Users[username].loggedIn = False
						self.Users[username].timedOut = False
				elif self.Users[username].password != password:
						raise ValueError("Invalid Password")
						
				self.Update()

		def Message(self, username, password, message):
			
				# Check whether the client has passed the time limit for an active session
				# Otherwise, reset the time active time and complete the client's command
				
				if not self.Users[username].timedOut:
					self.Users[username].timeReset()
				else:
					 raise Logger(-1)
				
				if username in self.Users.keys() and self.Users[username].password == u'{0}'.format(password):
					if self.Users[username].loggedIn == True:
						self.IMQ.append(message)
					else:
						raise Logger(0)

		def Store(self, username, password):
			
				if not self.Users[username].timedOut:
					self.Users[username].timeReset()
				else:
					 raise Logger(-1)
			
				if username in self.MBX.keys() and len(self.IMQ) > 0 and \
				username in self.Users.keys() and self.Users[username].password == password and \
				self.Users[username].loggedIn == True:
						self.MBX[username].append(self.IMQ.pop())
						self.Update()
						return True
				else:
						return False
			
		def Count(self, username, password):
			
				if not self.Users[username].timedOut:
					self.Users[username].timeReset()
				else:
					 raise Logger(-1)
			
				if username in self.MBX.keys() and username in self.Users.keys() and \
				self.Users[username].password == password and \
				self.Users[username].loggedIn == True:
						return len(self.MBX[username])
				else:
						return -1
						
			
		def DelMsg(self, username, password):
			
				if not self.Users[username].timedOut:
					self.Users[username].timeReset()
				else:
					 raise Logger(-1)
			
				if username in self.MBX.keys() and len(self.MBX[username]) > 0 and \
				self.Users[username].password == password and \
				self.Users[username].loggedIn == True:
						del self.MBX[username][0]
						return True
				else:
						return False
			
		def GetMsg(self, username, password):
			
				if not self.Users[username].timedOut:
					self.Users[username].timeReset()
				else:
					 raise Logger(-1)
			
				if username in self.MBX.keys() and len(self.MBX[username]) > 0 and \
				self.Users[username].password == password and \
				self.Users[username].loggedIn == True:
						return self.MBX[username][0]
				else:
						return -1
		def Dump(self, username, password):
			
				if not self.Users[username].timedOut:
					self.Users[username].timeReset()
				else:
					 raise Logger(-1)
			
				if self.Users[username].password == password and \
				self.Users[username].loggedIn == True:
						print("Current IMQ: {0}".format(self.IMQ))
						print("Current MBX: {0}".format(self.MBX))
				else:
						raise Logger(0)
		def Update(self):
				with open('messages.json', 'w') as outfile:
						json.dump(self.MBX,outfile)
				with open("__meta__idactivity.json", 'w') as outfile:
						json.dump({"unactive": self.unactive_UID, "active": self.active_UID}, outfile)
				with open('users.json', 'w') as outfile:
						json.dump({user: self.Users[user].__dict__ for user in self.Users.keys()} ,outfile)
		
