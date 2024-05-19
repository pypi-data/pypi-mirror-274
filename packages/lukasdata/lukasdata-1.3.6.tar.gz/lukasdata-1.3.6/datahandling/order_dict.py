def order_dict_by_key(dictionary):
    sorted_dict=dict(sorted(dictionary.items(), key=lambda x: x[1]))
    return sorted_dict

