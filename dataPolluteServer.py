#!/usr/bin/env python
# -*-coding: utf-8 -*-

from socket import *
from threading import Thread
from threading import Lock
from random import randint, sample
from urllib import urlencode, urlopen
from urllib2 import Request
import string

class PortMonitor(Thread):
    def __init__(self, socket, port, peerManager):
        Thread.__init__(self)
        self.socket = socket
        self.port = port
        self.manager = peerManager

    def run(self):
        while True:
            client, addr = self.socket.accept()
            print("peer connect received from %s:%d on port %d" % (addr[0], addr[1], self.port))
            data = client.recv(1024)
            peer_id = self.manager.getPeer(self.port)
            if len(data) == 48 :
                client.send(data + peer_id)
                client.close()
                print('tracker connect')
            else:
                client.send(data[:48] + peer_id)
                print('peer connect')
                info_hash = data[28:48]
                bitfield = self.manager.getBitfield(info_hash)
                if bitfield is None:
                    client.close()
                    print("cannot find the info_hash: %s" % info_hash)
                else:
                    client.send(bitfield)
                # try:
                    while True:
                        data = client.recv(1024)
                        if(len(data) < 5):
                            continue
                        if data == '\x00\x00\x00\x01\x02':
                            client.send('\x00\x00\x00\x01\x01')
                            break
                    while True:
                        data = client.recv(1024)
                        requests = data.split(b'\x00\x00\x00\x0d')
                        for i in range(1, len(requests)):
                            piece = self.pieceGen(requests[i])
                            client.send(piece)
                # except error:
                #     print(error.message)

    def pieceGen(self, request):
        print(request)
        length = request[9:]
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
        print()
        return data



class DataServer(Thread):
    def __init__(self, client, peerManager):
       Thread.__init__(self)
       self.client = client
       self.peerManager = peerManager

    def run(self):
        client = self.client
        info = []
        while True:
            data = client.recv(1024)
            if data == b'END' or len(data) < 22:
                break
            length, info_hash, announce = data.split(' ')
            length = int(length)
            info.append((info_hash, announce))
            bitfield = ''
            for i in range(length >> 3):
                bitfield += '\xff'
            mod = length & 0x08
            print(length)
            print(mod)
            print("%x", bitfield)
            if mod != 0:
                bitfield += chr(0xff & (0xff << ( 8 - mod)))
            sent = parseInt(len(bitfield) + 1) + '\x05' + bitfield
            print(urlencode({'sent': sent}))
            self.peerManager.addBitfield(info_hash, sent)
            client.send(b'OK')
        client.send(b'OK')
        client.close()
        num = int(200 / len(info))
        group = len(info)
        for i in range(group):
            info_hash, announce = info[i]
            for j in range(num):
                port = 7200 + i * num + j
                ran_str = ''.join(sample(string.ascii_letters + string.digits, 20))
                self.peerManager.addInfoHash(port, info_hash)
                self.peerManager.addPeer(port, ran_str)
                register(announce, info_hash, port, ran_str)




class InfoManager:
    def __init__(self):
        self.peerLock = Lock()
        self.peer_id = {}
        self.bitLock = Lock()
        self.bitfield = {}
        self.infoLock = Lock()
        self.info_hash = {}
    
    def addPeer(self, port, peer_id):
        self.peerLock.acquire()
        self.peer_id[port] = peer_id
        self.peerLock.release()
    
    def getPeer(self, port):
        self.peerLock.acquire()
        peer_id = self.peer_id[port]
        self.peerLock.release()
        return peer_id

    def addBitfield(self, info_hash, bitfield):
        self.bitLock.acquire()
        self.bitfield[info_hash] = bitfield
        self.bitLock.release()
    
    def getBitfield(self, info_hash):
        self.bitLock.acquire()
        if info_hash not in self.bitfield.keys():
            self.bitLock.release()
            return None
        bitfield = self.bitfield[info_hash]
        self.bitLock.release()
        return bitfield
    
    def addInfoHash(self, port, info_hash):
        self.infoLock.acquire()
        self.info_hash[port] = info_hash
        self.infoLock.release()
    
    def getInfoHash(self, port):
        self.infoLock.acquire()
        info_hash = None
        if port in self.info_hash.keys():
            info_hash = self.info_hash[port]
        self.infoLock.release()
        return info_hash

def register(url,hash,i,ran_str):
    print('register: port is: %d' % i)
    param = {'info_hash': hash, 'peer_id': ran_str, 'ip': '127.0.0.1', 'port': str(i)}
    urlq = url +'?' + urlencode(param) + "&upload=0&downloaded=0&left=0&event=started&numwant=200&compact=1&no_peer_id=1&supportcrypto=1&redundant=0"
    print(urlq)
    urlopen(urlq)

def parseInt(num):
    byt = ''
    for i in range(4):
        byt = chr(num & 0xff) + byt
        num >>= 8
    return byt

def parseByte(byt):
    num = 0
    for i in range(4):
        num <<= 8
        num += chr(byt[i])
    return num

def openport():
    threads = []
    sockets = []
    ip = '0.0.0.0'
    server_port = 1080
    manager = InfoManager()
    for port in range(7200, 7400):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((ip, port))
        sock.listen(10)
        thread = PortMonitor(sock, port, manager)
        thread.start()
        threads.append(thread)
        sockets.append(socket)
    print("All ports are opened.\n Open server port...")
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((ip, server_port))
    server.listen(5)
    print("Server port are opened.")
    while True:
        client, addr = server.accept()
        print("Server connected from %s:%s" % addr)
        serverThread = DataServer(client, manager)
        serverThread.start()

if __name__ == "__main__":
    openport()
