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
clients = {
    "some":[]
}

DB
{
    message: "",
    repo:"",
}
"""

import pymongo
from twisted.protocols import basic

db = pymongo.MongoClient().gitchat

class GitChat(basic.LineReceiver):
    def dataReceived(self, line):
        if line.split(' ')[0] == 'first':
            try:
                ct = 0
                for i in self.factory.clients[line.split(' ')[1]]:
                    if i == self:
                        ct = ct + 1
                        break
                if ct==0:
                    self.factory.clients[line.split(' ')[1]].append(self)

                # DB fetch
                result = db.chat_db.find({'repo':line.split(' ')[1]})
                for i in result:
                    self.transport.write(str(i['message']+' '+line.split(' ')[1]+'\n'))
            except KeyError:
                self.factory.clients[line.split(' ')[1]] = [self]
        elif line.split(' ')[0] == 'exit':
            user = line.split(' ')[1]
            repo = line.split(' ')[2]
            self.factory.clients[repo].remove(self)
        else:
            repo = line.split(' ')
            repo = repo[len(repo)-1]
            for c in self.factory.clients[repo]:
                c.transport.write(line)
            self.message(line)

    def message(self, message):
        content = message.split(' ')
        db.chat_db.insert({'repo':content[len(content)-1],'message':' '.join(content[:len(content)-1])})


from twisted.internet import protocol
from twisted.application import service, internet

factory = protocol.ServerFactory()
factory.protocol = GitChat
factory.clients = {}

application = service.Application("chatserver")
internet.TCPServer(1025, factory).setServiceParent(application)