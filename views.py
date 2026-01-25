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

@app.route("/proporcao-sobreviventes")
def sobreviventes():
    #dessa vez sem excel pois numeros são mto variados
    #armazenar tudo numa variavel data e depois jogar no datafrmae
    data = {
            "Status": ["Mortos", "Sobreviventes"],
            "Média (Milhões)": [37.5, 42.5],
            "Margem de Erro": [12.5, 12.5]
    }

    df = pd.DataFrame(data)    

    fig = px.bar(
        df,
        x="Status",
        y="Média (Milhões)",
        error_y="Margem de Erro", #margem de erro no eixo y
        color="Status",
        title="Europa: Mortos vs Sobreviventes (com estimativa de erro)",
        template="plotly_dark",
        text_auto=True,
        color_discrete_map={"Mortos": "#ff5a5f", "Sobreviventes": "#00a699"}
    )

    fig.update_layout(
        showlegend=False,
        yaxis_title="População (Milhões)"
    )

    grafico = fig.to_html(
        full_html=False,
        include_plotlyjs="cdn"
    )

    return render_template("sobreviventes.html",grafico=grafico)

@app.route("/letalidade")
def letalidade():
    return render_template("letalidade.html")

import plotly.express as px
import pandas as pd

@app.route("/mapa")
def mapa():
    # 1. CRIAR OS DADOS (Simulando uma tabela Excel)
    # Usamos os códigos ISO-3 (3 letras) para o Plotly achar os países fácil
    dados_peste = {
        "Pais": ["Itália", "França", "Espanha", "Reino Unido", "Alemanha", "Noruega", "Suécia", "Polônia", "Rússia", "Turquia", "Grécia", "Egito"],
        "Codigo": ["ITA", "FRA", "ESP", "GBR", "DEU", "NOR", "SWE", "POL", "RUS", "TUR", "GRC", "EGY"],
        "Ano": [1347, 1348, 1348, 1348, 1349, 1349, 1350, 1351, 1351, 1347, 1347, 1347],
        "Descricao": [
            "Ponto de entrada (Sicília e Gênova). Devastação total.",
            "Atingida via Marselha. Paris perdeu metade da população.",
            "Chegou via portos do Mediterrâneo.",
            "Entrou por Weymouth. Dizimou Londres.",
            "Avançou pelo Reno. Pogroms contra judeus aumentaram.",
            "Chegou por um navio fantasma em Bergen.",
            "Atingida tardiamente via Noruega.",
            "Menor impacto devido a quarentenas rígidas do Rei Casimiro.",
            "O fim da linha. Atingida por último.",
            "Constantinopla foi um dos primeiros focos.",
            "Espalhou-se pelas ilhas rapidamente.",
            "Alexandria foi atingida quase junto com a Itália."
        ]
    }

    df = pd.DataFrame(dados_peste)

    # 2. CRIAR O MAPA
    fig = px.choropleth(
        df,
        locations="Codigo",      # Coluna com os códigos dos países
        color="Ano",             # A cor depende do Ano
        hover_name="Pais",       # Nome que aparece ao passar o mouse
        hover_data=["Descricao"], # Info extra ao passar o mouse
        color_continuous_scale="Reds", # Escala de cor (Vermelho)
        scope="europe",          # Focar apenas na Europa
        title="A Propagação da Peste Negra (1347-1351)"
    )

    # 3. ESTILIZAR PARA PARECER MEDIEVAL
    fig.update_layout(
        height=800,
        #width=900,
        template="plotly_dark",
        paper_bgcolor="#f4e4bc",   # Cor do fundo do pergaminho (fora do mapa)
        geo=dict(
            bgcolor="#f4e4bc",     # Cor do fundo do mapa (oceanos)
            showlakes=False,       # Remove lagos azuis modernos
            showocean=False,       # Remove azul do oceano
            showcoastlines=True,   # Mostra linhas costeiras
            coastlinecolor="#5c4a35", # Linhas marrom escuro
            showland=True,
            landcolor="#e6d2aa",   # Cor de terra base (bege)
            countrycolor="#5c4a35", # Cor das fronteiras
            projection_type="mercator" # Tipo de projeção plana
        ),
        font=dict(color="#3e2b18", family="Quintessential"), # Fonte medieval
        margin={"r":0,"t":50,"l":0,"b":0} # Remove margens brancas
    )

    # Ajuste da barra de cores (legenda)
    fig.update_coloraxes(colorbar=dict(
        # MUDANÇA AQUI: O title agora agrupa o texto e a fonte
        title=dict(
            text="Ano de Chegada",
            font=dict(color="#3e2b18")
        ),
        tickfont=dict(color="#3e2b18")
    ))

    # Converter para HTML
    grafico_mapa = fig.to_html(full_html=False, include_plotlyjs="cdn")

    return render_template("mapa.html", grafico=grafico_mapa)