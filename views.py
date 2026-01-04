from main import app
from flask import render_template
import pandas as pd
import plotly.express as px
import os

#rotas
@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/linha-do-tempo")
def linha_tempo():
    #lendo um arquivo excel e salvando na variavel dataframe
    df = pd.read_excel("dadosmortesporano.xlsx")

    #tem que deixar ano em string para nao virar 1347,5
    df['ano'] = df['ano'].astype(str)

    # criar grafico interativo de linhas  e usa os dados do DataFrame para criar grafico com x e y
    fig = px.line(
        df,
        x="ano",
        y="mortes",
        title="Linha do Tempo da Mortalidade",
        template="plotly_dark" #deixar escuro bang
    )

    #vou mudar a cor da linha do grafico
    fig.update_traces(line_color='#FF0000')

    fig.update_layout(
        separators=",."
    )

    #fazer separador de milhar, aparecer 15.000.000 (eixo y)
    fig.update_yaxes(
        tickformat=",.0f",
    )

    #convertendo grafico (objeto python) para html
    grafico = fig.to_html(
        full_html=False,
        include_plotlyjs="cdn" # ia disse que 'include_plotlyjs="cdn"' faz o gráfico carregar a biblioteca visual via internet (mais leve)
        )
    

    # renderizar o template pasando grafico
    return render_template("line.html", grafico=grafico)

@app.route("/comparacao-paises")
def comparison_country():
    # --- 1. SEGURANÇA DE ARQUIVO ---
    # Garante que ele ache o Excel na mesma pasta do script
    base_path = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(base_path, "paisesmortalidade.xlsx")

    df = pd.read_excel(caminho_arquivo, engine='openpyxl')

    #tem que multiplicar por 100 para nao ficar 0.65 e sim 65%
    coluna_mortalidade = "Estimativas de Mortalidade (aproximada)"
    df[coluna_mortalidade] = df[coluna_mortalidade] * 100

    #grafico de coluna para gerar é px.bar
    fig = px.bar(
        df,
        x="Países",
        y="Estimativas de Mortalidade (aproximada)",
        title="Comparação da Mortalidade por Países da Europa",
        template="plotly_dark",
        text="Estimativas de Mortalidade (aproximada)"
    )

    fig.update_traces(
        marker_color='#002aff',
        textposition='outside',
        texttemplate='%{text:.1f}%'
    )

    fig.update_layout(
        yaxis_range=[0,100]
    )

    grafico = fig.to_html(
        full_html=False,
        include_plotlyjs="cdn"
    )

    return render_template("comparison.html",grafico=grafico)


