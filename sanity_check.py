#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- mode: python; -*-

import os
import re
import sys
from datetime import datetime
from glob import glob


EMAIL_REGEX = r'^[^\s@]+@[^\s]+\.[^\s]+$'
EMAIL_RE = re.compile(EMAIL_REGEX)


def trim_read(path):
    return open(path, encoding='utf-8-sig', errors='replace').read().strip()


class UuidManager(object):
    _uuids_seen = {}

    def uuid_seen(self, uuid, type_, path):
        if uuid in self._uuids_seen:
            print('UUID (%s) collision - you copied uuid.txt' % uuid)
            print('Existing: %s, Conflicting: %s' % (self._uuids_seen[uuid][1], path))
            sys.exit(1)
        self._uuids_seen[uuid] = (type_, path)

    def check_uuid_existence(self, uuid, type_):
        if uuid not in self._uuids_seen:
            print('UUID (%s) referenced but does not exist' % uuid)
            sys.exit(1)
        if self._uuids_seen[uuid][0] != type_:
            print('UUID (%s) type mismatch: %s != %s' % (uuid, self._uuids_seen[uuid][0], type_))
            sys.exit(1)

    def check_uuid(self, type_, path):
        uuid = trim_read(os.path.join(path, 'uuid.txt'))
        self.uuid_seen(uuid, type_, path)


def check_files(path, filenames):
    error = False
    for filename in filenames:
        fullpath = os.path.join(path, filename)
        if not os.path.isfile(fullpath):
            print('Missing: %s' % fullpath)
            error = True
    if error:
        sys.exit(1)


def check_recommendations(path):
    error = False
    recommendations = trim_read(os.path.join(path, 'recommendations.txt'))
    for line in recommendations.split('\n'):
        line = line.strip()
        if line:
            try:
                title, url = line.split('\t')
                assert url.startswith('http://') or url.startswith('https://')
            except:
                print('The line "%s" is not in "TITLE\\tABSOLUTEURL" format in %s/recommendations.txt' % (line, path))
                error = True
    if error:
        sys.exit(1)


def check_path(path):
    check_files(path, ('description.txt', 'name.txt', 'uuid.txt'))
    uuid_manager.check_uuid('path', path)
    check_recommendations(path)

    modules = glob(path + '/*/')
    for module in modules:
        check_module(module)


def check_module(path):
    check_files(path, ('description.html', 'name.txt', 'uuid.txt', 'difficulty.txt', 'type.txt', 'instruction.txt'))

    if os.path.isfile(os.path.join(path, 'NEED_FLAG')) == os.path.isfile(os.path.join(path, 'NOT_NEED_FLAG')):
        print('Exactly one of NEED_FLAG or NOT_NEED_FLAG must be present at %s' % path)
        sys.exit(1)

    type_ = trim_read(os.path.join(path, 'type.txt'))
    if type_ not in ('sshd', 'telnet', 'web', 'file'):
        print('Unknown type in %s/type.txt' % path)
        sys.exit(1)

    elif type_ in ('file',):
        for filename in ('flag.txt',):
            fullpath = os.path.join(path, filename)
            if not os.path.isfile(fullpath):
                print('Missing: %s (module type: %s)' % (fullpath, type_))
                sys.exit(1)
        if os.path.isdir(os.path.join(path, 'vm')):
            print('Warning: vm directory exists at %s but is not used' % path)

    elif type_ in ('sshd', 'web'):
        for filename in ('checker.txt', 'solvable.txt'):
            fullpath = os.path.join(path, 'vm/' + filename)
            if not os.path.isfile(fullpath):
                print('Missing: %s (module type: %s)' % (fullpath, type_))
                sys.exit(1)
            tag = trim_read(fullpath)
            if not os.path.isfile('docker/modules/%s/Dockerfile' % tag):
                print('Missing: docker/modules/%s/Dockerfile' % tag)
                print('Referenced from: %s' % fullpath)
                sys.exit(1)

    difficulty = trim_read(os.path.join(path, 'difficulty.txt'))
    if not difficulty.isdigit():
        print('Not a number in %s/difficulty.txt' % path)
        sys.exit(1)

    if os.path.exists(os.path.join(path, 'creator.txt')):
        creator_email = trim_read(os.path.join(path, 'creator.txt'))
        if not EMAIL_RE.match(creator_email):
            print('Invalid email address in %s/creator.txt' % path)
            sys.exit(1)

    uuid_manager.check_uuid('module', path)


def check_goal(path):
    check_files(path, ('description.txt', 'type.txt', 'name.txt', 'uuid.txt'))
    uuid_manager.check_uuid('goal', path)
    check_recommendations(path)

    type_ = trim_read(os.path.join(path, 'type.txt'))
    if type_ not in ('course', 'job'):
        print('Unknown type in %s/type.txt' % path)
        sys.exit(1)

    try:
        expiration = trim_read(os.path.join(path, 'expiration.txt'))
        datetime.strptime(expiration, '%Y-%m-%d')
    except ValueError:
        print('Invalid expiration date (Y-m-d) in %s/expiration.txt' % path)
        sys.exit(1)
    except:
        # No expiration date
        pass

    paths = glob(path + '/paths/*.txt')
    for path_link in paths:
        path_uuid = trim_read(path_link)
        uuid_manager.check_uuid_existence(path_uuid, 'path')


uuid_manager = UuidManager()

paths = glob('paths/*/')
for path in paths:
    check_path(path)

goals = glob('goals/*/')
for goal in goals:
    check_goal(goal)

print('Sanity check: OK')
