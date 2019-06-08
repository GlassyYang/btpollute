from urllib import request,parse
import random,string,client,socket


def register(url,hash,i,ran_str):
    urlq = url + "?info_hash="+ hash + "&peer_id="+ran_str+"&port="+str(i)+"&upload=0&downloaded=0&left=0&event=started&numwant=200&compact=1&no_peer_id=1&supportcrypto=1&redundant=0"
    req = request.Request(urlq)

    with request.urlopen(req) as f:
        Data = f.read()

def get(url,hash,times):
    r1 = range(7200,times+7200)
    lst = []
    for i in r1:
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 20))
        lst.append(ran_str)
    for i in r1:
        port = []
        port.append(i >> 8)
        port.append(i & 0xff)
        ports = bytes(port)
        peer = bytes(lst[i-7200],encoding='utf-8')
        data = ports + peer
        print(data)
        connectServer(data)
    for i in r1:
        register(url,hash,i,lst[i-7200])

def connectServer(data):
    ip = '192.168.43.160'
    port = 1080
    new_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    new_socket.connect((ip, port))
    while True:
        new_socket.send(data)
        back_str = new_socket.recv(1024)
        print(back_str)
        break
# if __name__ == "__main__":
#     get('http://152.136.78.34:6969/announce', '%deY%935%b8K%d8%f9%d9%c9kE%b8%c8%d4%ca%dc%b6%2f%90', 1)

# 电影的info_hash: %deY%935%b8K%d8%f9%d9%c9kE%b8%c8%d4%ca%dc%b6%2f%90