#! /usr/bin/env python3
from urllib import request,parse
import random,string,socket

def register(url,hash,i,ran_str):
    urlq = url + "?info_hash="+ hash + "&peer_id="+ran_str+"&ip=152.136.78.34&port="+str(i)+"&upload=0&downloaded=0&left=0&event=started&numwant=200&compact=1&no_peer_id=1&supportcrypto=1&redundant=0"
    req = request.Request(urlq)

    with request.urlopen(req) as f:
        Data = f.read()

def get(url,hash,times):

    # ip = '206.189.83.15'
    ip = '152.136.78.34'
    port = 1080
    new_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    new_socket.connect((ip, port))
    print(type(url))
    print(type(hash))
    new_socket.send(url.encode() + b' ' + hash.encode() + b' ' + str(times).encode())
    data = new_socket.recv(1024)
    print(data)

# if __name__ == "__main__":
#     get('http://152.136.78.34:6969/announce', '%deY%935%b8K%d8%f9%d9%c9kE%b8%c8%d4%ca%dc%b6%2f%90', 1)


# 电影的info_hash: %deY%935%b8K%d8%f9%d9%c9kE%b8%c8%d4%ca%dc%b6%2f%90