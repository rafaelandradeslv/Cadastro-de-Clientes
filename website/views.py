from os import sep
from flask import Blueprint, render_template, request, flash, redirect, url_for
import json
import requests
import pandas as pd
import numpy as np

views = Blueprint('views', __name__)

# -- OBJETO CLIENTE --


class Pessoa:
    df_principal = pd.read_csv('data/clientes.csv', sep=';')
    columns_name = []
    for i in df_principal:
        columns_name.append(i)

    def __init__(self, nome, sobrenome, email, cep):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.cep = cep

    # TODO buscar informações de endereço da API do ViaCEP (https://viacep.com.br/)

    def busca(self):
        response = requests.get(
            f'http://www.viacep.com.br/ws/{self.cep}/json/')
        # validando cep
        if response.status_code == 200:
            dados_json = json.loads(response.text)
            df = pd.DataFrame(data=dados_json, index=[0])
        else:
            print('Cep inválido !')
        return df

# -- PÁGINA INICIAL --


@views.route('/')
def home():
    """
    Rota inicial.
    Não é necessário modificar nada nessa função
    """
    return render_template('home.html')


# -- CADASTRO --

@views.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@views.route('/novo_cliente', methods=['POST', ])
def novo_cliente():
    """
    Função para cadastro de novos clientes. Deverá pegar as informações do forms e salvar numa nova linha no csv.
    Necessário também salvar as informações de endereço provindas da API de CEP
    """
    # TODO pegar informações do forms
    p1 = request.form['nome']
    p2 = request.form['sobrenome']
    p3 = request.form['email']
    p4 = request.form['cep']

    pessoa1 = Pessoa(p1, p2, p3, p4)

    dicio = {
        'nome': pessoa1.nome,
        'sobrenome': pessoa1.sobrenome,
        'email': pessoa1.email,
    }
    df1 = pd.DataFrame(data=dicio, index=[0])

    # TODO criar nova linha no arquivo csv

    df2 = pessoa1.busca()
    result = pd.concat([df1, df2], axis=1, ignore_index=True)
    result.columns = Pessoa.columns_name

    df_final = pd.concat([Pessoa.df_principal, result])

    Pessoa.df_principal = df_final

    return redirect(url_for('views.clientes'))

# -- CONSULTA CEP --


@views.route('/consulta-cep')
def consulta_cep():
    # TODO pegar CEP do forms

    # TODO buscar informações de endereço da API do ViaCEP (https://viacep.com.br/)

    # TODO mostrar no html as informações obtidas

    return render_template('consulta_cep.html')


@views.route('/clientes')
def clientes():
    """
    Rota para aba de clientes. Mostra na tela uma representação do csv de clientes
    Não é necessário modificar nada nessa função
    """
    Pessoa.df_principal.to_csv('clientes.csv', index=False, sep=';')
    
    return render_template('clientes.html', 
                            df=Pessoa.df_principal, 
                            titles=Pessoa.df_principal.columns.values)