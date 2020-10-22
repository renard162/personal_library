"""
Função que gera uma lista com listas contendo todas as combinações de inteiros,
com "positions" posições onde a soma dos valores resulta de "0" até "value".

Fonte: Stack Overflow (Nico Schlömer)
https://stackoverflow.com/questions/45348038/variable-number-of-dependent-nested-loops/45348441#45348441
"""

import numpy as np

def partitions(value, positions, depth=0):
    if positions == depth:
        return [[]]
    return [
        item + [i]
        for i in range(value+1)
        for item in partitions(value-i, positions, depth=depth+1)
        ]
        