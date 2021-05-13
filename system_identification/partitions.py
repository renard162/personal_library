# -*- coding: utf-8 -*-
# %%

def partitions(value, positions, depth=0):
    """
    Gera uma lista de listas contendo todas as combinações de inteiros, com
    "positions" posições onde a soma dos valores resulta de "0" até "value".
    
    Fonte:
    Stack Overflow (Nico Schlömer) - 
    https://stackoverflow.com/questions/45348038/variable-number-of-dependent-nested-loops/45348441#45348441

    Args:
        value (int):
            Valor máximo da soma de todos os elementos da lista.
        
        positions (int):
            Número de elementos de cada lista.
        
        depth (int, Não utilizar):
            Variável interna de recursividade, não utilizar.

    Returns:
        2D-list:
            Lista com as listas onde a soma dos elementos de cada uma resulta
            valores entre 0 e "value".

    """
    if positions == depth:
        return [[]]
    return [
        item + [i]
        for i in range(value+1)
        for item in partitions(value-i, positions, depth=depth+1)
        ]



if (__name__ == '__main__'):
    import numpy as np
    data = partitions(value=3,
                      positions=5)
    print('\nPartition de 3 em 5 posições:\n{}'.format(np.matrix(data)))
