from scapy.all import *
from lib import decode
# 存储会话的ip地址对
session_dict = {}
# 存储tracker服务器对应的info_hash
info_hash_dict = {}

def pcap_and_analyze():
    pkgs = sniff(iface="wlan0", filter="tcp", count=100, prn=rollback)
    # for pkg in pkgs:
    #     rollback(pkg)
    return


def rollback(pkg):
    payload = bytes(pkg[TCP].payload)
    length = len(payload)
    if payload is None or length <= 4:
        return
    if payload[:3] == b"GET" and payload[-4:] == b"\r\n\r\n":
        info_hash = isHttpRequest(payload)
        print(info_hash)
        if info_hash:
            session_dict[pkg.payload.dst] = pkg.payload.src
            info_hash_dict[pkg.payload.dst] = info_hash
    elif pkg.payload.src in session_dict.keys() and session_dict[pkg.payload.src] == pkg.payload.dst:
        response = payload.split(b"\r\n\r\n")
        if len(response) != 2:
            return
        head = response[0].split(b'\r\n')
        body = response[1]
        if len(head) == 0 and head[0] != b'HTTP/1.0 200 OK' and head[0] != b'HTTP/1.1 200 OK':
            return
        print(body)
        if not decode.decode(body):
            print(2)
            return
        print("succeed catch a pkg src is %s and dest is %s" % (pkg.payload.src, pkg.payload.dst))
    return


def isHttpRequest(payload):
    lines = payload.decode().split("\r\n")
    # 提取host:
    host = lines[1].split(': ')
    if len(host) != 2 or host[0] != 'Host':
        return False
    host = host[1]
    #提取url
    url = lines[0].split(' ')
    if len(url) != 3 or url[0] != 'GET':
        return False
    url = url[1].split('?')
    if len(url) != 2:
        return False
    url, params = url[0], url[1].split('&')
    # 从url的参数中生成字典
    temp = {}
    for param in params:
        sin = param.split('=')
        if len(sin) != 2 or len(sin[0]) == 0 or len(sin[1]) == 0:
            return False
        temp[sin[0]] = sin[1]
    param = temp
    if "info_hash" not in param.keys():
        return False
    info_hash = param["info_hash"]
    if "peer_id" not in param.keys():
        return False
    if "port" not in param.keys():
        return False
    return info_hash

if __name__ == "__main__":
    pcap_and_analyze()
