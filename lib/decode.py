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
data = "d8:completei3e10:incompletei0e8:intervali1800e5:peers4:liste"
def decode(data):
    print("输入为："+data)
    global p
    l = len(data)
    p = 0
    while p < l:
        if data[p] == "d":
            print("类型： dictionary")
            data_dict = decode_dict(data, p)
            p = int(data_dict["p"])
            del data_dict["p"]
            print("解码：")
            print(data_dict)
            print("true")
            return True
        elif data[p] == "l":
            print("类型： list")
            data_list = decode_list(data, p)
            p = int(data_list[-1])
            del data_list[-1]
            del data_list[-1]
            print("解码：")
            print(data_list)
            print("true")
            return True
        elif data[p] == "i":
            print("类型： int")
            f = data.index("e", p, l)
            data_int = data[p + 1:f]
            p = f + 1
            print(data_int)
            print("true")
            return True
        elif data[p].isdigit():
            print("类型： string")
            f = data.index(":", p, l)
            print("解码：")
            print(data[f])
            data_str = data[f + 1:int(data[p:f]) + f + 1]
            print(data_str)
            p = int(data[p:f]) + f + 1
            print("true")
            return True
        else:
            print("false")
            return False