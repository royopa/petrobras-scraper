#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import time
import tabula
import csv
import datetime
from tqdm import tqdm
import os
import wget


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


def download_file(url, file_name):
    response = requests.get(url, stream=True)
    with open(file_name, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)
    handle.close()


if __name__ == '__main__':
    # verifica a última data disponível na base 
    name_file_base = 'precos_medios_diesel_e_gasolina_base.csv'
    path_file_base = 'bases/'+name_file_base
    ultima_data_base = get_ultima_data_disponivel_base(path_file_base)
    print('Última data base disponível:', ultima_data_base)
    if (ultima_data_base is None):
        ultima_data_base = datetime.date(1900, 1, 1)

    # faz o download do PDF do site da petrobrás
    url = 'http://www.petrobras.com.br/lumis/api/rest/pricegraphnovo/report?n=4'
    name_file = 'precos_medios_diesel_e_gasolina_'+time.strftime("%d.%m.%Y")+'.pdf'
    path_file = 'downloads/'+name_file

    if not os.path.exists(path_file):
        wget.download(url, path_file)

    # convert PDF into CSV
    path_file_csv = path_file+'.csv'
    tabula.convert_into(path_file, path_file_csv, output_format="csv")
    
    print("Arquivo baixado com sucesso e está disponível na pasta downloads:", name_file)

    with open(path_file_csv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reversed(list(reader)):
            data = row['Últimos Ajustes']
            diesel = row['Diesel A (R$/litro)']
            gasolina = row['Gasolina A (R$/litro)']

            print(data, diesel, gasolina)

            if (datetime.datetime.strptime(data, '%d/%m/%Y').date() <= ultima_data_base):
                continue

            # faz o append no csv
            with open(path_file_base, 'a', newline='') as baseFile:
                fieldnames = ['Data', 'Diesel', 'Gasolina']
                writer = csv.DictWriter(baseFile, fieldnames=fieldnames, delimiter=';')
                row_inserted = {'Data': data, 'Gasolina': gasolina, 'Diesel': diesel}
                writer.writerow(row_inserted)
                print('Dado inserido no arquivo base:', row_inserted)
        print("Base de dados atualizada com sucesso:", path_file_base)
