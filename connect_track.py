from urllib3 import PoolManager

url = "http://152.136.78.34:6969/announce?info_hash=fV%a3%bc%c8Lc%df%e3%ebF%1b!%b1GC%9e%7c%2f%5b&peer_id=-qasdf0-4zKcDf5.gEWv&port=8999&uploaded=0&downloaded=0&left=0&corrupt=0&key=9A3DB0B4&event=started&numwant=200&compact=1&no_peer_id=1&supportcrypto=1&redundant=0"

http = PoolManager()
r = http.request('GET', url)
print(r.status)
print(r.data)