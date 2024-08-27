import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

current_working_directory = os.getcwd()

serie_gini_excel = os.path.join(current_working_directory, "serie_gini.xlsx")

# Configurar a página para usar a largura total
st.set_page_config(layout="wide")

st.title('R.I.D.B - Relatório interativo da desigualdade brasileira')
st.write('O Índice de Gini é uma medida de desigualdade de renda ou riqueza em uma população. Foi desenvolvido pelo estatístico italiano Corrado Gini e é amplamente utilizado para quantificar a disparidade econômica dentro de um país ou região.')

# Carrega o DataFrame a partir de um arquivo Excel
serie_gini = pd.read_excel(serie_gini_excel, sheet_name='serie_historica')

gini23 = pd.read_excel(serie_gini_excel, sheet_name='2023_gini')

gini23 = gini23.sort_values(by='GINI')

indice_max = gini23['GINI'].idxmax()
print(gini23['UF'][indice_max])

indice_min = gini23['GINI'].idxmin()
print(gini23['UF'][indice_min])

indice_mediano = (gini23['GINI'] - gini23['GINI'].median()).abs().idxmin()
print(gini23['UF'][indice_mediano])

def makeChart(values):

    fig = go.Figure()

    periodo = serie_gini['Ano'].tolist()

    for a in values:

        yvalues = serie_gini[a].tolist()

        fig.add_trace(go.Scatter(x=periodo, y=yvalues, mode='lines', name=a))

    fig.update_layout(
        title = 'Evolução do índice de gini (2015-2023)',
        xaxis_title = 'Anos',
        yaxis_title = 'GINI'
    )

    return fig

options = serie_gini.columns.tolist()

options.remove('Ano')

option = st.sidebar.multiselect('Selecione a opção:', options, default=['Brasil', 'Região Centro-oeste', 'Região Norte', 'Região Nordeste', 'Região Sul', 'Região Sudeste'])
print(option)

a1, a2, a3, a4 = st.columns(4)
a1.metric("GINI do Brasil (2023)", "BR - 0.518")
a2.metric("Estado com maior GINI (2023)",f"{gini23['UF'][indice_max]} - {gini23['GINI'][indice_max]}")
a3.metric("Estado com menor GINI (2023)",f"{gini23['UF'][indice_min]} - {gini23['GINI'][indice_min]}")
a4.metric("Estado com GINI mediano (2023)",f"{gini23['UF'][indice_mediano]} - {gini23['GINI'][indice_mediano]}")

col1, col2 = st.columns([3, 1])

with col1:
    st.plotly_chart(makeChart(option))
with col2:
    st.markdown('**Índice de GINI por UF em ordem crescente (2023)**')
    st.dataframe(gini23.reset_index(drop=True))