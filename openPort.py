#!/usr/bin/env python
# -*-coding: utf-8 -*-
from socket import *
from threading import Thread
from threading import Lock
from random import sample
import string
from urllib import urlencode, urlopen

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
            peer_id = self.manager.get(self.port)
            client.send(data + peer_id)


class IndexServer(Thread):
    def __init__(self, client, peerManager):
       Thread.__init__(self)
       self.client = client
       self.peerManager = peerManager


    def run(self):
        client = self.client
        data = client.recv(1024)
        url, hash, times = data.split(' ')
        times = int(times)
        for i in range(7200, 7200 + times):
            ran_str = ''.join(sample(string.ascii_letters + string.digits, 20))
            self.peerManager.add(i, ran_str)
            register(url, hash, i, ran_str)
        client.send(b'OK')
        client.close()



class PeerIdManager:
    def __init__(self):
        self.lock = Lock()
        self.peer_id = {}
    
    def add(self, port, peer_id):
        self.lock.acquire()
        self.peer_id[port] = peer_id
        self.lock.release()
    
    def get(self, port):
        self.lock.acquire()
        peer_id = self.peer_id[port]
        self.lock.release()
        return peer_id



def openport():
    threads = []
    sockets = []
    ip = '0.0.0.0'
    server_port = 1080
    manager = PeerIdManager()
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
        print("Server connected from %s:%s", addr)
        serverThread = IndexServer(client, manager)
        serverThread.start()

def register(url,hash,i,ran_str):
    print('register: port is: %d' % i)
    urlq = url + "?info_hash="+ hash + "&peer_id="+ran_str+"&ip=152.136.78.34&port="+str(i)+"&upload=0&downloaded=0&left=0&event=started&numwant=200&compact=1&no_peer_id=1&supportcrypto=1&redundant=0"
    urlopen(urlq)

if __name__ == "__main__":
    openport()
