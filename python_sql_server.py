#!/usr/bin/env python
# author "Jean Jacques"
# github https://github.com/jjeanjacques10/

import pyodbc 
import pandas as pd
import json

#Acessando o arquivo de configuração
with open('config.json') as config_file:
    data = json.load(config_file)

server = data['Server']
database = data['Database']
query = data['Query']

#Fazendo a conexão com o SQL Server
conn = pyodbc.connect('Driver={SQL Server};'
                      f'Server={server};'
                      f'Database={database};'
                      'Trusted_Connection=yes;')

#Fazeendo o SELECT na tabela selecionada
cursor = conn.cursor()
cursor.execute(query)

#Pegando o nome dos campos
num_fields = len(cursor.description)
field_names = [i[0] for i in cursor.description]

#Adicionando os valores em uma lista
table_rows = []

for row in cursor:
    #Gerando um item para adicionar a lista
    item = []
    for i in range(len(row)):
        item.append(row[i])

    table_rows.append(item)

#Gerando um DataFrame
df = pd.DataFrame(table_rows, columns=field_names)

#Salvando como .CSV
df.to_csv(f'{database}_dataframe.csv', index= False, header=True)