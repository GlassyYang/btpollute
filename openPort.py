#!/usr/bin/env python
# -*-coding: utf-8 -*-
from socket import *
from threading import Thread

class PortMonitor(Thread):
    def __init__(self, socket, port):
        Thread.__init__(self)
        self.socket = socket
        self.port = port

    def run(self):
        while True:
            client, addr = self.socket.accept()
            print("connect received from %s:%d on port %d" % (addr[0], addr[1], self.port))
            data = client.recv(1024)
            print(data)


def openport():
    threads = []
    sockets = []
    ip = 'localhost'
    for port in range(7200, 7400):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((ip, port))
        sock.listen(10)
        thread = PortMonitor(sock, port)
        thread.start()
        threads.append(thread)
        sockets.append(socket)
    print("all ports are opened")
    threads[0].join()

if __name__ == "__main__":
    openport()


        