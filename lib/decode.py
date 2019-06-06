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

def decode(str1):
    str2 = str1[92:136]
    str3 = str1[:92]
    str4 = str3 + b'65'
    data = codecs.decode(str4, "hex_codec")
    data = bytes.decode(data)
    str5 = str2[:14]
    str5 = codecs.decode(str5, "hex_codec")
    str5 = bytes.decode(str5)
    strs = str5.split(":")
    if len(strs[1]) != 5:
        sys.exit()
    str6 = str2[14:]
    str7 = str6[:4]
    str7 = codecs.decode(str7, "hex_codec")
    str7 = bytes.decode(str7)
    a = int(str7)
    if len(str6[6:]) != a*2:
        sys.exit()
    global p
    l = len(data)
    p = 0
    while p < l:
        if data[p] == "d":
            data_dict = decode_dict(data, p)
            p = int(data_dict["p"])
            del data_dict["p"]
            print("true")
            return True
        elif data[p] == "l":
            print("类型： list")
            data_list = decode_list(data, p)
            p = int(data_list[-1])
            del data_list[-1]
            del data_list[-1]
            print("true")
            return True
        elif data[p] == "i":
            f = data.index("e", p, l)
            data_int = data[p + 1:f]
            p = f + 1
            print("true")
            return True
        elif data[p].isdigit():
            f = data.index(":", p, l)
            data_str = data[f + 1:int(data[p:f]) + f + 1]
            p = int(data[p:f]) + f + 1
            print("true")
            return True
        else:
            print("false")
            return False

# str1 = b"64383a636f6d706c65746569336531303a696e636f6d706c657465693065383a696e74657276616c693138303065353a706565727331323a9de6f80d1ae198884e221ae165"
# decode(str1)