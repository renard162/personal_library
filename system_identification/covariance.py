# -*- coding: utf-8 -*-
# %%
"""
Funções para análise de covariância entre séries de dados e correlação entre
séries temporais.
"""
import numpy as np
import scipy.stats as spst

def normalized_covariance(x, y):
    """
    Função utilizada para melhorar a legibilidade dos códigos.

    A função numpy.corrcoef(x,y) retorna a matriz de correlação:
        [[Cii Cij] 
        [Cji Cjj]]
    O que força a se tomar um dos valores da anti-diagonal para se obter o
    valor da covariância entre os dois conjuntos de dados.

    A função scipy.stats.pearsonr(x,y) também retorna a covariância normalizada
    e também o p-value, contudo o nome da função dificulta a leitura de códigos
    mais densos.

    Args:
        x (1D-list ou 1D-array):
            Lista de dados.

        y (1D-list ou 1D-array):
            Lista de dados.

    Returns:
        float:
            Covariância normalizada entre "x" e "y".
            Também conhecido como coeficiente de correlação de Pearson.

    """
    return np.corrcoef(x, y)[0,1]





def correlation(y, u=None, confidence_level=0.95):
    """
    Função de correlação entre as séries temporais "y" e "u" normalizada:
        - Caso y == u -> Autocorrelação
        - Caso y != u -> Correlação Cruzada

    Bibliografia:
        Billings, S.A., 2013. Nonlinear system identification: NARMAX methods
        in the time, frequency, and spatio-temporal domains. John Wiley & Sons.

        Aguirre, L.A., 2007. Introdução à Identificação de Sistemas–Técnicas
        Lineares e Não-Lineares Aplicadas a Sistemas Reais. Editora UFMG.

    Args:
        y (1D-list ou 1D-array):
            Série temporal do sinal 1.

        u (1D-list ou 1D-array, optional):
            Série temporal do sinal 2.
            Caso não seja fornecida, retorna a autocorrelação de "y",
            caso seja fornecida, retorna a correlação cruzada entre "y" e "u".

        confidence_level (float, optional): Defaults = 0.95
            Coeficiente de confiança de r_yu = 0.

    Returns:
        ryu (1D-array):
            Correlação entre "y" e "u".

        t (1D-array):
            Vetor de atrasos (tau).
            No caso da Correlação cruzada, atrasos negativos representam
            atraso em "y" e atrasos positivos representam atrasos em "u".

        limit_inferior (float):
            Limite inferior do intervalo de confiança.

        limit_superior (float):
            Limite superior do intervalo de confiança.
    """
    y = np.array(y)
    u = np.array(u)

    t = np.arange(-1*(len(y)-1), len(y))

    #Correção para usar na função de correlação do numpy.
    y_temp = y - np.mean(y)

    #Na correlação cruzada entre "y" e "u", valores na metade esquerda do
    #gráfico representam atrasos aplicados em "y", enquanto o lado direito do
    #gráfico representa atrasos aplicados em "u", por esta simetria, no caso
    #da auto-correlação é tomada apenas a metade direita do gráfico. (t_0)
    if (u.ndim < 1): #Auto-correlação
        u = y
        u_temp = y_temp
        t_0 = int(len(t) / 2)

    else: #Correlação cruzada
        u_temp = u - np.mean(u)
        t_0 = 0

    #Função de correlação adotada pelo Billings:
    #Considerando-se x_m e y_m como a média de x e y respectivamente:
    #np.correlate(x_temp, y_temp) = sum_k{(x(k) - x_m)*(y(k+t) - y_m)}
    #Assim, np.correlate(x_temp, y_temp)/len(x) = covariância(x(k), y(k+t))
    #Normaliza-se com sqrt(variância(x) * variância(y))
    ryu = np.correlate(y_temp, u_temp, mode='full') / \
        (np.sqrt(np.var(y)*np.var(u))*len(y))

    #Limites = (+ ou -) Z_Score(confianca) / sqrt(N)
    #Onde N é o número total de amostras.
    confidence_interval = np.array(spst.norm.interval(confidence_level)) / np.sqrt(len(y))

    return ryu[t_0:], t[t_0:], confidence_interval[0], confidence_interval[-1]




if (__name__ == '__main__'):
    import matplotlib.pyplot as plt

    x = np.linspace(-1, 1, 50)
    y = lambda x: 0.31*x**2 + 0.61*x + np.random.rand(len(x))

    print('\nCorrelacao: {:0.4f}'.format(normalized_covariance(x, y(x))))

    corr, t, inf, sup = correlation(x, y(x))
    plt.figure()
    plt.plot(t, corr, 'b-.')
    plt.hlines(inf, t[0], t[-1], colors='black', linestyles='dotted')
    plt.hlines(sup, t[0], t[-1], colors='black', linestyles='dotted')
    plt.grid(True)
    plt.show()
