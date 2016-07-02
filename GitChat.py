#!/usr/bin/env python 

""" 
A simple echo client 
""" 

from login import LoginController

def main():
	login = LoginController()
	print login.USERNAME

# import socket 

# host = '' 
# port = 65535 
# size = 1024 
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# s.connect((host,port)) 
# while 1:
# 	inp = raw_input('Enter:')
# 	s.send(inp) 
# 	data = s.recv(size) 
# 	if inp == 'BYE':
# 		s.close()
# 		break
	
# 	print 'Received:', data

if __name__ == '__main__':
	main()
