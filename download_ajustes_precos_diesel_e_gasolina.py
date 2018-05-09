#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import time
import tabula
import csv
import datetime
import os

def get_ultima_data_disponivel_base(path_file_base):
    # verifica a última data disponívl na base
    ultima_data_base = ''
    with open(path_file_base, 'r') as f:
        for row in reversed(list(csv.reader(f))):
            data = row[0].split(';')[0]
            return datetime.datetime.strptime(data, '%d/%m/%Y').date()


def download_file(url, path_file):
    response = requests.get(url)
    with open(path_file, 'wb') as f:
        f.write(response.content)
    f.close()


def remove_old_files():
    file_list = os.listdir(r"downloads")
    for file_name in file_list:
        if not file_name.startswith('ajustes_precos_diesel_e_gasolina_'):
            continue
        today = datetime.datetime.now().strftime('%d.%m.%Y')
        data_arquivo = file_name.split('ajustes_precos_diesel_e_gasolina_')[-1][-20:][0:10]
        if today != data_arquivo:
            os.remove(os.path.join('downloads', file_name))


if __name__ == '__main__':
    remove_old_files()
    # verifica a última data disponível na base 
    name_file_base = 'ajustes_precos_diesel_e_gasolina_base.csv'
    path_file_base = 'bases/'+name_file_base
    ultima_data_base = get_ultima_data_disponivel_base(path_file_base)
    print('Última data base disponível:', ultima_data_base)

    # faz o download do PDF do site da petrobrás
    url = 'http://www.petrobras.com.br/lumis/api/rest/pricegraph/report'
    name_file = 'ajustes_precos_diesel_e_gasolina_'+time.strftime("%d.%m.%Y")+'.pdf'
    path_file = 'downloads/'+name_file
    
    if not os.path.exists(path_file):
        download_file(url, path_file)    

    # convert PDF into CSV
    path_file_csv = path_file+'.csv'
    tabula.convert_into(path_file, path_file_csv, output_format="csv")

    print("Arquivo baixado com sucesso e está disponível na pasta downloads:", name_file)

    with open(path_file_csv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reversed(list(reader)):
            data = row['Últimos ajustes (%)']
            diesel = row['Diesel']
            gasolina = row['Gasolina']

            if (datetime.datetime.strptime(data, '%d/%m/%Y').date() <= ultima_data_base):
                continue

            # faz o append no csv
            with open(path_file_base, 'a', newline='') as baseFile:
                fieldnames = ['Data', 'Gasolina', 'Diesel']
                writer = csv.DictWriter(baseFile, fieldnames=fieldnames, delimiter=';')
                row_inserted = {'Data': data, 'Gasolina': gasolina, 'Diesel': diesel}
                writer.writerow(row_inserted)
                print('Dado inserido no arquivo base:', path_file_base, row_inserted)
        print("Base de dados atualizada com sucesso:", path_file_base)
