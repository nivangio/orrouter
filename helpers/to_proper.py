from re import sub

def to_proper(x):
    return sub("_","",x).title()