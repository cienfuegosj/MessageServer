import sys
import socket

class Session:
  
  numberofSessions = 0
  
  def __init__(self,connection,client_address):
    self.sessionID = numberofSessions + 1
    self.connection = connection
    self.client_address = client_address
    print("Connection is of type ".format(type(self.connection)))
   