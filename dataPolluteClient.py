#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sha import sha
from bencode import bdecode, bencode
from socket import *
import os
import sys

def parseTorrent(file):
    f = open(file, 'rb')
    data = f.read()
    dic = bdecode(data)
    info = dic['info']
    announce = dic['announce']
    pieceNum = len(info['pieces']) / 20
    info_hash = sha(bencode(dic['info'])).digest()
    return pieceNum, info_hash, announce

def connectToServer(info):
    # ip = '206.189.83.15'
    ip = '152.136.78.34'
    # ip = '127.0.0.1'
    port = 1080
    connect = socket(AF_INET, SOCK_STREAM)
    connect.connect((ip, port))
    for num, hash, announce in info:
        data = str(num) + ' ' + hash + ' ' + announce
        connect.send(data)
        print(data)
        data = connect.recv(1024)
        print(data)
    connect.send('END')
    connect.close()

def scanDir(dir):
    info = []
    for file in os.listdir(dir):
        if os.path.splitext(file)[1] == '.torrent':
            info.append(parseTorrent(dir + '/' + file))
    connectToServer(info)


if __name__ == "__main__":
    if(len(sys.argv) == 1):
        scanDir('.')
    else:
        scanDir(sys.argv[1])



