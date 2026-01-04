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

    # criar grafico interativo e usa os dados do DataFrame para criar grafico com x e y
    fig = px.line(
        df,
        x="ano",
        y="mortes",
        title="Linha do Tempo da Mortalidade",
        template="plotly_dark" #deixar escuro bang
    )

    #vou mudar a cor da linha do grafico
    fig.update_traces(line_color='rgb(228, 8, 129)')

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