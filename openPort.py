#!/usr/bin/env python
# -*-coding: utf-8 -*-
from socket import *
from threading import Thread
from threading import Lock


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
        while True:
            data = client.recv(1024)
            if data == b'END' or len(data) < 22:
                break
            port = (data[0] << 8) + data[1]
            peer_id = data[2:]
            self.peerManager.add(port, peer_id)
            client.send(b'OK')
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
        peer_id = peer_id[port]
        self.lock.realease()
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

if __name__ == "__main__":
    openport()
