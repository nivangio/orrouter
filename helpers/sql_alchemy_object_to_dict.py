from decimal import Decimal

def sql_alchemy_object_to_dict(obj, variables = "all"):
    all_elems = obj.__dict__
    ret = {}
    if variables == "all":
        variables = list(all_elems.keys())
        variables.remove('_sa_instance_state')

    for i in variables:
        if isinstance(all_elems[i], Decimal):
            ret[i] = float(all_elems[i])
        else:
            ret[i] = all_elems[i]

    return ret
