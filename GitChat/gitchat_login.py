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
2. input username and password from user, hit on Git api to get
collaborators with param -u "username:password"
3. Check if status ok (200) then proceed, else if status forbidden
(403) SystemExit
4. save status for future use in the folder inside .git/.gitchatrc
"""
import json


class LoginController:

    # Object Initiated
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
                # Logged in successfuly
                import datetime
                now = datetime.datetime.strftime(datetime.datetime.now(),
                                                 '%Y-%m-%d %H:%M:%S')
                content = {
                    "status": 200,
                    "username": self.USERNAME,
                    "repo_uri": self.REPO_URI,
                    "logged_in": now
                }
                with open('.git/gitchat_login.json', 'w') as login_file:
                    json.dump(content, login_file)
        else:
            import datetime
            now = datetime.datetime.strftime(datetime.datetime.now(),
                                             '%Y-%m-%d %H:%M:%S')
            with open('.git/gitchat_login.json', 'r+') as login_file:
                data = json.load(login_file)
                data["logged_in"] = now
                login_file.seek(0)
                login_file.write(json.dumps(data))
                login_file.truncate()
            self.setUser(data)

    # method to setUsername from file
    def setUser(self, data):
        self.USERNAME = data["username"]
        self.REPO_URI = data["repo_uri"]

    # method to read .gitchatrc and get status
    def loginCheck(self):
        """
        json file structure
        {
                        "status" : 200,
                        "username" : "shubhodeep9",
                        "repo_url" : "url",
                        "logged_in" : "YYYY-MM-DD HH:MM:SS"
        }
        """
        try:
            with open('.git/gitchat_login.json', 'r') as login_file:
                data = json.load(login_file)
            status = data["status"]
            return status == 200
        except IOError:
            return False

    # definition to read repo uri from  .git/config
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
        req = get(gituri, auth=(username, password))
        self.STATUS_CODE = req.status_code
