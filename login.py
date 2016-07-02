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
[logged_in] = %s
				""" % (self.USERNAME,now)
				gitchatrc.write(content)
		else:
			import datetime
			now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
			f = open('.gitchatrc').read()
			endi = f.find('[logged')+len('[logged_in] = ')
			content = f[:endi]+now
			gitchatrc = open('.gitchatrc','w')
			gitchatrc.write(content)
			self.setUser(f.split('\n')[1])

	#method to setUsername from file
	def setUser(self,l):
		starti = len('[username] = ')
		self.USERNAME = l[starti:].strip()

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
		Owner_Repo = self.REPO_URI[starti:endi]
		gituri = 'https://api.github.com/repos/'+Owner_Repo+'/collaborators'
		from requests import get
		req = get(gituri, auth=(username,password))
		self.STATUS_CODE = req.status_code
