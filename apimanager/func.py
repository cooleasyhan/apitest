from builtins import *
import hashlib
import time


def md5(x):
    # return 'xxx'
    return hashlib.md5(x.encode('utf-8')).hexdigest()


def unix_time():
    return time.time()


def token(*args):
    s = ''.join(sorted([str(a) for a in args]))
    sha1 = hashlib.sha1()
    sha1.update(s.encode('utf-8'))
    key = sha1.hexdigest()
    return key


g = {'builtins__md5': md5, 'builtins__unix_time': unix_time, 'builtins__token': token}
