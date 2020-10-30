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
            
        *lists (múltiplas 1D-lists ou uma única list-lists):
            Listas ou arrays que formarão as colunas do arquivo de saída.
            
            Múltiplas listas ou arrays podem ser fornecidas desde que todas
            possuam o mesmo número de elementos.
            Esta forma de utilização facilita exportar dados simples.
            
            Caso seja fornecida uma lista de listas, essa deve ser fornecida
            única. A função não suporta múltiplas listas de listas.
            Esta forma de utilização facilita exportar dados em grandes
            quantidades, gerados em massa e organizados proceduralmente.
            
        titles (string-list, optional):
            Lista de strings que serão o título das colunas de dados.
            Opcional de ser fornecido mas, caso seja fornecido, deve conter
            o mesmo número de elementos que o número de listas fornecidas.
            
        separator (string, optional): Defaults to TAB ('\t').
            Caractere que delimitará as colunas de dados e, caso seja
            fornecido, os títulos das colunas.
            Por padrão adota-se o TAB como separador, porém, se for necessária
            compatibilidade com algum editor de planilhas (Excel, por exemplo)
            em Pt-Br, NÃO utilize vírgula (',') como separador, pois estes
            softwares reconecem a vírgula como separador de casas decimais.
            
        decimal_digit (string, optional): Defaults to '.'.
            Caractere que separará os valores decimais de elementos numéricos.
            Caso não seja fornecido, adota-se o padrão internacional de
            separar os dígitos decimais por ponto, por motivo de compatibilidade
            com outros softwares.
            Caso deseja-se compatibilizar o aqruvo com qualquer editor de
            planilha (Excel, por exemplo) que esteja no padrão Pt-Br, utilizar
            ',' (vírgula) como separador decimal.
            Este caractere deve ser diferente do delimitador de colunas
            'separator' para evitar conflitos.
            
        number_format (string, optional): Defaults to 'sci'.
            Formato dos dados numéricos de saída.
            Valores válidos são:
                - 'sci' -> Padrão científico (1,000E00).
                - 'dec' -> Padrão decimal (1,000).
                - Qualquer string diferente das anteriores farão os dados 
                  numéricos serem salvos como o padrão do python.
                
        precision (int, optional): Defaults to 10.
            Número de casas decimais utilizados em dados numéricos.

    Exemplo de uso 1 (múltiplas listas 1D fornecidas):
        Dadas as variáveis:
            I1 = [1.32, 2.65, 8.6, 0.7, 5.731]
            
            Vo = [12.0, 10.1, 14.68, 9.8, 7.99]
            
        Deseja-se salvar estes dados em arquivo CSV chamado "dados.csv" para
        utilizar em Excel Pt-Br com os títulos "Corrente de entrada" e
        "Tensão de saída", assim, define-se os títulos:
            titulos = ['Corrente de entrada', 'Tensão de saída']
            
        Aplica-se estes valores na função:
            csv_export('dados.csv', I1, Vo, titles=titulos, decimal_digit=',')
    
    Exemplo de uso 2 (Lista de listas única fornecida):
        Dada a matriz de dados:
            M = [[0.25, 0.6, 0.15], [35, 42, 15]]
            
        Onde os dados da primeira lista representa "Rendimento" e da segunda
        lista representa "Temperatura", deseja-se salvar estes dados em
        arquivo "experimento.dat" para ser utilizado em Excel Pt-Br com as
        colunas devidamente nomeadas e separadas por ";".
        Então cria-se o vetor de títulos das colunas:
            titulos = ['Rendimento', 'Temperatura']
        
        Então executa-se a função:
            csv_export('experimento.dat', M, titles=titulos, separator=';',
            decimal_digit=',')

    """
    #Checagem do tipo de entrada:
    #n-listas: dimensions = 2
    #lista de listas: dimensions = 3
    dimensions = np.array(lists, dtype=object).ndim
    if dimensions == 3:
        lists = lists[0]

    #Checagem dos títulos (caso fornecidos)
    if (titles != None):
        if (np.sum([isinstance(x, str) for x in titles]) != len(titles)):
            raise Exception('Todos os títulos devem ser Strings!')
            
        if (len(titles) != len(lists)):
            raise Exception('O número de títulos é diferente do número de '\
                            'listas fornecidas!')
                
    #Checagem de conflito entre separador decimal e delimitador de colunas.
    if (separator == decimal_digit):
        raise Exception('O caractere delimitador de colunas \'separator\' '\
                        'deve ser diferente do caractere separador decimal '\
                        '\'decimal_digit\'!')
    
    #Como é esperado que o número de amostras seja muito, muito maior que o
    #número de listas, excutar a checagem da validade das listas antes de
    #processar seus elementos aumenta o desempenho do código.
    data_length = len(lists[0])
    for data in lists:
        if (len(data) != data_length):
            raise Exception('Todos os vetores de dados devem ter o mesmo tamanho!')
    
    #Montagem da matriz de dados
    data_matrix = []
    for data in lists:
        try: #Vetor numérico
            str_format = '{:.' + str(precision)
            if (number_format == 'sci'):
                str_format += 'E}'
            elif (number_format == 'dec'):
                str_format += 'f}'
            else: #Vetores numéricos tratados como vetores genéricos
                raise Exception()
                
            data = np.array(data, dtype=float)
            
            temp_data = [str_format.format(x).replace('.', decimal_digit) \
                         for x in data]
            
        except: #Vetor genérico
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
