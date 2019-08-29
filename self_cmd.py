#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import json
import threading
from ssh_remote import Remote

name = sys.argv[1]
cmd = sys.argv[2]

with open("remote.config","r") as r_config:
    r_config = r_config.read()
    r_config = json.loads(r_config)
    if name not in r_config:
        print('\033[31m{0}:is not exists\033[0m'.format(name))
        sys.exit()
    else:
        h = r_config[name]
        if "host" and "user" and "port" and "passwd" not in h:
            print('\033[41mremote.config\033[0m ' + '\033[31mnot right !\033[0m')
            sys.exit()

remote = Remote()
lock = threading.Lock()

def task(cmd,n):
    host=h['host'][n]
    port=h['port']
    user=h['user']
    passwd=h['passwd']
    rc = remote.connect(host=host,port=port,user=user,passwd=passwd)
    lock.acquire()
    print('\033[34m{0}:\033[0m'.format(host))
    remote.exec_cmd(rc,cmd)
    lock.release()

task_list = []
if __name__ == '__main__':
    for n in range(len(h['host'])):
        t1 = threading.Thread( target=task,args=(cmd,n,))
        t1.start()
        task_list.append(t1)
    for task in task_list:
        task.join()  
