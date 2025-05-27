import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time


@st.cache_data
def converte_csv(df: pd.DataFrame):
    return df.to_csv(index=False, encoding='utf-8')


def mensagem_sucesso():
    sucesso = st.success('Download concluído', icon="✅")
    time.sleep(5)
    sucesso.empty()


st.set_page_config(layout='wide')

st.title("DADOS BRUTOS")


url = 'https://labdados.com/produtos'
response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())

# dados = pd.read_json('produtos.json')

dados['Data da Compra'] = pd.to_datetime(
    dados['Data da Compra'], format='%d/%m/%Y')

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas',
                             dados.columns.to_list(), dados.columns.to_list())
st.sidebar.title('Filtros')

with st.sidebar.expander('Nome do Produto'):
    produtos = st.multiselect(
        'Selecione os produtos', dados['Produto'].unique(), dados['Produto'].unique())
with st.sidebar.expander('Categoria'):
    categoria = st.multiselect(
        'Selecione a categoria', dados['Categoria do Produto'].unique(), dados['Categoria do Produto'].unique())
with st.sidebar.expander('Preço do Produto'):
    preco = st.slider('Selecione o preço', dados['Preço'].min(
    ), dados['Preço'].max(), (dados['Preço'].min(), dados['Preço'].max()))
with st.sidebar.expander('Frete de Vendas'):
    frete = st.slider('Frete', dados['Frete'].min(), dados['Frete'].max(
    ), (dados['Frete'].min(), dados['Frete'].max()))
with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input(
        'Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))
with st.sidebar.expander('Vendedor'):
    vendedor = st.multiselect(
        'Selecione os vendedores', dados['Vendedor'].unique(), dados['Vendedor'].unique())
with st.sidebar.expander('Local da Compra'):
    local_compra = st.multiselect('Local da compra', dados['Local da compra'].unique(
    ), dados['Local da compra'].unique())
with st.sidebar.expander('Avaliação da Compra'):
    avaliacao = st.slider('Selecione a avaliação da compra', 1, 5, (1, 5))
with st.sidebar.expander('Tipo de Pagamento'):
    tipo_pagamento = st.multiselect(
        'Selecione o tipo de pagamento', dados['Tipo de pagamento'].unique(), dados['Tipo de pagamento'].unique())
with st.sidebar.expander('Quantidade de Parcelas'):
    qtde_parcelas = st.slider(
        'Selecione a quantidade de parcelas', 1, 24, (1, 24))


query = '''
Produto in @produtos and \
`Categoria do Produto` in @categoria and \
@preco[0] <= Preço <= @preco[1] and \
@frete[0] <= Frete <= @frete[1] and \
@data_compra[0] <= `Data da Compra` <= @data_compra[1] and \
Vendedor in @vendedor and \
`Local da compra` in @local_compra and \
@avaliacao[0] <= `Avaliação da compra` <= @avaliacao[1] and \
`Tipo de pagamento` in @tipo_pagamento and \
@qtde_parcelas[0] <= `Quantidade de parcelas` <= @qtde_parcelas[1]
'''

dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)
st.markdown(
    f'A tabela possui :blue[{dados_filtrados.shape[0]:}] linhas e  :blue[{dados_filtrados.shape[1]}] colunas')

st.markdown('Nome do arquivo')
coluna1, coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = st.text_input(
        '', label_visibility='collapsed', value='dados')
    nome_arquivo += '.csv'
with coluna2:
    st.download_button('Download CSV', data=converte_csv(
        dados_filtrados), file_name=nome_arquivo, mime='txt/csv', on_click=mensagem_sucesso)
