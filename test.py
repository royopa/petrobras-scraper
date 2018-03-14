import time
import csv
import datetime
import pandas as pd
import numpy as np
import dateutil.relativedelta
import calendar
from datetime import date
from dateutil.rrule import rrule
from dateutil.rrule import MONTHLY


def get_pandas_dataframe_base(path_file_base):
    df = pd.read_csv(path_file_base, sep=';')
    df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d', errors='ignore')
    return df


def filtra_df_por_data(df, start_date, end_date):
    mask = (df['data'] >= start_date) & (df['data'] <= end_date)
    return (df.loc[mask])


def get_datas_by_indice(data_referencia, indice = ""):
    # calcula o último mês de acordo com a data de referência
    last_month = data_referencia - dateutil.relativedelta.relativedelta(months=1)
   
    if (indice == "10"):
        # IGP 10 - do dia 11 mês anterior ao dia 10 do mês de referência
        return {
            'start_date': last_month.replace(day=11),
            'end_date': data_referencia.replace(day=10)
        }
    
    if (indice == "m"):
        # IGP M - do dia 21 do mês anterior ao dia 20 do mês de referência
        return {
            'start_date': last_month.replace(day=11),
            'end_date': data_referencia.replace(day=10)
        }
        data_ini_igp_m = last_month.replace(day=21)
        data_fim_igp_m = data_referencia.replace(day=20)        
    

    if (indice == "di"):
        # IGP DI - primeiro e último dia do mês de referência
        end_date = data_referencia.replace(
            day=calendar.monthrange(
                data_referencia.year, data_referencia.month
            )[1]
        )
        
        return {
            'start_date': data_referencia.replace(day=1),
            'end_date': end_date
        }
    
    return False


if __name__ == '__main__':
    name_file_base = 'saida_indices_diesel_e_gasolina_base.csv'
    path_file_base = 'bases/'+name_file_base
    df = get_pandas_dataframe_base(path_file_base)

    for data_referencia in rrule(MONTHLY, dtstart=date(2017, 3, 1), until=date.today()):
        get_datas_by_indice(data_referencia, indice = "10")
        get_datas_by_indice(data_referencia, indice = "m")
        get_datas_by_indice(data_referencia, indice = "di")

        for indice in ['10', 'm', 'di']:
            print(indice)
            print(get_datas_by_indice(data_referencia, indice=indice))
            
            start_date = get_datas_by_indice(data_referencia, indice=indice)['start_date']
            end_date = get_datas_by_indice(data_referencia, indice=indice)['end_date']

            df_filtered = filtra_df_por_data(df, start_date, end_date)
            print(df_filtered)
