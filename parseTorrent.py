from bencode import bdecode

def decodeTorrent():
    f = open('/home/zhangyang/Downloads/BitTorrent-4.0.3.tar.gz.torrent', 'rb')
    data = f.read()
    f.close()
    print(bdecode(data))

if __name__ == "__main__":
    decodeTorrent()