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
        print(name,u':is not exists')
        sys.exit()

h = r_config[name]
remote = Remote()
lock = threading.Lock()

def task(cmd,n):
    host=h['host'][n]
    port=h['port']
    user=h['user']
    passwd=h['passwd']
    rc = remote.connect(host=host,port=port,user=user,passwd=passwd)
    lock.acquire()
    print(host,u':')
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
