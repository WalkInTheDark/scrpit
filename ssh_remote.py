#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import json
import paramiko
import threading

class Remote():

    def connect(self,host,port,user,passwd):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, port, user, passwd)
        return ssh_client

    def exec_cmd(self,ssh_client,cmd):
        try:
            std_in, std_out, std_err = ssh_client.exec_command(cmd)
            for line in std_out:
                print line.strip("\n")
            ssh_client.close()
        except Exception, e:
            print e
