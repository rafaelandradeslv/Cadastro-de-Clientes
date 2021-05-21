from flask import Blueprint, render_template, request, flash, redirect, url_for
import json
import requests
import pandas as pd
import numpy as np

views = Blueprint('views', __name__)

## -- PÁGINA INICIAL --
@views.route('/')
def home():
    """
    Rota inicial.
    Não é necessário modificar nada nessa função
    """
    return render_template('home.html')


@views.route('/clientes')
def clientes():
    """
    Rota para aba de clientes. Mostra na tela uma representação do csv de clientes
    Não é necessário modificar nada nessa função
    """
    df = pd.read_csv('data/clientes.csv', dtype=object, sep=';')
    df = df.replace(np.nan, '', regex=True)
    return render_template('clientes.html', df=df, titles=df.columns.values)


## -- CADASTRO --
@views.route('/cadastro')
def cadastro():
    """
    Função para cadastro de novos clientes. Deverá pegar as informações do forms e salvar numa nova linha no csv.
    Necessário também salvar as informações de endereço provindas da API de CEP
    """
    ## TODO pegar informações do forms


    ## TODO buscar informações de endereço da API do ViaCEP (https://viacep.com.br/)


    ## TODO criar nova linha no arquivo csv


    return render_template('cadastro.html')


## -- CONSULTA CEP --
@views.route('/consulta-cep')
def consulta_cep():
    ## TODO pegar CEP do forms


    ## TODO buscar informações de endereço da API do ViaCEP (https://viacep.com.br/)


    ## TODO mostrar no html as informações obtidas


    return render_template('consulta_cep.html')