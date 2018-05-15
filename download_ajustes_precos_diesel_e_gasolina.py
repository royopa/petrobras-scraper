#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import tabula
import csv
import datetime
import os
import utils


if __name__ == '__main__':
    utils.remove_old_files('ajustes_precos_diesel_e_gasolina_')
    dt_referencia = datetime.datetime.now().date()
    # verifica a última data disponível na base 
    name_file_base = 'ajustes_precos_diesel_e_gasolina_base.csv'
    path_file_base = 'bases/'+name_file_base
    ultima_data_base = utils.get_ultima_data_disponivel_base(path_file_base)
    print('Última data base disponível:', ultima_data_base)

    # faz o download do PDF do site da petrobrás
    url = 'http://www.petrobras.com.br/lumis/api/rest/pricegraph/report'
    name_file = 'ajustes_precos_diesel_e_gasolina_'+dt_referencia.strftime("%d.%m.%Y")+'.pdf'
    path_file = os.path.join('downloads', name_file)
    
    # somente faz o download se for dia útil
    if not utils.check_download(dt_referencia, path_file):
        print('Processo terminado, a data não é dia útil ou o arquivo já foi importado', dt_referencia)
        exit()

    # faz o download
    utils.download_file(url, path_file)

    # convert PDF into CSV
    path_file_csv = path_file+'.csv'
    tabula.convert_into(path_file, path_file_csv, output_format="csv")

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
