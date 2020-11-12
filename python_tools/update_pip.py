# -*- coding: utf-8 -*-
import os
import csv
import time
import numpy as np
from tqdm import tqdm

with open('pip_update.log', 'w', newline='') as file:
    csvwrite = csv.writer(file, delimiter='\t')
    try:
        with open('conda_list.log', 'w') as file:
            for _ in tqdm(range(1), desc='Coletando lista', ascii=True):
                pack_string = os.popen('conda list --export').read()
                file.write(pack_string)
                packages = np.loadtxt('conda_list.log', delimiter='=',\
                                      comments='#', dtype=object)

        if (len(packages) > 0):
            log = ['Conda List', 'OK']
            csvwrite.writerow(log)
        else:
            raise Exception()

    except:
        log = ['Conda List', 'Error getting list!']
        csvwrite.writerow(log)

    time.sleep(1)

    try:
        if (len(packages[packages[:,2]=='pypi_0']) < 1):
            raise Exception()
        for pack in tqdm(packages[packages[:,2]=='pypi_0'],\
                          desc='PIP update', ascii=True):
            log = os.popen('pip install -U ' + pack[0]).read()
            csvwrite.writerow([pack[0], log])

    except:
        log = ['PIP Update', 'No package to update!']
        csvwrite.writerow(log)

    finally:
        time.sleep(1)
        log = ['Log File', 'Finished']
        csvwrite.writerow(log)

