Petrobras scraper
-----------------

O Petrobras scraper são programas em Python 3 para baixar arquivos do site da Petrobrás com os indicadores de preços médios da Gasolina e Diesel para análise.


## Informações contidas nos Relatórios

### Relatório com variação de preços

Até 17/02/2018 a Petrobras apresentava o ajuste de preços com a variação em percentual em relação a data divulgada anteriormente, através do PDF 
[deste relatório PDF](http://www.petrobras.com.br/lumis/api/rest/pricegraph/report). Este relatório não é mais atualizado no site da Petrobrás, sendo o dia 17/02/2018 a última data disponível.

Um trecho [relatório com as variações de preço](http://www.petrobras.com.br/lumis/api/rest/pricegraph/report) pode ser visto abaixo:

![relatorio_ajuste_precos_example.png](https://raw.githubusercontent.com/royopa/petrobras-scraper/master/images/relatorio_ajuste_precos_example.png)

O programa que faz o download e converte os dados baixados para CSV é o [download_ajustes_precos_diesel_e_gasolina.py](download_ajustes_precos_diesel_e_gasolina.py).

### Relatório com preços médios

A partir de 08/02/2018 a Petrobras passou a disponibilizar a informação de preços médios em reais por litro, através [deste relatório PDF](http://www.petrobras.com.br/lumis/api/rest/pricegraphnovo/report?n=4)

Um trecho do [relatório dos preços médios de diesel e gasolina](http://www.petrobras.com.br/lumis/api/rest/pricegraph/report) pode ser visto abaixo:

![relatorio_preco_medio_example.png](https://raw.githubusercontent.com/royopa/petrobras-scraper/master/images/relatorio_preco_medio_example.png)

O programa que faz o download e converte os dados baixados para CSV é o [download_precos_medios_diesel_e_gasolina.py](download_precos_medios_diesel_e_gasolina.py).

## Relatórios apenas no formato PDF

As informações disponibilizadas estão apenas no formato PDF. Entrei em contato com a Petrobras solicitando que o relatório fosse disponibilizado em outro formato (como json, xml ou txt), mas eles responderam (Protocolo Ouvidoria Geral Nº 00914/2018
) que existia apenas o formato PDF disponível e não me deram nenhum indicativo sobre a possibilidade de disponibilização da informação em outros formatos no futuro.

Diante disso, após o download do PDF foi necessário a criação de um passo para extrair os dados da tabela em PDF, tarefa que foi realizada pela biblioteca [tabula-py](https://github.com/chezou/tabula-py). O [tabula-py]((https://github.com/chezou/tabula-py)) é um wrapper do [tabula-java](https://github.com/tabulapdf/tabula-java), que extrai uma tabela de um pdf para um [DataFrame pandas](https://www.datacamp.com/community/tutorials/pandas-tutorial-dataframe-python).

## Instalar dependências do projeto

```sh
> pip install -r requirements.txt
```

Os arquivos PDF baixados e convertidos em csv estarão disponíveis na pasta [./downloads]() do projeto.

As bases atualizadas estarão disponíveis na basta ./bases do projeto.

python download_precos_medios_diesel_e_gasolina.py %*


python atualiza_base_ajuste_precos_diesel_gasolina.py %*
python calcula_preco_base_100.py %*