def combine_dict_list(list_a, list_b):
    list_c = list()
    i = j = 0
    while i < len(list_a) and j < len(list_b):
        if list_a[i]["date"] > list_b[j]["date"]:
            list_c.append(list_a[i])
            i = i + 1
        elif list_a[i]["date"] < list_b[j]["date"]:
            list_c.append(list_b[j])
            j = j + 1
        else:
            list_c.append(list_a[i])
            i = i + 1
            j = j + 1
    if i < len(list_a):
        list_c.extend(list_a[i:])
    if j < len(list_b):
        list_c.extend(list_b[j:])
    return list_c


def parse_str_array(string):
    arr_tmp = string.split(",")
    arr = list()
    for item in arr_tmp:
        if item.isdigit():
            arr.append(int(item))
            continue
        pair = item.split("-")
        arr.extend(range(int(pair[0]), int(pair[1]) + 1))
    return arr
