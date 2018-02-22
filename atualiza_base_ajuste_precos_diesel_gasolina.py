#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import time
import csv
import datetime
import pandas as pd
import numpy as np


def get_ultima_data_disponivel_base(path_file_base):
    # verifica a última data disponívl na base
    ultima_data_base = ''
    with open(path_file_base, 'r') as f:
        for row in reversed(list(csv.reader(f))):
            data = row[0].split(';')[0]
            if data == 'Data':
                return None
            data = row[0].split(';')[0]
            return datetime.datetime.strptime(data, '%d/%m/%Y').date()


if __name__ == '__main__':
    # verifica a última data disponível na base 
    path_file_base = 'ajustes_precos_diesel_e_gasolina_base.csv'
    ultima_data_base = get_ultima_data_disponivel_base(path_file_base)
    print('Última data base disponível:', ultima_data_base)
    if (ultima_data_base is None):
        ultima_data_base = datetime.date(1900, 1, 1)

    # pega a base de preços para geração dos indíces
    path_file_base_precos = 'precos_medios_diesel_e_gasolina_base.csv'
    df = pd.read_csv(path_file_base_precos, sep=';')
    # we use .str to replace and then convert to float
    df['Diesel'] = df.Diesel.str.replace(',', '.').astype(float)
    df['Gasolina'] = df.Gasolina.str.replace(',', '.').astype(float)
    
    # printa os n elementos do dataframe df.head(n)
    #print(df['Diesel'])

    # converte um dataframe para numpy array
    np_base_precos = df.values
    # pega todas as linhas da segunda coluna do dataframe
    np_precos_diesel = np_base_precos[:, 1]
    # pega todas as linhas da terceira coluna do dataframe
    np_precos_gasolina = np_base_precos[:, 2]

    # calcula os retornos com base nos preços
    df['ret_diesel'] = ((df.Diesel / df.Diesel.shift(1))-1)*100
    df['ret_diesel'] = df['ret_diesel'].round(1)
    
    df['ret_gasolina'] = ((df.Gasolina / df.Gasolina.shift(1))-1)*100
    df['ret_gasolina'] = df['ret_gasolina'].round(1)
    
    rows_to_insert = []

    for index, row in df.iterrows():
        if (datetime.datetime.strptime(row['Data'], '%d/%m/%Y').date() <= ultima_data_base):
            continue

        row_inserted = {
            'Data': row['Data'],
            'Gasolina': str(row['ret_gasolina']).replace('.', ','),
            'Diesel': str(row['ret_diesel']).replace('.', ',')
        }
        rows_to_insert.append(row_inserted)
        
    print(rows_to_insert)

    # faz o append no csv
    with open(path_file_base, 'a', newline='') as baseFile:
        fieldnames = ['Data', 'Gasolina', 'Diesel']
        writer = csv.DictWriter(baseFile, fieldnames=fieldnames, delimiter=';')
        for row_inserted in rows_to_insert:
            writer.writerow(row_inserted)
            print('Dado inserido no arquivo base:', row_inserted)