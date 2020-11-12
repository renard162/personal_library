# -*- coding: utf-8 -*-
# %%
"""
Pacote com funções para compatibilizar os arquivos de saída do LtSpice com o Python.
"""
import numpy as np

def step_import(file_name: str):
    """
    Importa arquivos gerados pelo LtSpice com a função ".step" separando cada
    passo em uma lista independente, organizando os dados em uma lista de
    matrizes (arrays).
    
    Como cada "step" pode gerar números diferentes de pontos experimentais,
    são geradas listas de 2D-arrays e não simplesmente 3D-arrays.
    
    Caso não seja utilizada a função "step" do LtSpice, a lista resultante
    desta função possuirá apenas um array.
    
    Obs.:
        Esta versão da função utiliza uma versão do "numpy.fromstring" que
        gera um DeprecationWarning. Em versões futuras do numpy, quando o
        "numpy.fromstring" gerar um Exception, será necessário atualizar esta
        função.
    
    Args:
        file_name (str): 
            Nome do arquivo com os dados a serem importados. 
            Ex.: 'dados.txt'

    Returns:
        final_table_list (list):
            Lista de arrays com os dados separados por "step".
    """
    with open(file_name, 'r') as file:
        final_table_list = []
        temp_table_data = []
        valid_line = False
        
        for line in file:
            line_data = np.fromstring(line, dtype=float, sep='\t')
            
            #Quando "numpy.fromstring" gerar exception, substituir o
            #"if" "else" por "try" "except" e colocar a atribuição de
            #"line_data" dentro do "try".
            if (len(line_data) > 0):
                valid_line = True
                temp_table_data.append(line_data)
            else:
                if valid_line:
                    final_table_list.append(np.vstack(temp_table_data))
                    temp_table_data = []
                valid_line = False
                
        final_table_list.append(np.vstack(temp_table_data))
        
    return final_table_list
