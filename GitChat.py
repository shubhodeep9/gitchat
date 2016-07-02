#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Shubhodeep Mukherjee
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

""" 
A simple echo client 
""" 
import os
from login import LoginController

def main():
	checkDirectory()
	login = LoginController()
	if not os.system('clear') == 0:
		os.system('cls')
	message = """ Welcome %s to the chat of %s
""" % (login.USERNAME,login.REPO_URI)
	client(login.USERNAME,message)
	

#method to check if directory is a git repo
def checkDirectory():
	try:
		open('.git/config')
	except IOError:
		raise SystemExit('Not a git repo')




def client(username,message):
	import thread
	import socket 
	import os

	host = '' 
	port = 1025 
	size = 1024 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s.connect((host,port)) 
	ls = []
	while 1:
		inp = raw_input('Enter: ')
		s.send('['+username+']:'+inp)
		os.system('clear')
		print message
		data = s.recv(size)
		ls.append(data)
		print '\n'.join(ls)

	s.close()

if __name__ == '__main__':
	main()
