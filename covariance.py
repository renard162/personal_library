# -*- coding: utf-8 -*-
"""
Funções para análise de covariância entre séries de dados e correlação entre
séries temporais.
"""
import numpy as np
from scipy import stats as spst

def normalized_covariance(x, y):
    """
    Função utilizada para melhorar a legibilidade dos códigos.
    
    A função numpy.corrcoef(x,y) retorna a matriz de correlação:
        [Cii Cij]
        [Cji Cjj]
    O que força a se tomar um dos valores da anti-diagonal para se obter o
    valor da covariância entre os dois conjuntos de dados.
    
    A função scipy.stats.pearsonr(x,y) também retorna a covariância normalizada
    e também o p-value, contudo o nome da função dificulta a leitura de códigos
    mais densos.

    Args:
        x (1D-list ou 1D-array): Lista de dados.
        y (1D-list ou 1D-array): Lista de dados.

    Returns:
        float: Covariância normalizada entre "x" e "y".

    """
    return np.corrcoef(x, y)[0,1]



def correlation(y, u, confidence_level=0.95):
    """
    Função de correlação entre as séries temporais "y" e "u" normalizada:
        - Caso y == u -> Autocorrelação
        - Caso y != u -> Correlação Cruzada
    
    Bibliografia:
        Billings, S.A., 2013. Nonlinear system identification: NARMAX methods
        in the time, frequency, and spatio-temporal domains. John Wiley & Sons.
        
        Aguirre, L.A., Introdução à Identificação de Sistemas–Técnicas Lineares
        e Não-Lineares Aplicadas a Sistemas Reais. Editora UFMG.

    Args:
        y (1D-list ou 1D-array): Série temporal do sinal 1.
        
        u (1D-list ou 1D-array): Série temporal do sinal 2.
        
        confidence_level (float, optional): Defaults = 0.95
            Coeficiente de confiança de r_yu = 0.

    Returns:
        ryu (1D-array): Correlação entre "y" e "u".
        superior_limit (float): Limite superior do intervalo de confiança.
        inferior_limit (float): Limite inferior do intervalo de confiança.

    """
    y = np.array(y)
    u = np.array(u)
    
    #Após a metade da amostragem o valor da média pode divergir pois valores
    #são eliminados durante o cálculo, assim os resultados podem se tornar
    #inconsistentes e, portanto, a correlação é calculada apenas até a metade
    #do tempo total amostrado.
    t_max = int(len(y) / 2)
    
    ryu = np.zeros(t_max)
    
    y = y - np.mean(y)
    u = u - np.mean(u)
    #Função de correlação adotada pelo Billings
    ryu[0] = np.sum(y*u) / (np.sqrt(np.sum(y*y)) * np.sqrt(np.sum(u*u)))
    
    for t in range(1, t_max):
        y = y - np.mean(y[:-t])
        u = u - np.mean(u[t:])
        ryu[t] = np.sum(y[:-t]*u[t:]) / \
            (np.sqrt(np.sum(y[:-t]*y[:-t])) * np.sqrt(np.sum(u[t:]*u[t:])))
    
    
    #Limites = (+ ou -) Z_Score(confianca) / sqrt(N)
    #Onde N é o número total de amostras.
    limit_superior = spst.norm.ppf(1-((1-confidence_level)/2)) / np.sqrt(len(y))
    limit_inferior = limit_superior * (-1)
    
    return ryu, limit_superior, limit_inferior
