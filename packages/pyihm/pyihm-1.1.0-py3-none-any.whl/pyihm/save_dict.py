#! /usr/bin/env python3

from klassez import *

def save_dict(par, filename):
    with open(filename, 'a') as f:
        f.write('!\n{')
        for key, item in par.valuesdict().items():
            f.write(f'"{key}" : {item}, ')
        f.write('}\n')

