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
    # converte os dados do dataframe
    df['data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='ignore')
    del df['Data']

    count_nan = sum(pd.isnull(df['indice_gasolina']))
    while count_nan > 0:
        df['indice_gasolina'] = df['indice_gasolina'].fillna(value=(df['indice_gasolina'].shift(1) * df.Gasolina / 100) + df['indice_gasolina'].shift(1))
        df['indice_diesel'] = df['indice_gasolina'].fillna(value=(df['indice_diesel'].shift(1) * df.Diesel / 100) + df['indice_diesel'].shift(1))    
        count_nan -= 1

    saida_path_file_base = 'bases/saida_'+name_file_base
    df.to_csv(saida_path_file_base, sep='\t', encoding='utf-8')
    quit()

    writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()