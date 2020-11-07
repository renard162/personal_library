"""
Funções de teste de algoritmos de otimização.
Mais funções disponíveis em:
https://www.sfu.ca/~ssurjano/optimization.html

Funções disponíveis:
    Funções de conversão Binário -> Inteiro:
        - bin2int: y = sum(b_n * 2^n)
        - signed_bin2int: y = ((-1)^b_0) * bin2int(b_1...b_n)
        - bin2int_list: y = [signed_bin2int(b_0...b_n), ..., signed_bin2int(b_h...b_N)]

    Funções de teste em domínio contínuo:
        - nan_sphere(x): y=f(x_1...x_n) com NaN para todo x_n<0
        - constant(x): y=-1 para todo x_n
        - sphere(x): y=f(x_1...x_n)
        - rastrigin(x): y=f(x_1...x_n)
        - rosenbrock(x): y=f(x_1...x_n)
        - holder(x): y=f(x_1...x_n)
        - crossintray(x): y=f(x_1...x_n)
        - styblinski_tang(x): y=f(x_1...x_n)
"""
# %%
import numpy as np
import math as mt

#---------------------------------------
#Funções para testar algoritmos de otimização binários
def bin2int(b):
    return int(sum([mt.pow(2,x)*b[::-1][x] for x in range(len(b))]))

def signed_bin2int(b):
    return int(bin2int(b[1:])*(mt.pow(-1,b[0]*(-1))))

def bin2int_list(b, variables_count):
    if ((len(b) % variables_count) != 0):
        raise Exception('Insuficient bits!')
    bits_per_var = len(b)/variables_count
    output_list = []
    final = int(0)
    for i in range(1,variables_count+1):
        init = final
        final += int(bits_per_var)
        output_list.append(signed_bin2int(b[init:final]))
    return output_list
#---------------------------------------

def nan_sphere(x):
    #Sphere function with negative domain as NaN
    total = 0
    for i in range(len(x)):
        if (x[i]<0):
            total = np.nan
        else:
            total += x[i]**2
    return total

def constant(x):
    #Constant plane to test algorithm comportment in
    #an extreme exploration scenario.
    return -1

def sphere(x):
    #Sphere function
    total = 0
    for i in range(len(x)):
        total += x[i]**2
    return total
	
def rastrigin(x):
    #Rastringin function
	return 10*len(x) + sum([(xi**2 - 10 * np.cos(2 * np.pi * xi)) for xi in x])

def rosenbrock(x):
    #Rosenbrock function
	total = 0
	for i in range(len(x)-1):
		total += 100*((x[i]**2 - x[i+1])**2) + (1-x[i])**2
	return total

def holder(x):
    #Holder-Table Function
    product_factor = 1
    sum_factor = 0
    for i in range(len(x)):
        product_factor *= np.cos(x[i]) if (i%2) else np.sin(x[i])
        sum_factor += x[i]**2
    sum_factor = np.exp(np.abs(1 - np.sqrt(sum_factor)/np.pi))
    return (-1)*np.abs(product_factor * sum_factor)

def crossintray(x):
    #Cross-in-tray Function
    product_factor = 1
    sum_factor = 0
    for i in range(len(x)):
        product_factor *= np.sin(x[i])
        sum_factor += x[i]**2
    sum_factor = np.exp(np.abs(100 - np.sqrt(sum_factor)/np.pi))
    return (-0.0001)*((np.abs(product_factor * sum_factor)+1)**0.1)

def styblinski_tang(x):
    #Styblinski-Tang Function
    total = 0
    for i in range(len(x)):
        total += (x[i]**4) - (16*x[i]**2) + (5*x[i])
    return total/2

