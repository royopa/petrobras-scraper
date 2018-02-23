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
            return datetime.datetime.strptime(data[0:10], '%d/%m/%Y').date()
            # return datetime.datetime.strptime(data[0:10], '%Y-%m-%d').date()


if __name__ == '__main__':
    # verifica a última data disponível na base 
    # name_file_base = 'ajustes_precos_diesel_e_gasolina_base.csv'
    name_file_base = 'indices_diesel_e_gasolina_base.csv'
    path_file_base = 'bases/'+name_file_base
    ultima_data_base = get_ultima_data_disponivel_base(path_file_base)
    print('Última data base disponível:', ultima_data_base)

    # pega a base de preços para geração dos indíces
    name_file_base_precos = 'precos_medios_diesel_e_gasolina_base.csv'
    path_file_base_precos = 'bases/'+name_file_base_precos
    df = pd.read_csv(path_file_base_precos, sep=';')

    start_date = datetime.datetime(2017, 1, 1)
    all_days = pd.date_range(start_date, datetime.datetime.now(), freq='D')
    df.index = pd.DatetimeIndex(df.Data)
    #df = df.reindex(all_days, fill_value=0)
    
    # converte um dataframe para numpy array
    np_base_precos = df.values
    # pega todas as linhas da segunda coluna do dataframe
    np_precos_diesel = np_base_precos[:, 1]
    # pega todas as linhas da terceira coluna do dataframe
    np_precos_gasolina = np_base_precos[:, 2]

    # calcula os retornos com base nos preços
    df['preco_diesel'] = df.Diesel.str.replace(',', '.').astype(float)
    df['preco_gasolina'] = df.Gasolina.str.replace(',', '.').astype(float)
    
    df['ret_diesel'] = ((df.preco_diesel / df.preco_diesel.shift(1))-1)*100
    df['ret_diesel'] = df['ret_diesel'].round(1)
    
    df['ret_gasolina'] = ((df.preco_gasolina / df.preco_gasolina.shift(1))-1)*100
    df['ret_gasolina'] = df['ret_gasolina'].round(1)

    '''
    # calcula os retornos com base nos preços
    df['ret_perc_diesel'] = ((df.Diesel / df.Diesel.shift(1))-1)*100
    df['ret_perc_diesel'] = df['ret_perc_diesel'].round(4)
    df['ret_val_diesel'] = (df.Diesel - df.Diesel.shift(1))
    df['ret_val_calculado_diesel'] = ((df.Diesel * df.ret_perc_diesel)/100)
    df['ret_log_diesel'] = (np.log(df.Diesel) - np.log(df.Diesel.shift(1)))
    df['val_calculado_diesel'] = (df.Diesel.shift(-1) - (df.ret_val_calculado_diesel.shift(-1)))
    df['val_calculado_diesel'] = df['val_calculado_diesel'].round(4)


    df['ret_perc_gasolina'] = ((df.Gasolina / df.Gasolina.shift(1))-1)*100
    df['ret_perc_gasolina'] = df['ret_perc_gasolina'].round(4)
    # calcula o valor da diferenca em valor em relação ao dia anterior
    df['ret_val_gasolina'] = (df.Gasolina - df.Gasolina.shift(1))
    # calcula o valor da diferenca em valor em relação ao dia anterior
    # usando o retorno percentual
    df['ret_val_calculado_gasolina'] = ((df.Gasolina - df.ret_perc_gasolina)/100)
    # calcula os retornos logarítmos
    df['ret_log_gasolina'] = (np.log(df.Gasolina) - np.log(df.Gasolina.shift(1)))
    # calcula o preço do dia, baseado no praço do dia posterior e retorno do preço posterior
    df['val_calculado_gasolina'] = (df.Gasolina.shift(-1) - (df.ret_val_calculado_gasolina.shift(-1)))

    writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    '''

    rows_to_insert = []

    for index, row in df.iterrows():
        # pula os registros que já estão na base
        data = datetime.datetime.strptime(row['Data'], '%d/%m/%Y').date()
        if (data <= ultima_data_base):
            continue

        row_inserted = {
            'Data': row['Data'],
            'Gasolina': row['ret_gasolina'],
            'Diesel': row['ret_diesel'],
            'indice_gasolina': '',#row['indice_gasolina'],
            'indice_diesel': '',#row['indice_diesel']
        }
        rows_to_insert.append(row_inserted)

    # faz o append no csv
    with open(path_file_base, 'a', newline='') as baseFile:
        fieldnames = ['Data', 'Gasolina', 'Diesel', 'indice_gasolina', 'indice_diesel']
        writer = csv.DictWriter(baseFile, fieldnames=fieldnames, delimiter=';')
        for row_inserted in rows_to_insert:
            writer.writerow(row_inserted)
            print('Dado inserido no arquivo base:', row_inserted)    

    print(rows_to_insert)

    # depois de inserir os dados é necessário recalcular o valor base 100
    df = pd.read_csv(path_file_base, sep=';')
    df['data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='ignore')
    df['indice_gasolina'] = (df['indice_gasolina'].shift(1) * df.Gasolina / 100) + df['indice_gasolina'].shift(1)
    df['indice_diesel'] = (df['indice_diesel'].shift(1) * df.Diesel / 100) + df['indice_diesel'].shift(1)

    start_date = datetime.datetime(2017, 1, 1)
    all_days = pd.date_range(start_date, datetime.datetime.now(), freq='D')
    df.index = pd.DatetimeIndex(df.Data)
    df = df.reindex(all_days, fill_value=0)

    writer = pd.ExcelWriter(path_file_base+'.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()        
