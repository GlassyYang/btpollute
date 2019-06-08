from urllib3 import PoolManager

url = "http://127.0.0.1:6969/announce?info_hash=%deY%935%b8K%d8%f9%d9%c9kE%b8%c8%d4%ca%dc%b6%2f%90&peer_id=-qasdf0-zKsDfy.gEWva&port=8999&uploaded=0&downloaded=157027&left=0&corrupt=0&key=9A3DB0B4&event=completed&numwant=200&compact=1&no_peer_id=1&supportcrypto=1&redundant=0"

http = PoolManager()
r = http.request('GET', url)
print(r.status)
print(r.data)