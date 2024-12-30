from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import openpyxl 

app = Dash(__name__, external_stylesheets = [dbc.themes.CYBORG])

df = pd.read_excel('dados/dados_cumulativos.xlsx')
caso_Total = df['Casos'].sum()
obitos_Total = df['Óbitos'].sum()

opcoes = list(df.drop(columns = ['Província']).columns)

#Layout
app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4('Cólera'), 
                html.H5('Dados cumulativos (2022 - 2024)')   
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Total de Casos'),
                            html.H5(f'{caso_Total:,}', style = {'color': '#389fd6'}, id = 'casos')
                        ])
                    ], className = 'caso', outline = True)
                ], md = 6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Óbitos'),
                            html.H5(f'{obitos_Total:,}', style = {'color': '#DF2935'}, id = 'obitos')
                        ])
                    ], className = 'card', outline = True)
                ], md = 6)
            ]),

            html.Div([
                dcc.Dropdown(opcoes,
                             value = 'Óbitos',
                             id = 'colunas'
                             ),
                dcc.Graph(id = 'bar_Graph'),
                html.P('A Cólera é perigosa. Prévina a doença lavando as mãos depois de usar  sanitário e antes de levar qualquer alimento à boca. Use água tratada ou fervida. Se tiver diarreia ou vómitos mais de 3 vezes, dirija-se imediatamente a Unidade Sanitária mais próxima (MISAU, 2024).')
            ], className = 'graph')
        ], className = 'sidebar', md = 5),

        dbc.Col([
            html.Iframe(srcDoc = open('mapa.html', 'r').read(), width = '100%', height = '100%')
        ], md = 7, style = {'padding': '0px'})
    ], className = 'geral')
, fluid = True)

@app.callback(
    Output('bar_Graph', 'figure'),
    Input('colunas', 'value')
)
def update_output(value):
    if value == 'Casos':
        fig = px.bar(df, x = df['Província'], y = df[value])
    if value == 'Óbitos':
        fig = px.bar(df, x = df['Província'], y = df[value])
    fig.update_layout(
            paper_bgcolor = '#242424',
            plot_bgcolor = '#242424',
            font = dict(color = 'white'),
            autosize = True,
            margin = dict(l = 10, r = 10, t = 10, b = 10)
        )
    return fig

if __name__ == '__main__':
    app.run_server(debug = True)