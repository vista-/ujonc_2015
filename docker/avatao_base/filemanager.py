import base64
import mimetypes
import re
import os
from collections import namedtuple
from fnmatch import fnmatch
from pathlib import Path
from urllib.request import urlretrieve
from flask import request


DEFAULT_MIME = os.environ['DEFAULT_MIME'] if 'DEFAULT_MIME' in os.environ else 'application/octet-stream'
FILES_ROOT = os.environ['FILES_ROOT'] if 'FILES_ROOT' in os.environ else '/home/user'
File = namedtuple('File', ('path', 'content', 'editable', 'executable'))


DATA_URI_REGEX = r'^data:' \
    r'(?P<mime>[\w]+/[\w\-\+\.]+)?' \
    r'(?:;charset=(?P<charset>[\w\-\+\.]+))?' \
    r'(?P<base64>;base64)?' \
    r',(?P<data>.*)$'
DATA_URI_RE = re.compile(DATA_URI_REGEX, re.DOTALL)


class Ignore:
    """Ignore handler for directory listing

    Initialize it with path parts pointing to an ignore file.
    The ignore file should contain one pattern per line that's understood by fnmatch.
    If the ignore file does not exist, it will not fail and always return false.
    """

    def __init__(self, *args):
        path = os.path.join(*args)
        self._exists = os.path.isfile(path)
        if self._exists:
            with open(path, encoding='utf-8-sig', errors='replace') as f:
                self.patterns = f.read().splitlines()
            self.patterns.append(args[-1])

    def is_ignored(self, rel_path):
        if self._exists:
            for pattern in self.patterns:
                if fnmatch(rel_path, pattern):
                    return True
        return False

ignore_handler = Ignore(FILES_ROOT, '.ignore')


def sanitized_path(*args) -> tuple:
    """Return the real and relative paths

    :param *args: optional number of path parts
    :return tuple: path, rel_path
    :raise ValueError: if the path is invalid
    """

    path = os.path.abspath(os.path.join(*args))
    rel_path = str(Path(path).relative_to(FILES_ROOT))
    return path, rel_path


def file(path_) -> File:
    """GET, POST/PUT or DELETE a File

    # Sample code for Flask:
    @app.route('/%s/file/<path:path_>' % os.environ['SECRET'], methods=['GET', 'PUT', 'DELETE'])
    def file(path_):
        return jsonify(file=filemanager.file(path_))

    :param path_: relative path to FILES_ROOT
    :return File: path, content, editable, executable
    :raise ValueError: if the path or data URI is invalid
    :raise IOError: in case of file errors
    :raise FileNotFoundError: in case of file errors
    :raise PermissionError: in case of file errors
    """

    path, rel_path = sanitized_path(FILES_ROOT, path_)

    if request.method == 'GET':
        with open(path, 'rb') as f:
            mime, _ = mimetypes.guess_type(path)
            data64 = base64.b64encode(f.read()).decode('ascii')
            content = u'data:%s;base64,%s' % (mime if mime else DEFAULT_MIME, data64)
            editable = os.access(path, os.W_OK)
            executable = os.access(path, os.X_OK)
            return File(rel_path, content, editable, executable)

    elif request.method == 'DELETE':
        os.remove(path)
        return File(rel_path, None, False, False)

    else:
        if not DATA_URI_RE.match(request.json['content']):
            raise ValueError('Invalid data URI')
        os.makedirs(os.path.dirname(path), 0o755, True)
        urlretrieve(request.json['content'], path)
        return File(rel_path, None, True, os.access(path, os.X_OK))


def files() -> [File]:
    """Return a deep list of Files in FILES_ROOT

    # Sample code for Flask:
    @app.route('/%s/files' % os.environ['SECRET'], methods=['GET'])
    def files():
        return jsonify(files=filemanager.files())

    :return [File]
    """

    file_list = []
    for subdir, dirs, files_ in os.walk(FILES_ROOT, followlinks=True):
        for file_ in files_:
            path, rel_path = sanitized_path(subdir, file_)
            if not ignore_handler.is_ignored(rel_path):
                editable = os.access(path, os.W_OK)
                executable = os.access(path, os.X_OK)
                file_list.append(File(rel_path, None, editable, executable))
    return file_list
