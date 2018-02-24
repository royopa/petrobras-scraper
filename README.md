Petrobras scraper
-----------------

O Petrobras scraper é um projeto para captura de dados do site da Petrobras com indicadores de preços médios da Gasolina e Diesel.

## Informações contidas nos Relatórios

### Relatório com variação de preços

A Petrobras apresentava o ajuste de preços com a variação em percentual em relação a data divulgada anteriormente, através [deste relatório PDF](http://www.petrobras.com.br/lumis/api/rest/pricegraph/report). Este relatório não é mais atualizado, sendo o dia 17/02/2018 a última data disponível.

Um trecho [relatório com as variações de preço](http://www.petrobras.com.br/lumis/api/rest/pricegraph/report) pode ser visto abaixo:

![relatorio_ajuste_precos_example.png](https://raw.githubusercontent.com/royopa/petrobras-scraper/master/images/relatorio_ajuste_precos_example.png)

O programa que faz o download e converte os dados baixados para CSV é o [download_ajustes_precos_diesel_e_gasolina.py](https://github.com/royopa/petrobras-scraper/blob/master/download_ajustes_precos_diesel_e_gasolina.py).

### Relatório com preços médios

A partir de 08/02/2018 a Petrobras passou a disponibilizar a informação de preços médios em reais por litro, através [deste relatório PDF](http://www.petrobras.com.br/lumis/api/rest/pricegraphnovo/report?n=4)

Um trecho do [relatório dos preços médios de diesel e gasolina](http://www.petrobras.com.br/lumis/api/rest/pricegraph/report) pode ser visto abaixo:

![relatorio_preco_medio_example.png](https://raw.githubusercontent.com/royopa/petrobras-scraper/master/images/relatorio_preco_medio_example.png)

O programa que faz o download e converte os dados baixados para CSV é o [download_precos_medios_diesel_e_gasolina.py](https://github.com/royopa/petrobras-scraper/blob/master/download_precos_medios_diesel_e_gasolina.py).

## Relatórios apenas no formato PDF

As informações disponibilizadas estão apenas no formato PDF. Entrei em contato com a Petrobras solicitando que o relatório fosse disponibilizado em outro formato (como json, xml ou txt), mas eles responderam (Protocolo Ouvidoria Geral Nº 00914/2018
) que existia apenas o formato PDF disponível e não me deram nenhum indicativo sobre a possibilidade de disponibilização da informação em outros formatos no futuro.

Diante disso, após o download do PDF foi necessário a criação de um passo para extrair os dados da tabela em PDF, tarefa que foi realizada pela biblioteca [tabula-py](https://github.com/chezou/tabula-py). O [tabula-py]((https://github.com/chezou/tabula-py)) é um wrapper do [tabula-java](https://github.com/tabulapdf/tabula-java), que extrai uma tabela de um pdf para um [DataFrame pandas](https://www.datacamp.com/community/tutorials/pandas-tutorial-dataframe-python).

## Instalar dependências do projeto

```sh
> pip install -r requirements.txt
```

## Utilizando os programas

#### 1º passo - Fazer o download e atualizar a base de dados de preços

Para fazer o download dos preços e atualizar a [base de dados de preços](https://github.com/royopa/petrobras-scraper/blob/master/bases/precos_medios_diesel_e_gasolina_base.csv) basta executar o programa [download_precos_medios_diesel_e_gasolina.py](https://github.com/royopa/petrobras-scraper/blob/master/download_precos_medios_diesel_e_gasolina.py) com o comando abaixo:

```sh
> python download_precos_medios_diesel_e_gasolina.py
```

#### 2º passo - Calcular valores e atualizar a base de indicadores

A partir da base de preços médios diários atualizada no passo anterior, foi criado uma outra base com a variação de preços em percentual. Para executar esse processo e atualizar a [base de ajuste de preços](https://github.com/royopa/petrobras-scraper/blob/master/bases/indices_diesel_e_gasolina_base.csv) basta executar o programa [atualiza_base_ajuste_precos_diesel_gasolina.py](https://github.com/royopa/petrobras-scraper/blob/master/atualiza_base_ajuste_precos_diesel_gasolina.py) com o comando abaixo:

```sh
> python atualiza_base_ajuste_precos_diesel_gasolina.py
```

#### 3º passo - Calcular o preço na base 100 com dados a partir de 2017

Visto que os dados de preços da Petrobras foram disponibilizados apenas a partir de fevereiro/2018 e anteriormente já existia na base de dados preços utilizando base 100 tendo como início 01/01/2017, foi criado o programa [calcula_preco_base_100.py](https://github.com/royopa/petrobras-scraper/blob/master/calcula_preco_base_100.py) para fazer esse cálculo e gerar os arquivos com a base final, contendo a variação diária e os preços usando base 100 a partir de 01/01/2017. A execução desse programa gera dois arquivos de saída com o mesmo conteúdo: [um em csv](https://github.com/royopa/petrobras-scraper/blob/master/bases/saida_indices_diesel_e_gasolina_base.csv) e [outro no formato excel xlsx](https://github.com/royopa/petrobras-scraper/blob/master/bases/saida_xlsx_indices_diesel_e_gasolina_base.csv.xlsx)

Os arquivo de base terão o seguinte formato e poderão ser usados para análise:

![base_final.png](https://raw.githubusercontent.com/royopa/petrobras-scraper/master/images/base_final.png)


#### Atalho para executar os passos de uma única vez

Para executar a atualização das bases de dados de uma única vez, basta executar os 3 passos seguidos. Para facilitar esse processo, apenas execute o script start.bat/start.sh, de acordo com o seu sistema operacional:

##### No Linux
```sh
> ./start.sh
```

##### No Windows
```sh
> ./start.bat
```

## Análise dos dados

Caso você deseja abrir as bases de dados como um dataframe [pandas](https://pandas.pydata.org/) utilize a [função read_csv()](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html), conforme exemplo abaixo:

```python
import pandas as pd

path_file_base = 'bases/saida_indices_diesel_e_gasolina_base.csv'
df = pd.read_csv(path_file_base, sep=';')

print(df.tail())

```

A partir do dataframe carregado você já pode executar todas as ações para análise.