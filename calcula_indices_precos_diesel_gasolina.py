#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import time
import csv
import datetime
import pandas as pd
import numpy as np
import calendar
import pandas as pd
import datetime
import dateutil.relativedelta


def get_ultima_data_disponivel_base(path_file_base):
    # verifica a última data disponível na base
    ultima_data_base = ''
    with open(path_file_base, 'r') as f:
        for row in reversed(list(csv.reader(f))):
            data = row[0].split(';')[0]
            if data == 'Data':
                return None
            data = row[0].split(';')[0]
            return datetime.datetime.strptime(data, '%d/%m/%Y').date()


def get_numpy_array_base(path_file_base):
    df = get_pandas_dataframe_base(path_file_base)
    return df.values


def get_pandas_dataframe_base(path_file_base):
    df = pd.read_csv(path_file_base, sep=';')
    # we use .str to replace and then convert to float
    df['Diesel'] = df.Diesel.str.replace(',', '.').astype(float)
    df['Gasolina'] = df.Gasolina.str.replace(',', '.').astype(float)
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='ignore')
    return df


def filtra_df_por_data(df, start_date, end_date):
    mask = (df['Data'] >= start_date) & (df['Data'] <= end_date)
    df = df.loc[mask]
    all_days = pd.date_range(start_date, end_date, freq='D')
    df.index = pd.DatetimeIndex(df.Data)
    return df.reindex(all_days, fill_value=0)


def calcula_medias_detalhe(data_referencia):
    # calcula o último mês de acordo com a data de referência
    last_month = data_referencia - dateutil.relativedelta.relativedelta(months=1)
    # IGP 10 - do dia 11 mês anterior ao dia 10 do mês de referência
    data_ini_igp_10 = last_month.replace(day=11)
    data_fim_igp_10 = data_referencia.replace(day=10)
    # IGP M - do dia 21 do mês anterior ao dia 20 do mês de referência
    data_ini_igp_m = last_month.replace(day=21)
    data_fim_igp_m = data_referencia.replace(day=20)
    # IGP DI - primeiro e último dia do mês de referência
    data_ini_igp_di = data_referencia.replace(day=1)
    data_fim_igp_di = data_referencia.replace(
        day=calendar.monthrange(
            data_referencia.year, data_referencia.month
        )[1]
    )

    print('DT REF:', data_referencia)
    # data frame com a base de dados
    df = get_pandas_dataframe_base(path_file_base)
    print(df)
    print("\n\n")

    print("-----------------------------------------------")
    print('IGP-10:', data_ini_igp_10, data_fim_igp_10)
    print("-----------------------------------------------")
    df_igp_10 = filtra_df_por_data(df, data_ini_igp_10, data_fim_igp_10)
    print(df_igp_10)
    print('Gasolina média', df_igp_10.Gasolina.mean())
    print('Diesel média', df_igp_10.Diesel.mean())
    print("\n\n")

    print("-----------------------------------------------")
    print('IGP-M: ', data_ini_igp_m, data_fim_igp_m)
    print("-----------------------------------------------")
    df_igp_m = filtra_df_por_data(df, data_ini_igp_m, data_fim_igp_m)
    print(df_igp_m)
    print('Gasolina média', df_igp_m.Gasolina.mean())
    print('Diesel média', df_igp_m.Diesel.mean())
    print("\n\n")

    print("-----------------------------------------------")
    print('IGP-DI:', data_ini_igp_di, data_fim_igp_di)
    print("-----------------------------------------------")
    df_igp_di = filtra_df_por_data(df, data_ini_igp_di, data_fim_igp_di)
    print(df_igp_di)
    print('Gasolina média', df_igp_di.Gasolina.mean())
    print('Diesel média', df_igp_di.Diesel.mean())
    print("\n\n")

    return True


def calcula_medias(data_referencia):
    # calcula o último mês de acordo com a data de referência
    last_month = data_referencia - dateutil.relativedelta.relativedelta(months=1)
    # IGP 10 - do dia 11 mês anterior ao dia 10 do mês de referência
    data_ini_igp_10 = last_month.replace(day=11)
    data_fim_igp_10 = data_referencia.replace(day=10)
    # IGP M - do dia 21 do mês anterior ao dia 20 do mês de referência
    data_ini_igp_m = last_month.replace(day=21)
    data_fim_igp_m = data_referencia.replace(day=20)
    # IGP DI - primeiro e último dia do mês de referência
    data_ini_igp_di = data_referencia.replace(day=1)
    data_fim_igp_di = data_referencia.replace(
        day=calendar.monthrange(
            data_referencia.year, data_referencia.month
        )[1]
    )

    print('DT REF:', data_referencia)
    # data frame com a base de dados
    df = get_pandas_dataframe_base(path_file_base)
    print("\n\n")

    print("-----------------------------------------------")
    print('IGP-10:', data_ini_igp_10, data_fim_igp_10)
    print("-----------------------------------------------")
    df_igp_10 = filtra_df_por_data(df, data_ini_igp_10, data_fim_igp_10)
    print('Gasolina média', df_igp_10.Gasolina.mean())
    print('Diesel média', df_igp_10.Diesel.mean())
    print("\n\n")

    print("-----------------------------------------------")
    print('IGP-M: ', data_ini_igp_m, data_fim_igp_m)
    print("-----------------------------------------------")
    df_igp_m = filtra_df_por_data(df, data_ini_igp_m, data_fim_igp_m)
    print('Gasolina média', df_igp_m.Gasolina.mean())
    print('Diesel média', df_igp_m.Diesel.mean())
    print("\n\n")

    print("-----------------------------------------------")
    print('IGP-DI:', data_ini_igp_di, data_fim_igp_di)
    print("-----------------------------------------------")
    df_igp_di = filtra_df_por_data(df, data_ini_igp_di, data_fim_igp_di)
    print('Gasolina média', df_igp_di.Gasolina.mean())
    print('Diesel média', df_igp_di.Diesel.mean())
    print("\n\n")

    return True

if __name__ == '__main__':
    # verifica a última data disponível na base
    name_file_base = 'ajustes_precos_diesel_e_gasolina_base.csv'
    path_file_base = 'bases/'+name_file_base

    data_referencia = datetime.datetime(2017, 12, 1)
    calcula_medias(data_referencia)

    data_referencia = datetime.datetime(2018, 1, 1)
    calcula_medias(data_referencia)

