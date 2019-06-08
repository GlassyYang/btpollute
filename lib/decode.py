import codecs,sys
def decode_list(str, p):
    lenth = len(str)
    list = []
    while p < lenth:
        if str[p + 1].isdigit():
            f_m = str.index(":", p + 1, lenth)
            f_n = int(str[p + 1:f_m])
            f_e = f_m + f_n
            data_str = str[f_m + 1:f_e + 1]
            list.append(data_str)
            p = f_e
        elif str[p + 1] == "i":
            end = str.index("e", p + 1, lenth)
            data_int = str[p + 2: int(end)]
            list.append(data_int)
            p = end
        elif str[p + 1] == "e":
            p = p + 2
            list.append("p")
            list.append(p)
            break
        elif str[p + 1] == "l":
            p = p + 1
    return list

def decode_dict(str, p):
    test = decode_list(str, p)
    data_seq = []
    data_val = []
    i = 0
    while i < len(test):
        data_seq.append(test[i])
        data_val.append(test[i + 1])
        i = i + 2
    data_dict = dict.fromkeys(data_seq)
    i = 0
    while i < len(test) / 2:
        data_dict[data_seq[i]] = data_val[i]
        i = i + 1
    return data_dict

def decode(str):
    try:
        strs = str.split(b'5:peers')
        str0 = strs[0] + b'e'
        data = bytes.decode(str0)
        strq  = strs[1].split(b":")
        a = int(strq[0])
        if a != len(strq[1])-1:
            return False
        global p
        l = len(data)
        p = 0
        while p < l:
            if data[p] == "d":
                data_dict = decode_dict(data, p)
                p = int(data_dict["p"])
                del data_dict["p"]
                return True
            elif data[p] == "l":
                data_list = decode_list(data, p)
                p = int(data_list[-1])
                del data_list[-1]
                del data_list[-1]
                return True
            elif data[p] == "i":
                f = data.index("e", p, l)
                data_int = data[p + 1:f]
                p = f + 1
                return True
            elif data[p].isdigit():
                f = data.index(":", p, l)
                data_str = data[f + 1:int(data[p:f]) + f + 1]
                p = int(data[p:f]) + f + 1
                return True
            else:
                return False
    except ValueError:
        return False

# str = b'd8:completei3e10:incompletei0e8:intervali1800e5:peers12:\x9d\xe6\xf8\r\x1a\xe1\x98\x88N"\x1a\xe1e'
# str = b'd8:completei14e10:incompletei0e8:intervali1800e5:peersld2:ip13:152.136.78.347:peer_id20:M4-0-3--cbe1c06b37c34:porti6882eed2:ip13:152.136.78.347:peer_id20:M4-0-3--6ea32d19e7734:porti6881eeee'
# print(decode(str))
