# Exceptions Class Library
# @author: Javier Cienfuegos & Emmanuel Acheampong
class Loggedin(Exception):
	'''
	-1 suggests that the user has logged out.
	0 suggests that the LOGIN failed. 
	1 suggests that the LOGIN  was successful. 
	'''
	pass

class Registered(Exception):
	'''
	1 suggests that the REGISTER was successful. 
	0 suggests that the REGISTER failed. 
	'''
	pass
	
class Logger(Exception):
	'''
	-1 suggests that the user has timed out in their session.
	0 suggests that the user has is not currently logged in. 
	'''
	pass

class CRCException(Exception):
	'''
	-1 suggests that there was a mismatch with the CRC, so data
	was loss which would suggest a retry/resend.
	'''
	pass