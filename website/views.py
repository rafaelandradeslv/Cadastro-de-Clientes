from flask import Blueprint, render_template, request, flash, redirect, url_for
import pandas as pd

# -- MODELOS --
from models.models import Pessoa, Busca

# -- INÍCIO DO APP --
views = Blueprint('views', __name__)


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
    
    info_nome = request.form['nome']
    info_sobrenome = request.form['sobrenome']
    info_email = request.form['email']
    info_cep = request.form['cep']

    pessoa1 = Pessoa(info_nome, info_sobrenome, info_email, info_cep)

    pessoa = {
        'nome': pessoa1.nome,
        'sobrenome': pessoa1.sobrenome,
        'email': pessoa1.email,
    }
    # coleta as informações cadastradas
    df1 = pd.DataFrame(data=pessoa, index=[0])

    
    print('cheguei na api')
    df2 = pessoa1.api()
    print('passei da api')
    try:
        # coleta informações da API
        # une as informações
        result = pd.concat([df1, df2], axis=1, ignore_index=True)
        result.columns = Pessoa.columns_name  # renomeia as informações

        df_final = pd.concat([Pessoa.df_principal, result]
                             )  # constrói o dataset final

        Pessoa.df_principal = df_final

        flash('Cliente cadastrado com sucesso')
        print('deu certo em views')
        return redirect(url_for('views.clientes'))

    except:
        print('deu errado em views')
        flash('Cep Não Encontrado ou Inválido')
        return redirect(url_for('views.cadastro'))


# -- CONSULTA CEP --
@views.route('/consulta-cep')
def consulta_cep():
    return render_template('consulta_cep.html', dic=Busca.dicionario)


@views.route('/validando_busca', methods=['POST', ])
def consulta():
    busca_cep = request.form['cep_busca']
    result = Busca(busca_cep)
    busca_final = Busca.pesquisa(result)
    Busca.dicionario = busca_final
    return redirect(url_for('views.consulta_cep'))


# -- CLIENTES CADASTRADOS --
@views.route('/clientes')
def clientes():
    """
    Rota para aba de clientes. Mostra na tela uma representação do csv de clientes
    Não é necessário modificar nada nessa função
    """
    Pessoa.df_principal.to_csv('data/clientes.csv', index=False,
                               sep=';')  # executa a função e salva os dados no csv
    return render_template('/clientes.html',
                           df=Pessoa.df_principal,
                           titles=Pessoa.df_principal.columns.values)
