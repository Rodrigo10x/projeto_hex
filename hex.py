import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pyngrok import ngrok
import os

# Crie um túnel para a porta padrão do Streamlit
public_url = ngrok.connect(8501)
print(f" * Streamlit app is live at: {public_url}")

# Supondo que 'df' seja o DataFrame com os dados de vendas
df = pd.DataFrame({
    'DATA': ['2023-01-15', '2023-02-20', '2023-03-10', '2023-04-25', '2023-05-05'],
    'PRODUTO': ['Produto A', 'Produto B', 'Produto A', 'Produto C', 'Produto B'],
    'TOTAL_DEVIDO': ['R$1.000,00', 'R$2.500,00', 'R$1.200,00', 'R$3.300,00', 'R$2.000,00'],
    'ESTADO': ['SP', 'SP', 'RJ', 'RJ', 'SP']
})

# Conversão da coluna de data e valor
df['DATA'] = pd.to_datetime(df['DATA'])
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

# Visualização 1: Gráfico de Barras - Vendas por Produto (Top 10)
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
df_filtrado['ANO_TRIMESTRE'] = df_filtrado['DATA'].dt.to_period('Q')
vendas_por_trimestre = df_filtrado.groupby('ANO_TRIMESTRE')['TOTAL_DEVIDO'].sum().reset_index()

# Limitar para os últimos 8 trimestres
vendas_por_trimestre = vendas_por_trimestre.sort_values(by='ANO_TRIMESTRE', ascending=False).head(8).sort_values(by='ANO_TRIMESTRE')

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(vendas_por_trimestre['ANO_TRIMESTRE'].astype(str), vendas_por_trimestre['TOTAL_DEVIDO'], 
        marker='o', color='orange', linestyle='-', linewidth=2)
ax.set_xlabel('Ano-Trimestre')
ax.set_ylabel('Vendas em R$')
ax.set_title('Vendas ao Longo do Tempo (Últimos 8 Trimestres)')
ax.grid(True)
plt.xticks(rotation=45)
ax.set_ylim(0, vendas_por_trimestre['TOTAL_DEVIDO'].max() * 1.1)  # Limitar o eixo y com um buffer
st.pyplot(fig)

# Execute o comando do Streamlit
os.system('streamlit run app.py')
