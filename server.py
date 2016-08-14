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
-------------------------------------------------------------------------------
The server code that distributes one message from one socket to another
according to the repository the chat is destined.
Using dictionary structure
-------------------------------------------------------------------------------
clients = {
    "some":[]
}
DB
chat_db :=
{
    message: "",
    repo:"",
    users:[
    "",
    ""
    ]
}

repo_db :=
{
    repo:"",
    users:[

    ]
}
"""
import re
import pymongo
from twisted.protocols import basic

db = pymongo.MongoClient().gitchat

class GitChat(basic.LineReceiver):
    def dataReceived(self, line):
        if line.split(' ')[0] == 'first':
            try:
                first,repo,username = line.split(' ')
                ct = 0
                repo_db = db.repo_db.find_one({'repo':re.compile(repo,re.IGNORECASE)})
                if not bool(repo_db):
                    db.repo_db.insert({'repo':repo,'users':[username]})
                else:
                    if username not in repo_db['users']:
                        db.repo_db.update({'_id':repo_db['_id']},{'$push':{'users':username}})
                for i in self.factory.clients[repo]:
                    if i == self:
                        ct = ct + 1
                        break
                if ct==0:
                    self.factory.clients[repo].append(self)
                self.factory.client_to_ref[username] = self
                # DB fetch
                result = db.chat_db.find({'repo':re.compile(repo,re.IGNORECASE)})
                for i in result:
                    if username in i['users']:
                        self.transport.write(str(i['message']+' '+line.split(' ')[1]+'\n'))
                db.chat_db.update({'repo':re.compile(repo,re.IGNORECASE)},{'$pull':{'users':username}})
            except KeyError:
                self.factory.clients[line.split(' ')[1]] = [self]
        elif line.split(' ')[0] == 'exit':
            user = line.split(' ')[1]
            repo = line.split(' ')[2]
            self.factory.clients[repo].remove(self)
            self.factory.client_to_ref.remove(user)
        else:
            repo = line.split(' ')
            repo = repo[len(repo)-1]
            read_clients = []
            for c in self.factory.clients[repo]:
                c.transport.write(line)
                read_clients.append(c)
            self.message(line,read_clients)

    def message(self, message, read_clients):
        content = message.split(' ')
        repo = content[len(content)-1]
        repo_users = db.repo_db.find_one({'repo':re.compile(repo,re.IGNORECASE)})['users']
        real_read_clients = []
        for i in read_clients:
            real_read_clients.append(self.factory.client_to_ref.keys()[self.factory.client_to_ref.values().index(i)])
        repo_to_go = set(repo_users) - set(real_read_clients)
        repo_to_go = list(repo_to_go)
        db.chat_db.insert({'repo':repo,
                           'message':' '.join(content[:len(content)-1]),'users':repo_to_go})


from twisted.internet import protocol
from twisted.application import service, internet

factory = protocol.ServerFactory()
factory.protocol = GitChat
factory.clients = {}
factory.client_to_ref = {}

application = service.Application("chatserver")
internet.TCPServer(1025, factory).setServiceParent(application)
