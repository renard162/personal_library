# -*- coding: utf-8 -*-
# %%
"""
Funções para manipular arquivos de texto contendo dados.
"""
import numpy as np
import csv

def csv_export(file_name, *lists, titles=None, separator='\t',
               decimal_digit='.', number_format='sci', precision=10):
    """
    Função para salvar em arquivo de texto os dados de listas ou arrays.

    Args:
        file_name (string):
            Nome do arquivo que será criado ou sobrescrito.
            Ex.: 'arquivo.txt'
            
        *lists (1D-Lists ou 1D-arrays):
            Listas ou arrays que formarão as colunas do arquivo de saída.
            Múltiplas listas ou arrays podem ser fornecidas desde que todas
            possuam o mesmo número de elementos.
            
        titles (string-list, optional):
            Lista de strings que serão o título das colunas de dados.
            Opcional de ser fornecido mas, caso seja fornecido, deve conter
            o mesmo número de elementos que o número de listas fornecidas.
            
        separator (string, optional): Defaults to TAB ('\t').
            Caractere que separará as colunas de dados e, caso seja fornecido,
            os títulos das colunas.
            Por padrão adota-se o TAB como separador, porém, se for necessária
            compatibilidade com algum editor de planilhas (Excel, por exemplo)
            em Pt-Br, NÃO utilize vírgula (',') como separador, pois estes
            softwares reconecem a vírgula como separador de casas decimais.
            
        decimal_digit (string, optional): DESCRIPTION. Defaults to '.'.
            Caractere que separará os valores decimais de elementos numéricos.
            Caso não seja fornecido, adota-se o padrão internacional de
            separar os dígitos decimais por ponto, por motivo de compatibilidade
            com outros softwares.
            Caso deseja-se compatibilizar o aqruvo com qualquer editor de
            planilha (Excel, por exemplo) que esteja no padrão Pt-Br, utilizar
            ',' (vírgula) como separador decimal.
            
        number_format (string, optional): Defaults to 'sci'.
            Formato dos dados numéricos de saída.
            Valores válidos são:
                - 'sci' -> Padrão científico (1,000E00).
                - 'dec' -> Padrão decimal (1,000).
                
        precision (int, optional): Defaults to 10.
            Número de casas decimais utilizados em dados numéricos.

    Exemplo de uso:
        dadas as variáveis:
            I1 = [1.32, 2.65, 8.6, 0.7, 5.731]
            
            Vo = [12.0, 10.1, 14.68, 9.8, 7.99]
            
        Deseja-se salvar estes dados em arquivo CSV chamado "dados.csv" para
        utilizar em Excel Pt-Br com os títulos "Corrente de entrada" e
        "Tensão de saída", define-se os títulos:
            titulos = ['Corrente de entrada', 'Tensão de saída']
            
        Aplica-se estes valores na função:
            csv_export('dados.csv', I1, Vo, titles=titulos, decimal_digit=',')

    """
    
    #Checagem dos títulos (caso fornecidos)
    if (titles != None):
        if (np.sum([isinstance(x, str) for x in titles]) != len(titles)):
            raise Exception('Todos os títulos devem ser Strings!')
            
        if (len(titles) != len(lists)):
            raise Exception('O número de títulos é diferente do número de '\
                            'listas fornecidas!')
    
    #Montagem da matriz de dados
    validation = len(lists[0])
    data_matrix = []

    for data in lists:
        if (len(data) != validation):
            raise Exception('Todos os vetores de dados devem ter o mesmo tamanho!')
            
        else:
            try: #Vetor numérico
                data = np.array(data, dtype=float)
                
                str_format = '{:.' + str(precision)
                if (number_format == 'sci'):
                    str_format += 'E}'
                else:
                    str_format += 'f}'
                
                temp_data = [str_format.format(x).replace('.', decimal_digit) \
                             for x in data]
                
            except: #Vetor não numérico
                temp_data = [str(x) for x in data]
            
            finally:
                data_matrix.append(temp_data)
    
    data_matrix = np.array(data_matrix).T.tolist()

    #Escrita no arquivo
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=separator)
        
        if (titles != None):
            writer.writerow(titles)
        
        for line in data_matrix:
            writer.writerow(line)
