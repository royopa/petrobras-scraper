# -*- coding: utf-8 -*-
import csv
import json
from io import StringIO
from flask import Flask, render_template, request, make_response, jsonify
import os
import pandas as pd


app = Flask(__name__)
app.debug = True


def csv2json(data):
	reader = csv.DictReader
	reader = csv.DictReader(data)
	out = json.dumps([ row for row in reader ])
	print("JSON parsed!")
	return out


@app.route('/')
def precos():
    name_file_base = 'precos_medios_diesel_e_gasolina_base.csv'
    path_file_base = os.path.join('bases', name_file_base)
    df = pd.read_csv(path_file_base, sep=';')
    df['Diesel'] = df.Diesel.str.replace(',', '.').astype(float)
    df['Gasolina'] = df.Gasolina.str.replace(',', '.').astype(float)
    return jsonify(df.to_json())


@app.route('/indices')
def indices():
    name_file_base = 'saida_indices_diesel_e_gasolina_base.csv'
    path_file_base = os.path.join('bases', name_file_base)
    df = pd.read_csv(path_file_base, sep=';')
    return jsonify(df.to_json())


if __name__ == "__main__":
    app.run()