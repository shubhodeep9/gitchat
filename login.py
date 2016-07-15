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
Controller for Sign In Verification
ALGORITHM:
1. get repo link from .git/config
2. input username and password from user, hit on Git api to get collaborators with param -u "username:password"
3. Check if status ok (200) then proceed, else if status forbidden (403) SystemExit
4. save status for future use in the folder inside .gitchatrc
"""

class LoginController:
	#Class variables
	REPO_URI = ''
	STATUS_CODE = 0
	USERNAME = ''

	#Object Initiated
	def __init__(self):
		login_status = self.loginCheck()
		if not login_status:
			log_count = 3
			while log_count:
				self.readRepo()
				self.getColab()
				if self.STATUS_CODE == 200:
					break
				elif self.STATUS_CODE == 401:
					if log_count-1:
						print 'Wront Credentials'
				else:
					if log_count-1:
						print 'Not part of this repo'
				log_count = log_count - 1

			if not log_count:
				raise SystemExit('Try again later!!')
			else:
				#Logged in successfuly
				gitchatrc = open('.gitchatrc','w')
				import datetime
				now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
				content = """[status] = 200
[username] = %s
[repo_uri] = %s
[logged_in] = %s
				""" % (self.USERNAME,self.REPO_URI,now)
				gitchatrc.write(content)
		else:
			import datetime
			now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
			f = open('.gitchatrc').read()
			endi = f.find('[logged')+len('[logged_in] = ')
			content = f[:endi]+now
			gitchatrc = open('.gitchatrc','w')
			gitchatrc.write(content)
			self.setUser(f.split('\n')[1],f.split('\n')[2])

	#method to setUsername from file
	def setUser(self,l,m):
		starti = len('[username] = ')
		self.USERNAME = l[starti:].strip()
		starti = len('[repo_uri] = ')
		self.REPO_URI = m[starti:].strip()

	#method to read .gitchatrc and get status
	def loginCheck(self):
		try:
			f = open('.gitchatrc').readline()
			status = f.split('=')[1].strip()
			return status == '200'
		except IOError:
			return False



	#definition to read repo uri from  .git/config
	def readRepo(self):
		f = open('.git/config').read()
		starti = f.find('url')
		endi = f.find('fetch')
		self.REPO_URI = f[starti:endi].split('=')[1].strip()

	def getColab(self):
		from getpass import getpass
		username = raw_input('Enter your github username: ')
		self.USERNAME = username
		password = getpass('Enter your password for "'+username+'": ')
		starti = self.REPO_URI.find('github.com/')+len('github.com/')
		endi = self.REPO_URI.find('.git')
		if '.git' in self.REPO_URI:
			Owner_Repo = self.REPO_URI[starti:endi]
		else:
			Owner_Repo = self.REPO_URI[starti:]
		gituri = 'https://api.github.com/repos/'+Owner_Repo+'/collaborators'
		from requests import get
		req = get(gituri, auth=(username,password))
		self.STATUS_CODE = req.status_code
