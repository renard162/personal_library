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
    
    Obs.: Esta versão da função utiliza uma versão do "numpy.fromstring" que
          gera um DeprecationWarning, em versões futuras do numpy, quando o
          "numpy.fromstring" gerar um Exception, será necessário atualizar
          esta função.
    
    Args:
        file_name (str): Nome do arquivo com os dados a serem importados.
                         Ex.: 'dados.txt'

    Returns:
        final_table_list (TYPE): Lista de arrays com os dados separados por "step".
    """
    with open(file_name, 'r') as file:
        final_table_list = []
        temp_table_data = []
        table_count = 0
        valid_line = False
        
        for line in file:
            line_data = np.fromstring(line, dtype=float, sep='\t')
            
            #Quando "numpy.fromstring" gerar exception, substituir o "if" "else"
            #por "try" "except".
            if (len(line_data) > 0):
                valid_line = True
                temp_table_data.append(line_data)
            else:
                if valid_line:
                    final_table_list.append(np.vstack(temp_table_data))
                    temp_table_data = []
                    table_count += 1
                valid_line = False
                
        final_table_list.append(np.vstack(temp_table_data))
        
    return final_table_list
