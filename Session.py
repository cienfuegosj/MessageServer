import sys
import socket
import threading
import time

class Session:
  
  def __init__(self):
    self.sessionID = 0
    self.connection = None
    self.client_address = None
    self.userID = None
    
  def validate(self, connection, client_address, sessID):
    self.connection = connection
    self.client_address = client_address
    self.sessionID = sessID