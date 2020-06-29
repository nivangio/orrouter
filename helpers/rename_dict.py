
def rename_dict(x, old_key, new_key):
    x[new_key] = x.pop(old_key)
    return  x