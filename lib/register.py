from urllib import request,parse
import random,string

def register(url,hash):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 20))
    print(ran_str)
    ran_int = random.randrange(6881,6969)
    print(ran_int)
    value = parse.urlencode({'info_hash':hash,'peer_id':ran_str,'ip':'114.114.114.114','port':ran_int,'uploaded':0,'downloaded':0,'left':0,'event':'started'})
    header = {'info_hash':hash,'peer_id':ran_str,'ip':'114.114.114.114','port':ran_int,'uploaded':0,'downloaded':0,'left':0,'event':'started'}
    urlq = url + "/announce?info_hash="+ hash + "&peer_id="+ran_str+"&ip=114.114.114.114&port="+str(ran_int)+"&upload=0&downloaded=0&left=0&event=started"
    req = request.Request(urlq,headers=header)

    with request.urlopen(req) as f:
        Data = f.read()
        print(Data)

def get(url,hash,times):
    r1 = range(0,times)
    for i in r1:
        register(url,hash)