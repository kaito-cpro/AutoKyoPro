# Python Version: 3.x
# -*- coding: utf-8 -*-
import onlinejudge.implementation.logging as log
import onlinejudge.__about__ as version
from onlinejudge.type import LabeledString, TestCase

import appdirs
import bs4
import requests

import contextlib
import distutils.version
import http.client
import http.cookiejar
import json
import pathlib
import posixpath
import re
import subprocess
import sys
import time
import urllib.parse
from typing import *
from typing.io import *

config_dir = pathlib.Path(appdirs.user_config_dir(version.__package_name__))
data_dir = pathlib.Path(appdirs.user_data_dir(version.__package_name__))
cache_dir = pathlib.Path(appdirs.user_cache_dir(version.__package_name__))
html_parser = 'lxml'

def percentformat(s: str, table: Dict[str, str]) -> str:
    assert '%' not in table or table['%'] == '%'
    table['%'] = '%'
    result = ''
    for m in re.finditer('[^%]|%(.)', s):
        if m.group(1):
            if m.group(1) in table:
                result += table[m.group(1)]
        else:
            result += m.group(0)
    return result

def describe_status_code(status_code: int) -> str:
    return '{} {}'.format(status_code, http.client.responses[status_code])

def previous_sibling_tag(tag: bs4.Tag) -> bs4.Tag:
    tag = tag.previous_sibling
    while tag and not isinstance(tag, bs4.Tag):
        tag = tag.previous_sibling
    return tag

def next_sibling_tag(tag: bs4.Tag) -> bs4.Tag:
    tag = tag.next_sibling
    while tag and not isinstance(tag, bs4.Tag):
        tag = tag.next_sibling
    return tag

def new_default_session() -> requests.Session:  # without setting cookiejar
    session = requests.Session()
    session.headers['User-Agent'] += ' (+{})'.format(version.__url__)
    return session

default_cookie_path = data_dir / 'cookie.jar'

@contextlib.contextmanager
def with_cookiejar(session: requests.Session, path: pathlib.Path = default_cookie_path) -> Generator[requests.Session, None, None]:
    session.cookies = http.cookiejar.LWPCookieJar(str(path))  # type: ignore
    if path.exists():
        log.status('load cookie from: %s', path)
        session.cookies.load()  # type: ignore
    yield session
    log.status('save cookie to: %s', path)
    path.parent.mkdir(parents=True, exist_ok=True)
    session.cookies.save()  # type: ignore
    path.chmod(0o600)  # NOTE: to make secure a little bit


class SampleZipper(object):
    def __init__(self):
        self.data = []
        self.dangling = None

    def add(self, s: str, name: str = '') -> None:
        if self.dangling is None:
            if re.search('output', name, re.IGNORECASE) or re.search('出力', name):
                log.warning('strange name for input string: %s', name)
            self.dangling = LabeledString(name, s)
        else:
            if re.search('input', name, re.IGNORECASE) or re.search('入力', name):
                if not (re.search('output', name, re.IGNORECASE) or re.search('出力', name)):  # to ignore titles like "Output for Sample Input 1"
                    log.warning('strange name for output string: %s', name)
            self.data += [ TestCase(self.dangling, LabeledString(name, s)) ]
            self.dangling = None

    def get(self) -> List[TestCase]:
        if self.dangling is not None:
            log.error('dangling sample string: %s', self.dangling[1])
        return self.data

