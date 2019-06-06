from urllib import request,parse
import random,string

def register(url,hash,i,num):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 20))
    header = {'info_hash':hash,'peer_id':ran_str,'ip':'206.189.83.15','port':i,'uploaded':0,'downloaded':num,'left':0,'event':'completed'}
    urlq = url + "?info_hash="+ hash + "&peer_id="+ran_str+"&ip=206.189.83.15&port="+str(i)+"&upload=0&downloaded="+num+"&left=0&event=completed"
    req = request.Request(urlq,headers=header)

    with request.urlopen(req) as f:
        Data = f.read()

def get(url,hash,times,num):
    r1 = range(7200,times+7200)
    for i in r1:
        register(url,hash,i,num)