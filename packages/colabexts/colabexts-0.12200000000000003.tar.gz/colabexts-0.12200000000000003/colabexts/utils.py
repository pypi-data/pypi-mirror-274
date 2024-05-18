import os, sys, re, importlib, json, datetime, glob, platform, matplotlib, dateutil 
import numpy as np
from datetime import timedelta;
import urllib.request;
from collections import defaultdict
#-----------------------------------------------------------------------------------
class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]


#-----------------------------------------------------------------------------------
def inJupyter():
    try:    get_ipython; return True
    except: return False
#--------------------------------------------------------------------------------
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
#--------------------------------------------------------------------------------
def encrypt(msg_text = b'message', secret_key='password'):
    if (type(msg_text) == str):
        msg_text = bytes(msg_text, encoding='utf-8').rjust(32)
    if (type(secret_key) == str):
        secret_key = bytes(secret_key, encoding='utf-8') .rjust(32)

    cipher = AES.new(secret_key,AES.MODE_ECB) 
    encoded = base64.b64encode(cipher.encrypt(msg_text))
    ret = encoded.decode("utf-8")
    print(ret)
    return ret
#--------------------------------------------------------------------------------
def decrypt(encoded, secret_key='password'):
    if (type(secret_key) == str):
        secret_key = bytes(secret_key, encoding='utf-8') .rjust(32)

    cipher = AES.new(secret_key,AES.MODE_ECB) 
    if (type(encoded) == str):
        encoded = bytes(encoded, encoding='utf-8')
    decoded = cipher.decrypt(base64.b64decode(encoded))
    ret =decoded.decode("utf-8").strip()
    print(ret)
    return ret
#--------------------------------------------------------------------------------
class mydict(dict):
    def __init__(self, *args, **kwargs):
        super(mydict, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(mydict, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(mydict, self).__delitem__(key)
        del self.__dict__[key]

    def __missing__(self, key):
         if key in  locals():
             return locals()[key]
         return key

    def parsej(self, s):
        eval(s, **self)

        
def parsej(s, *args, **kwargs):
    return mydict(eval(s.strip() or "{}", mydict(*args, **kwargs)))

