# -*- coding: utf-8 -*-
import os
import csv
import time
import numpy as np
from tqdm import tqdm

update_log = []
try:
    with open('conda_list.log', 'w') as file:
        for _ in tqdm(range(1), desc='Coletando lista', ascii=True):
            pack_string = os.popen('conda list --export').read()
            file.write(pack_string)
            packages = np.loadtxt('conda_list.log', delimiter='=',\
                                  comments='#', dtype=object)

    if (len(packages) > 0):
        update_log.append(['Conda List', 'OK'])
    else:
        raise Exception()

except:
    update_log.append(['Conda List', 'Error getting list!'])

time.sleep(1)

try:
    if (len(packages[packages[:,2]=='pypi_0']) < 1):
        raise Exception()
    for pack in tqdm(packages[packages[:,2]=='pypi_0'],\
                     desc='PIP update', ascii=True):
        log = os.popen('pip install -U ' + pack[0]).read()
        update_log.append([pack[0], log])

except:
    update_log.append(['PIP Update', 'No package to update!'])

finally:
    time.sleep(1)
    
    with open('pip_update.log', 'w', newline='') as file:
        csvwrite = csv.writer(file, delimiter='\t')
        for log in tqdm(update_log, desc='Escrevendo log', ascii=True):
            csvwrite.writerow(log)
        csvwrite.writerow(['Log File', 'OK'])


