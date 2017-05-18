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
The application focuses on making development easy for developers using
github.com. Kindly follow method docstrings to understand the flow.
To contribute, please follow PEP8, and do notify if the code doesn't follow
PEP8.
"""
import os
import signal
from gitchat_login import LoginController
from gitchat_ui import *

__version__ = '0.1.0'


def main():
    checkDirectory()
    login = LoginController()
    if not os.system('clear') == 0:
        os.system('cls')
    Execute(login)


# method to check if directory is a git repo
def checkDirectory():
    try:
        open('.git/config')
    except IOError:
        raise SystemExit('Not a git repo')


# Method used to prevent Ctrl^C program exit
def nothing(signum, frame):
    pass


if __name__ == '__main__':
    signal.signal(signal.SIGINT, nothing)
    main()
