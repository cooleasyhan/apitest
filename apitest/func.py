import hashlib
import time
from base64 import b64decode, b64encode
from builtins import *
from hashlib import md5

from Crypto import Random
from Crypto.Cipher import AES

# Padding for the input string --not
# related to encryption itself.
BLOCK_SIZE = 16  # Bytes


def pad(s):
    if isinstance(s, str):
        _s = s.encode('utf-8')
    else:
        _s = s
    return s + (BLOCK_SIZE - len(_s) % BLOCK_SIZE) * \
        chr(BLOCK_SIZE - len(_s) % BLOCK_SIZE)


def unpad(s): return s[:-ord(s[len(s) - 1:])]


def aes_cbc_encrypt(key, iv, raw):
    raw = pad(raw)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return b64encode(cipher.encrypt(raw.encode('utf-8')))


def aes_cbc_decrypt(key, iv, enc):
    enc = b64decode(enc)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    x = unpad(cipher.decrypt(enc))
    return x.decode('utf8')


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


g = {'md5': md5, 'unix_time': unix_time, 'token': token,
     'aes_cbc_encrypt': aes_cbc_encrypt, 'aes_cbc_decrypt': aes_cbc_decrypt}
