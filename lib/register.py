from urllib import request,parse
import random,string

def register(url,hash,i):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 20))
    header = {'info_hash':hash,'peer_id':ran_str,'ip':'206.189.83.15','port':i,'uploaded':0,'downloaded':0,'left':0,'event':'started'}
    urlq = url + "?info_hash="+ hash + "&peer_id="+ran_str+"&ip=206.189.83.15&port="+str(i)+"&upload=0&downloaded=0&left=0&event=started"
    req = request.Request(urlq,headers=header)

    with request.urlopen(req) as f:
        Data = f.read()

def get(url,hash,times):
    r1 = range(6200,times+6200)
    for i in r1:
        register(url,hash,i)