#Importação das bibliotecas.
import streamlit as st
import pandas as pd
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

df_data = pd.read_csv(r"C:\Users\xrodr\OneDrive\Área de Trabalho\Projeto_hex\hex.csv")

st.title("Dashboard Hexagon")



import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import streamlit as st

# Carregar o DataFrame formatado
df = pd.read_csv(r'C:\Users\xrodr\OneDrive\Área de Trabalho\Projeto_hex\hex.csv', delimiter=';')
df['PRODUTO'] = df['PRODUTO'].str.split(',').str[0].str.strip()
df['DATA'] = pd.to_datetime(df['DATA'], errors='coerce')
df['TOTAL_DEVIDO'] = df['TOTAL_DEVIDO'].replace({'R\$': '', ',': ''}, regex=True).astype(float)

# Sidebar com os filtros de período, produto e região
st.sidebar.header("Filtros")

# Filtro de data
data_inicial = st.sidebar.date_input("Data Inicial", df['DATA'].min().date())
data_final = st.sidebar.date_input("Data Final", df['DATA'].max().date())

# Filtro de produto
produtos = df['PRODUTO'].unique()
produtos_selecionados = st.sidebar.multiselect("Selecionar Produto(s)", produtos, default=produtos)

# Filtro de região
regioes = df['ESTADO'].unique()
regioes_selecionadas = st.sidebar.multiselect("Selecionar Região(ões)", regioes, default=regioes)

# Filtrar o DataFrame baseado nos filtros selecionados
df_filtrado = df[(df['DATA'].dt.date >= data_inicial) & (df['DATA'].dt.date <= data_final)]
df_filtrado = df_filtrado[df_filtrado['PRODUTO'].isin(produtos_selecionados)]
df_filtrado = df_filtrado[df_filtrado['ESTADO'].isin(regioes_selecionadas)]

# KPI: Vendas Totais no Período Filtrado
vendas_totais = df_filtrado['TOTAL_DEVIDO'].sum()
st.metric("Vendas Totais no Período", f"R${vendas_totais:,.2f}")

# Visualização 1: Gráfico de Barras - Vendas por Produto
st.subheader("Vendas Totais por Produto (Top 10)")
vendas_por_produto = df_filtrado.groupby('PRODUTO')['TOTAL_DEVIDO'].sum().reset_index()
vendas_por_produto = vendas_por_produto.sort_values(by='TOTAL_DEVIDO', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(12, 6))
ax.barh(vendas_por_produto['PRODUTO'], vendas_por_produto['TOTAL_DEVIDO'], color='skyblue')
ax.set_xlabel('Vendas em R$')
ax.set_ylabel('Produto')
ax.set_title('Vendas Totais por Produto (Top 10)')
ax.xaxis.set_major_formatter(mtick.StrMethodFormatter('R${x:,.2f}'))
ax.set_xlim(0, vendas_por_produto['TOTAL_DEVIDO'].max() * 1.1)  # Limitar o eixo x com um buffer
st.pyplot(fig)

# Visualização 2: Gráfico de Linhas - Vendas ao Longo do Tempo (Trimestral)
st.subheader("Vendas ao Longo do Tempo (Trimestral)")
df_filtrado['ANO_TRIMESTRE'] = df_filtrado['DATA'].dt.to_period('Q').astype(str)
vendas_por_trimestre = df_filtrado.groupby('ANO_TRIMESTRE')['TOTAL_DEVIDO'].sum().reset_index()

# Limitar para os últimos 8 trimestres
vendas_por_trimestre = vendas_por_trimestre.sort_values(by='ANO_TRIMESTRE', ascending=False).head(8).sort_values(by='ANO_TRIMESTRE')

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(vendas_por_trimestre['ANO_TRIMESTRE'], vendas_por_trimestre['TOTAL_DEVIDO'], 
        marker='o', color='orange', linestyle='-', linewidth=2)
ax.set_xlabel('Ano-Trimestre')
ax.set_ylabel('Vendas em R$')
ax.set_title('Vendas ao Longo do Tempo (Últimos 8 Trimestres)')
ax.grid(True)
plt.xticks(rotation=45)
ax.set_ylim(0, vendas_por_trimestre['TOTAL_DEVIDO'].max() * 1.1)  # Limitar o eixo y com um buffer
st.pyplot(fig)

