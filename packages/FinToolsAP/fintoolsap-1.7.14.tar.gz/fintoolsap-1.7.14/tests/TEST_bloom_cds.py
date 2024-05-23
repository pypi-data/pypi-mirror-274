import os
import sys
import time
import numpy
import pandas
import pathlib
import datetime
import functools
import matplotlib.pyplot as plt

# add source directory to path
sys.path.insert(0, '../src/FinToolsAP/')

import LaTeXBuilder
import LocalDatabase
import PortfolioSorts
import UtilityFunctions

# set printing options
import shutil
pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', shutil.get_terminal_size()[0])
pandas.set_option('display.float_format', lambda x: '%.3f' % x)

# directory for loacl wrds database
LOCAL_DB = pathlib.Path('/home/andrewperry/Documents')

def main():
    

    data_path = pathlib.Path('/home/andrewperry/Nextcloud/Research/Bank Elasticity')

    DB = LocalDatabase.LocalDatabase(save_directory = data_path, database_name = 'BankElasticityDB') 

    cds_df = DB.queryDB('Bloomberg.CDS')

    # remove due to data avalibilty
    cds_df = cds_df[~cds_df.id.isin(['citibank', 'firstcitizens'])]

    # remove usb data pre 2010
    ubs_df = cds_df[cds_df.id == 'usb']
    cds_df = cds_df[~cds_df.id.isin(['usb'])]
    ubs_df = ubs_df[ubs_df.date >= datetime.datetime(2010, 1, 1)]
    cds_df = pandas.concat([cds_df, ubs_df])

    alm_df = DB.queryDB('UBPR.BSP', 
                    idrssd = list(cds_df.idrssd.unique()), 
                    all_vars = True)
    
    jpm_alm_df = alm_df[alm_df.idrssd == 852218]
    jpm_cds_df = cds_df[cds_df.idrssd == 852218]

    min_date = jpm_cds_df.date.min()
    max_date = jpm_cds_df.date.max()
    jpm_alm_df = jpm_alm_df[(jpm_alm_df.date >= min_date) & (jpm_alm_df.date <= max_date)]
    jpm_alm_df = jpm_alm_df.drop(columns = ['?'])

    jpm_alm_df = jpm_alm_df.ffill()

    jpm_alm_df = jpm_alm_df.dropna(axis = 1, how = 'any')

    n_unique = jpm_alm_df.nunique()
    cols_to_drop = n_unique[n_unique == 1].index
    jpm_alm_df = jpm_alm_df.drop(cols_to_drop, axis = 1)

    pca_col = list(jpm_alm_df.columns)
    pca_col.remove('date')

    pca_res = UtilityFunctions.pca(X = jpm_alm_df, vr = pca_col)

    jpm_alm_df['idrssd'] = 852218

    print(pca_res)




if __name__ == '__main__':
    main()