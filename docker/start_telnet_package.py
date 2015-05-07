#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python; -*-

import subprocess
import atexit
import time
import sys
import os

registry = 'docker-registry.avatao.com:5000'

if len(sys.argv) != 1+2:
    print "Usage: ./start_telnet_package.py <name_of_solvable> <name_of_solution_checker>"
    sys.exit(1)

print 'Sorry about the confusing " * Running on http://0.0.0.0:5555/" line.'
print 'It\'s from the output of the Flask solution checker'
print '(and in some cases the solvable\'s too).'
print 'I\'m intentionally leaving it here, so that you can see errors.'
print

solvable = sys.argv[1]
checker = sys.argv[2]

solvable_process = None
checker_process = None
timestamp = str(int(time.time()))
def cleanup():
    print 'Killing solvable..'
    os.system('docker kill %s' % solvable+timestamp)
    print 'Killing checker..'
    os.system('docker kill %s' % checker+timestamp)
    print 'Bye'

atexit.register(cleanup)

print 'Starting solvable...' 
solvable_process = subprocess.Popen(['docker', 'run', '-p', '127.0.0.1:8888:8888', '--name', solvable+timestamp, '--rm', '--dns', '0.0.0.0', '--hostname', 'avatao', '-e', 'SECRET=secret', '%s/%s' % (registry, solvable)])
time.sleep(1)
print 'Starting checker...' 
checker_process = subprocess.Popen(['docker', 'run', '-p', '127.0.0.1:5555:5555', '--name', checker+timestamp, '--rm', '--dns', '0.0.0.0', '--link', '%s:solvable'% (solvable+timestamp), '-e', 'SECRET=secret', '--volumes-from', solvable+timestamp , '%s/%s' %  (registry, checker)])

time.sleep(1)
print
print "Solvable's telnet server (127.0.0.1:8888) port on host:"
subprocess.check_call(['docker', 'port', solvable+timestamp, '8888'])
print
print "Checker's checker (http://127.0.0.1:5555/secret) port on host:"
subprocess.check_call(['docker', 'port', checker+timestamp, '5555'])

print
print 'All up!'
print
print 'When you gracefully(Ctrl+C) terminate this script, both containers will be destroyed.' 

solvable_process.wait()
checker_process.wait()

