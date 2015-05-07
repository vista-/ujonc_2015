#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python; -*-

from subprocess import check_call
import glob
import sys
import os

targets = None
if len(sys.argv)>=2:
    targets = sys.argv[1:]

registry = 'docker-registry.avatao.com:5000'

def build(tag, target):
    check_call(['docker', 'build', '-t', '%s/%s' % (registry,tag), target])

os.chdir(sys.path[0])

if not targets:
    build('base', 'avatao_base')

if not targets:
    targets = sorted(glob.glob('modules/*'))
    
for target in targets:
    print>> sys.stderr,  'About to build:', target
    _, tag = target.split('/')
    build(tag, target)
    
print 'All finished!'
