#!/usr/bin/env python
# -*-coding: utf-8 -*-

from sha import sha
from bencode import bencode, bdecode
from random import randint
def pieceGen(request):
        print('pieces: ', request)
        length = request[9:]
        print(length)
        count = 0
        for i in range(4):
            count <<= 8
            count += ord(length[i])
        print(count)
        data = ''
        for i in range(count):
            data += chr(randint(1, 255))
        data = '\x07' + request[1:9] + data
        count += 9
        length = ''
        for i in range(4):
            length = chr(count & 0xff) + length
            count >>= 8
        data = length + data
        return data

piece = '\x06\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00@\x00'

print(pieceGen(piece))

