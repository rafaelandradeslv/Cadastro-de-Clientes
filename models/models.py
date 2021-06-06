import requests
import pandas as pd
import json
from flask import redirect, url_for, flash, render_template


# -- OBJETO CLIENTE --

class Pessoa:

    # -- Variáveis Acessíveis --
    df_principal = pd.read_csv('data/clientes.csv', sep=';')
    columns_name = []
    for i in df_principal:
        columns_name.append(i)

    # -- FUNÇÕES --
    def __init__(self, nome, sobrenome, email, cep):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.cep = cep

    def api(self): 
        # Busca informação de endereço da API do ViaCEP (https://viacep.com.br/)
        print('cheguei em models')
        response = requests.get(f'http://www.viacep.com.br/ws/{self.cep}/json/') 
        print(f'este e o valor de {response}')
        # validando cep
        if response.status_code == requests.codes.ok:
            dados_json = json.loads(response.text)
            df = pd.DataFrame(data=dados_json, index=[0])
            print('deu certo')
            return df
        else:
            print('deu errado')
            return response

class Busca:
    dicionario = ''

    def __init__(self, cep):
        self.cep = cep

    def pesquisa(self):
        response = requests.get(
            f'http://www.viacep.com.br/ws/{self.cep}/json/')
        if response.status_code == requests.codes.ok:
            print(response.status_code)
            busca = json.loads(response.text)
            return busca
        else:
            flash('cep não encontrado')
            print(response.status_code)
            return redirect(url_for('views.consulta_cep'))
