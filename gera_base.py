#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import time
import csv
import datetime
import pandas as pd
import numpy as np


if __name__ == '__main__':
    name_file_base = 'indices_diesel_e_gasolina_base.csv'
    path_file_base = 'bases/'+name_file_base
    # começa a fazer os cálculos para o arquivo base
    df = pd.read_csv(path_file_base, sep=';')
    # we use .str to replace and then convert to float
    df['data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='ignore')
    df['indice_gasolina'] = (df['indice_gasolina'].shift(1) * df.Gasolina / 100) + df['indice_gasolina'].shift(1)
    df['indice_diesel'] = (df['indice_diesel'].shift(1) * df.Diesel / 100) + df['indice_diesel'].shift(1)

    start_date = datetime.datetime(2017, 1, 1)
    all_days = pd.date_range(start_date, datetime.datetime.now(), freq='D')
    df.index = pd.DatetimeIndex(df.Data)
    df = df.reindex(all_days, fill_value=0)

    writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    
    quit()

