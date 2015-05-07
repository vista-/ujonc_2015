#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python; -*-


# PUSH script
# This assumes a valid repository lives at docker-repository.avatao.com:5000.
#
# If you are using the fig configuration, then you already have a valid
#    repository for testing running at 127.0.0.1:5000, and you should add the
#    following line to /etc/hosts to just make it work:
#    127.0.0.1	docker-repository.avatao.com

from subprocess import check_call
import glob
import sys
import os

targets = None
if len(sys.argv)>=2:
    targets = sys.argv[1:]

registry = 'docker-registry.avatao.com:5000'

def push(tag):
    check_call(['docker', 'push', '%s/%s' % (registry, tag)])

os.chdir(sys.path[0])

if not targets:
    push('base')

if not targets:
    targets = sorted(glob.glob('modules/*'))

for target in targets:
    print 'About to push:', target
    _, tag = target.split('/')
    push(tag)

print 'All finished!'
