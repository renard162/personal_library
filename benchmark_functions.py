"""
Funções de teste de algoritmos de otimização.
"""

import numpy as np


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

