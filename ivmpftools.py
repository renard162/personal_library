"""
Funções para operações com intervalos do tipo ivmpf (mpmath).
"""

import numpy as np
import mpmath as mp

def ivmpf_disassembler(ivmpf):
    """
    Converte um intervalo "iv.mpf" ou uma lista/array de intervalos "iv.mpf" em
    um array de números no formato "mp.mpf", dessa forma os valores podem ser
    aplicados em outras funções, inclusive em plots, ou mesmo convertido em
    float -> string (por meio das funções float()->str() ou float()->format())
    para ser utilizado em outras funções do código.

    Args:
        ivmpf (iv.mpf ou lista/array de iv.mpf): Intervalo/s de entrada.

    Returns:
        TYPE: Array de mp.mpf.
            - 1D-array = [<inferior>, <superior>]
              caso seja fornecido "iv.mpf".
              
            - 2D-array = [[<inferior_0>, <superior_0>] ... [<inferior_n>, <superior_n>]]
              caso seja fornecido [<iv.mpf>, ..., <iv.mpf>].
    """
    try:
        elements_count = len(ivmpf)
        output = []
        for i in range(elements_count):
            output.append(ivmpf_disassembler(ivmpf[i]))
        return np.array(output, dtype=object)
    except:
        ivmpf = str(ivmpf)[1:-1].replace(' ','')
        sep_position = ivmpf.find(',')
        return np.array([mp.mpf(ivmpf[:sep_position]), mp.mpf(ivmpf[sep_position+1:])])

