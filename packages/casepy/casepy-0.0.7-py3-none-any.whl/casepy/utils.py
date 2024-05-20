def in_list_to_bin(in_list: list):
    result_dict = {}
    element_list = []
    for i in in_list:
        if i not in element_list:
            element_list.append(i)
            result_dict[i] = 1
        else:
            result_dict[i] += 1

    result_list = list(result_dict.values())
    return result_list, element_list
