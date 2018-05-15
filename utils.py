#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import csv
import datetime
import os
import pandas as pd
from datetime import timedelta
import bizdays
from tqdm import tqdm


def check_download(dt_referencia, file_name):
    if not isbizday(dt_referencia):
        print(dt_referencia, 'não é dia útil')
        return False
    if os.path.exists(file_name):
        print(file_name, 'arquivo já baixado')
        return False
    return True


def download_file(url, file_name):
    response = requests.get(url, stream=True)
    with open(file_name, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)
    handle.close()


def get_ultima_data_disponivel_base(path_file_base):
    # verifica a última data disponívl na base
    with open(path_file_base, 'r') as f:
        for row in reversed(list(csv.reader(f))):
            data = row[0].split(';')[0]
            if data == 'Data':
                return None
            data = row[0].split(';')[0]
            return datetime.datetime.strptime(data, '%d/%m/%Y').date()


def remove_old_files(start_name):
    file_list = os.listdir(r"downloads")
    for file_name in file_list:
        if not file_name.startswith(start_name):
            continue
        today = datetime.datetime.now().strftime('%d.%m.%Y')
        data_arquivo = file_name.split(start_name)[-1][-20:][0:10]
        if today != data_arquivo:
            os.remove(os.path.join('downloads', file_name))


def get_calendar():
    holidays = bizdays.load_holidays('ANBIMA.txt')
    return bizdays.Calendar(holidays, ['Sunday', 'Saturday'])


def isbizday(dt_referencia):
    cal = get_calendar()
    return cal.isbizday(dt_referencia)