class FormSender(object):
    def __init__(self, form: bs4.Tag, url: str):
        assert isinstance(form, bs4.Tag)
        assert form.name == 'form'
        self.form = form
        self.url = url
        self.payload = {}  # type: Dict[str, str]
        self.files = {}  # type: Dict[str, IO[Any]]
        for input in self.form.find_all('input'):
            log.debug('input: %s', str(input))
            if input.attrs.get('type') in [ 'checkbox', 'radio' ]:
                continue
            if 'name' in input.attrs and 'value' in input.attrs:
                self.payload[input['name']] = input['value']

    def set(self, key: str, value: str) -> None:
        self.payload[key] = value

    def get(self) -> Dict[str, str]:
        return self.payload

    def set_file(self, key: str, filename: str, content: bytes) -> None:
        self.files[key] = ( filename, content )  # type: ignore

    def request(self, session: requests.Session, action: Optional[str] = None, **kwargs) -> requests.Response:
        action = action or self.form['action']
        url = urllib.parse.urljoin(self.url, action)
        method = self.form['method'].upper()
        log.status('%s: %s', method, url)
        log.debug('payload: %s', str(self.payload))
        resp = session.request(method, url, data=self.payload, files=self.files, **kwargs)
        log.status(describe_status_code(resp.status_code))
        return resp

def dos2unix(s: str) -> str:
    return s.replace('\r\n', '\n')
def textfile(s: str) -> str:  # should have trailing newline
    if s.endswith('\n'):
        return s
    elif '\r\n' in s:
        return s + '\r\n'
    else:
        return s + '\n'

# http://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons-in-python/12850496#12850496
def singleton(cls):
    instance = cls()
    # Always return the same object
    cls.__new__ = staticmethod(lambda cls: instance)
    # Disable __init__
    try:
        del cls.__init__
    except AttributeError:
        pass
    return cls

def exec_command(command: List[str], timeout: float = None, **kwargs) -> Tuple[bytes, subprocess.Popen]:
    try:
        # 自分で書き換えた箇所
        f = open('onlinejudge/communication.py', 'r')
        com_prob = f.read()[0]
        f.close()
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=sys.stderr, **kwargs, cwd=r''+com_prob.upper())
    except FileNotFoundError:
        log.error('No such file or directory: %s', command)
        sys.exit(1)
    except PermissionError:
        log.error('Permission denied: %s', command)
        sys.exit(1)
    try:
        answer, _ = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        answer = b''
    return answer, proc

# We should use this instead of posixpath.normpath
# posixpath.normpath doesn't collapse a leading duplicated slashes. see: https://stackoverflow.com/questions/7816818/why-doesnt-os-normpath-collapse-a-leading-double-slash
def normpath(path: str) -> str:
    path = posixpath.normpath(path)
    if path.startswith('//'):
        path = '/' + path.lstrip('/')
    return path


def request(method: str, url: str, session: requests.Session, raise_for_status: bool = True, **kwargs) -> requests.Response:
    assert method in [ 'GET', 'POST' ]
    kwargs.setdefault('allow_redirects', True)
    log.status('%s: %s', method, url)
    resp = session.request(method, url, **kwargs)
    log.status(describe_status_code(resp.status_code))
    if raise_for_status:
        resp.raise_for_status()
    return resp


def get_latest_version_from_pypi() -> str:
    pypi_url = 'https://pypi.org/pypi/{}/json'.format(version.__package_name__)
    version_cache_path = cache_dir / "pypi.json"
    update_interval = 60 * 60 * 8  # 8 hours

    # load cache
    if version_cache_path.exists():
        with version_cache_path.open() as fh:
            cache = json.load(fh)
        if time.time() < cache['time'] + update_interval:
            return cache['version']

    # get
    try:
        resp = request('GET', pypi_url, session=requests.Session())
        data = json.loads(resp.content.decode())
        value = data['info']['version']
    except requests.RequestException as e:
        log.error(str(e))
        value = '0.0.0'  # ignore since this failure is not important
    cache = {
        'time': int(time.time()),  # use timestamp because Python's standard datetime library is too weak to parse strings
        'version': value,
    }

    # store cache
    version_cache_path.parent.mkdir(parents=True, exist_ok=True)
    with version_cache_path.open('w') as fh:
        json.dump(cache, fh)

    return value

def is_update_available_on_pypi() -> bool:
    a = distutils.version.StrictVersion(version.__version__)
    b = distutils.version.StrictVersion(get_latest_version_from_pypi())
    return a < b
