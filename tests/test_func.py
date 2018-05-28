import string
from apitest.func import aes_cbc_decrypt, aes_cbc_encrypt
import random


def test_aes_cbc():
    key = iv = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=16))
    ss = ['中文',
          'abc',
          '1234567890123456',
          string.printable,
          '简介：汉语，汉族的语言，中国的通用语言。国际通用语言之一。属汉藏语系，同中国境内的藏语、壮语、傣语、侗语、黎语、彝语、苗语、瑶语等，中国境外的泰语、缅甸语等都是亲属语言。汉语历史悠久，使用的人数最多。全球至少15亿使用者']

    for s in ss:
        enc = aes_cbc_encrypt(key, iv, s)
        x = aes_cbc_decrypt(key, iv, enc)

        assert (s == x)
