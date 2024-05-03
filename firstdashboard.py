import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# Load the CSV data into a DataFrame
data_path = '/Users/carloscarvalho/PycharmProjects/Usina_Solar_Dashboard/first_dashboard_db.csv' # 'https://raw.githubusercontent.com/loscarlo/solar_pp_monitor/main/first_dashboard_db.csv'
# '/Users/carloscarvalho/Downloads/first_dashboard_colunas_novas_tratado copy 3.csv' # '/home/loscar/mysite//first_dashboard_db.csv'
df = pd.read_csv(data_path)

# Convert the 'data' column to datetime
df['data'] = pd.to_datetime(df['data'], dayfirst=True)

# Extract the month and year from the 'data' column
df['month_year'] = df['data'].dt.to_period('M')

# cleaning '%', 'R$',',' and converting to float
# df['cota_energia'] = df['cota_energia'].str.replace('%','').astype(float)
df['valor_pago'] = df['valor_pago'].str.replace('R$','').str.replace(',','.').astype(float)
df['custo_kWh'] = df['custo_kWh'].str.replace('R$','').str.replace(',','.').astype(float)

# creating column Economia:
df['economia'] = df['energia_inj'] * df['custo_kWh']

# Initialize the Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.themes.SPACELAB, dbc.icons.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# Layout section: Bootstrap (https://hackerthemes.com/bootstrap-cheatsheet/)
# ************************************************************************
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
                html.H1('Usina Solar Pacheco Leão 1559',className='text-center text-primary mb-4'
                ),
         width=12
        )

    ),

    dbc.Row(
        # Date range filter with custom display format (month and year)
        dbc.Col([html.H5('Período:',className='text-center text-primary mb-4'),
            dcc.DatePickerRange(
                id='date-range',
                start_date=df['data'].min(),
                end_date=df['data'].max(),
                display_format='MMM YYYY'
            )],
        width=10),className='text-center text-primary mb-4',
    justify='center'),

    dbc.Row([
        # Combined area and bar chart to display 'energia_gerada' as an area and 'consumo' as bars
        dbc.Col(
            dcc.Graph(id='combined-chart'),# width={'size':5, 'offset':1, 'order':1},
                xs=12, sm=12, md=12, lg=6, xl=6
        ),
        # Doughnut chart to display the relationship between 'unidade' and 'consumo'
        dbc.Col(
            dcc.Graph(id='doughnut-chart'),# width={'size':5, 'offset':1, 'order':1},
                xs=12, sm=12, md=12, lg=4, xl=4
        )
    ], justify='around'),

    dbc.Row([
        # Card to display the average of the sum of 'consumo' by month
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                    html.H4("Consumo Mensal Médio"),
                    html.H3(id='average-box-consumo', className="text-danger")
                    ],
                ),
                className="text-center"
            ),
            xs=12, sm=12, md=12, lg=4, xl=4
        ),
        dbc.Col(
            # Card to display the average of the sum of 'energia_gerada' by month
            dbc.Card(
                dbc.CardBody(
                    [
                    html.H4("Energia Gerada Mensal Média"),
                    html.H3(id='average-box-energia', className="text-primary")
                    ],
                ),
                className="text-center"
            ),
            xs=12, sm=12, md=12, lg=4, xl=4
        )
    ], justify='around'),

    dbc.Row([
        # Container for the new area chart Saldo de Credito
        dbc.Col(
            dcc.Graph(id='saldo-credito-chart'),# width={'size':5, 'offset':1, 'order':1},
                xs=12, sm=12, md=12, lg=6, xl=6
        ),
        # Container for the dounut chart Saldo por unidade
        dbc.Col(
            dcc.Graph(id='donut-chart-credito-mes'),# width={'size':5, 'offset':1, 'order':1},
                xs=12, sm=12, md=12, lg=4, xl=4
        )

    ], justify='around'),

    # Container for cards estoque e duracao por unidade
    dbc.Row([
        dbc.Col([
            html.P("Estoque por Unidade:",
                   className="text-nowrap"),
            dbc.CardGroup([

                dbc.Card(
                    dbc.CardBody(
                        [
                        html.H4("Ju & Rafael", className="text-nowrap"),
                        html.H3(id='estoque-cred-unid-1'),
                        html.H5(id='estoque-duracao-unid-1')
                        ], className="border-start border-primary border-5"
                    ),
                    className="text-center m-4",
                ),

                dbc.Card(
                    dbc.CardBody(
                        [
                        html.H4("Luciana", className="text-nowrap"),
                        html.H3(id='estoque-cred-unid-2'),
                        html.H5(id='estoque-duracao-unid-2')
                        ], className="border-start border-primary border-5"
                    ),
                    className="text-center m-4"
                ),

                dbc.Card(
                    dbc.CardBody(
                        [
                        html.H4("Valdione", className="text-nowrap"),
                        html.H3(id='estoque-cred-unid-3'),
                        html.H5(id='estoque-duracao-unid-3')
                        ], className="border-start border-primary border-5"
                    ),
                    className="text-center m-4"
                ),
            ])
        ], xs=12, sm=12, md=12, lg=12, xl=12),

    ], align='end'),

    dbc.Row([
        # Container for bar chart gasto por mes
        dbc.Col(
            dcc.Graph(id='gasto-energia-chart'),# width={'size':5, 'offset':1, 'order':1},
                xs=12, sm=12, md=12, lg=5, xl=5
        ),
        # Container for bar chart Economia por mes
        dbc.Col(
            dcc.Graph(id='economia-chart'),# width={'size':5, 'offset':1, 'order':1},
                xs=12, sm=12, md=12, lg=5, xl=5
        )
    ],justify='around'),

    dbc.Row([
        # Container for Card Despesa Mensal Média
        dbc.Col([
            # html.P("Estoque por Unidade:",
            #        className="text-nowrap"),
            dbc.Card(
                dbc.CardBody(
                    [
                    html.H4("Despesa Mensal Média", className="text-nowrap"),
                    html.H3(id='average-box-gasto'),
                    # html.H5(id='estoque-duracao-unid-2')
                    ], className="border-start border-warning border-5"
                ),
                className="text-center m-4"
            ),
        ], xs=12, sm=12, md=12, lg=6, xl=6),

        # Container for Card  Economia Mensal Média
        dbc.Col([
            # html.P("Estoque por Unidade:",
            #        className="text-nowrap"),
            dbc.Card(
                dbc.CardBody(
                    [
                    html.H4("Economia Mensal Média", className="text-nowrap"),
                    html.H3(id='average-box-economia'),
                    # html.H5(id='estoque-duracao-unid-3')
                    ], className="border-start border-success border-5"
                ),
                className="text-center m-4"
            ),
        ], xs=12, sm=12, md=12, lg=6, xl=6),

    ], align='around'),

    dbc.Row([
        # Container for Card  Despesa Mensal Média por unidade
        dbc.Col([
            # html.P("Estoque por Unidade:",
            #        className="text-nowrap"),
            dbc.CardGroup([

                dbc.Card(
                    dbc.CardBody(
                        [
                        html.H6("Carlos", className="text-nowrap"),
                        html.H5(id='average-box-gasto-unid-0'),
                        # html.H5(id='estoque-duracao-unid-3')
                        ], className="border-start border-warning border-5"
                    ),
                    className="text-center m-4"
                ),

                dbc.Card(
                    dbc.CardBody(
                        [
                        html.H6("Ju & Rafael", className="text-nowrap"),
                        html.H5(id='average-box-gasto-unid-1'),
                        # html.H5(id='estoque-duracao-unid-2')
                        ], className="border-start border-warning border-5"
                    ),
                    className="text-center m-4"
                ),

                dbc.Card(
                    dbc.CardBody(
                        [
                        html.H6("Luciana", className="text-nowrap"),
                        html.H5(id='average-box-gasto-unid-2'),
                        # html.H5(id='estoque-duracao-unid-3')
                        ], className="border-start border-warning border-5"
                    ),
                    className="text-center m-4"
                ),

                dbc.Card(
                    dbc.CardBody(
                        [
                        html.H6("Valdione", className="text-nowrap"),
                        html.H5(id='average-box-gasto-unid-3'),
                        # html.H5(id='estoque-duracao-unid-3')
                        ], className="border-start border-warning border-5"
                    ),
                    className="text-center m-4"
                ),
            ]),

        ], xs=12, sm=12, md=12, lg=6, xl=6),

        # Container for Card  Economia Mensal Média por unidade
        dbc.Col([
            # html.P("Estoque por Unidade:",
            #        className="text-nowrap"),
            dbc.CardGroup([

                dbc.Card(
                    dbc.CardBody(
                        [
                        html.H6("Carlos", className="text-nowrap"),
                        html.H5(id='average-box-economia-unid-0'),
                        # html.H5(id='estoque-duracao-unid-3')
                        ], className="border-start border-success border-5"
                    ),
                    className="text-center m-4"
                ),

                dbc.Card(
                    dbc.CardBody(
                        [
                        html.H6("Ju & Rafael", className="text-nowrap"),
                        html.H5(id='average-box-economia-unid-1'),
                        # html.H5(id='estoque-duracao-unid-2')
                        ], className="border-start border-success border-5"
                    ),
                    className="text-center m-4"
                ),

                dbc.Card(
                    dbc.CardBody(
                        [
                        html.H6("Luciana", className="text-nowrap"),
                        html.H5(id='average-box-economia-unid-2'),
                        # html.H5(id='estoque-duracao-unid-3')
                        ], className="border-start border-success border-5"
                    ),
                    className="text-center m-4"
                ),

                dbc.Card(
                    dbc.CardBody(
                        [
                        html.H6("Valdione", className="text-nowrap"),
                        html.H5(id='average-box-economia-unid-3'),
                        # html.H5(id='estoque-duracao-unid-3')
                        ], className="border-start border-success border-5"
                    ),
                    className="text-center m-4"
                ),
            ]),


        ], xs=12, sm=12, md=12, lg=6, xl=6)

    ]),

    dbc.Row([
        # Combined Gauges displaying Payback status in %
        dbc.Col([html.H3("Pay Back Status:", className="text-nowrap"),
            dcc.Graph(id='gauge-chart')],
                xs=12, sm=12, md=12, lg=10, xl=10
        ),
    ], justify='around'),

], fluid=True)

# Define a callback to update the combined chart, doughnut chart, average boxes, the new area chart, and the Cards (scoreboards) based on the selected date range
@app.callback(
    [Output('combined-chart', 'figure'), Output('doughnut-chart', 'figure'),
     Output('average-box-consumo', 'children'), Output('average-box-energia', 'children'),
     Output('saldo-credito-chart', 'figure'), Output('donut-chart-credito-mes', 'figure'),
     Output('estoque-cred-unid-1', 'children'),Output('estoque-cred-unid-2', 'children'),Output('estoque-cred-unid-3', 'children'),Output('estoque-duracao-unid-1', 'children'),Output('estoque-duracao-unid-2', 'children'),Output('estoque-duracao-unid-3', 'children'),
     Output('gasto-energia-chart', 'figure'), Output('economia-chart', 'figure'),
     Output('average-box-gasto', 'children'), Output('average-box-economia', 'children'),
     Output('average-box-gasto-unid-0', 'children'),Output('average-box-gasto-unid-1', 'children'),Output('average-box-gasto-unid-2', 'children'),Output('average-box-gasto-unid-3', 'children'),
     Output('average-box-economia-unid-0', 'children'),Output('average-box-economia-unid-1', 'children'),Output('average-box-economia-unid-2', 'children'),Output('average-box-economia-unid-3', 'children'),Output('gauge-chart', 'figure'),
     ],
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_charts(start_date, end_date):
    filtered_df = df[(df['data'] >= start_date) & (df['data'] <= end_date)]

    # Create a figure with 'energia_gerada' as an area and 'consumo' as bars
    combined_fig = go.Figure()

    # Add 'energia_gerada' as an area
    combined_fig.add_trace(go.Scatter(x=filtered_df['data'], y=filtered_df['energia_gerada'],
                                      mode='lines', fill='tozeroy', name='Energia Gerada'))

    # Add 'consumo' as bars
    combined_fig.add_trace(go.Bar(x=filtered_df['data'], y= filtered_df['consumo'], name='Consumo'))

    # Update the layout of the combined chart
    combined_fig.update_layout(title='Consumo vs Energia por Mês'#, xaxis_title='Date'
                                , yaxis_title='(kWh)')

    # Create the doughnut chart to display the relationship between 'unidade' and 'consumo' with absolute numbers
    doughnut_fig = px.pie(filtered_df, names='unidade', values='consumo', title='% Consumo por Unidade', hole=0.90)

    # Calculate the average of the sum of 'consumo' by month
    monthly_avg_consumo = filtered_df.groupby('month_year')['consumo'].sum().mean()

    # Calculate the average of the sum of 'energia_gerada' by month
    monthly_avg_energia = filtered_df.groupby('month_year')['energia_gerada'].sum().mean()

    # Calculate the average of the sum of 'Gasto' by month
    monthly_avg_gasto = filtered_df.groupby('month_year')['valor_pago'].sum().mean()

    # Calculate the average of the sum of 'Economia' by month
    monthly_avg_economia = filtered_df.groupby('month_year')['economia'].sum().mean()

    # Calculate the average of the sum of 'Gasto' by month by 'Unidade'
    gasto_uni = filtered_df.groupby('unidade')['valor_pago'].mean()

    # Calculate the average of the sum of 'Economia' by month by 'unidade'
    economia_uni = filtered_df.groupby('unidade')['economia'].mean()

# ++++++++++++++++++++++++++++  necessary for gauges ++++++++++++++++++++++++++++++++++++++++++

    # Calculate the sum of 'Economia' by 'unidade'
    economia_uni_acum = filtered_df.groupby('unidade')['economia'].sum()

    # Calculate the sum of 'Economia 'global'
    economia_total_acum = filtered_df['economia'].sum()

    # Calculate the average of the sum of 'consumo' by 'unidade'
    avg_consumo_uni = filtered_df.groupby(['unidade'])['consumo'].mean()

    # Calculando o % do investimento recuperado e o tempo pendente para o payback

    invest_total = 75203.66
    invest_valdione = 21928.08
    invest_jurafael = 21928.08
    invest_luciana = 17542.46
    invest_carlos = 13805.04

    pb_percent_global = (economia_total_acum / invest_total) * 100
    pb_percent_valdione = (economia_uni_acum.iloc[-1] / invest_valdione) * 100
    pb_percent_jurafael = (economia_uni_acum.iloc[-3] / invest_jurafael) * 100
    pb_percent_luciana = (economia_uni_acum.iloc[-2] / invest_luciana) * 100
    pb_percent_carlos = (economia_uni_acum.iloc[0] / invest_carlos) * 100

    pb_status_global = invest_total - economia_total_acum
    pb_status_valdione = invest_valdione - economia_uni_acum.iloc[-1]
    pb_status_luciana = invest_luciana - economia_uni_acum.iloc[-2]
    pb_status_jurafael = invest_jurafael - economia_uni_acum.iloc[-3]
    pb_status_carlos = invest_carlos - economia_uni_acum.iloc[0]

    time_to_pb_global = pb_status_global / monthly_avg_consumo
    time_to_pb_valdione = pb_status_valdione / avg_consumo_uni.iloc[-1]
    time_to_pb_jurafael = pb_status_jurafael / avg_consumo_uni.iloc[-3]
    time_to_pb_luciana = pb_status_luciana / avg_consumo_uni.iloc[-2]
    time_to_pb_carlos = pb_status_carlos / avg_consumo_uni.iloc[0]

    # Pay Back Status Gauge charts grid :

    gauge_fig = go.Figure()

    gauge_fig.add_trace(go.Indicator(

        value=pb_percent_global,
        mode='number+gauge',
        number={'suffix': '%'},
        gauge={
            'shape': "bullet",
            'axis': {'range': [None, 100]}},
        # domain = {'x': [0, 1], 'y': [0, 1]},
        domain={'row': 0, 'column': 0},
        title={'text': "Global",
               'font_size':22}))

    gauge_fig.add_trace(go.Indicator(

        value=pb_percent_valdione,
        mode='number+gauge',
        number={'suffix': '%'},
        gauge={
            'shape': "bullet",
            'axis': {'range': [None, 100]}},
        domain={'row': 2, 'column': 0},
        # domain = {'x': [0.05, 0.5], 'y': [0.35, 0.45]},
        title={'text': "Valdione",
               'font_size':16}))

    gauge_fig.add_trace(go.Indicator(
        value=pb_percent_jurafael,
        mode='number+gauge',
        number={'suffix': '%'},
        gauge={
            'shape': "bullet",
            'axis': {'range': [None, 100]}},
        domain={'row': 2, 'column': 1},
        title={'text': "Ju & Rafael",
               'font_size':16}))

    gauge_fig.add_trace(go.Indicator(
        value=pb_percent_luciana,
        mode='number+gauge',
        number={'suffix': '%'},
        gauge={
            'shape': "bullet",
            'axis': {'range': [None, 100]}},
        domain={'row': 4, 'column': 1},
        title={'text': "Luciana",
               'font_size':16}))

    gauge_fig.add_trace(go.Indicator(
        value=pb_percent_carlos,
        mode='number+gauge',
        number={'suffix': '%'},
        gauge={
            'shape': "bullet",
            'axis': {'range': [None, 100]}},
        domain={'row': 4, 'column': 0},
        title={'text': "Carlos",
               'font_size':16}))

    gauge_fig.update_layout(
        grid={'rows': 5, 'columns': 2, 'pattern': "independent"})


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Calculate the amount of credits (global)
    # saldo_credito_global = filtered_df.groupby('month_year')['saldo_credito']

    # Calculate the amount of credits (per unit)
    saldo_credito_uni = filtered_df.groupby('unidade')['credito_mes'].sum()

    # Calculate the average of consumo (per unit)
    avg_consumo_uni = filtered_df.groupby(['unidade'])['consumo'].mean()

    # Create the new area chart to display the relationship between 'data' and 'saldo_credito'
    saldo_credito_fig = px.area(
        filtered_df, x='data', y='saldo_credito',
        color='unidade',
        title='Créditos Acumulados',
        labels={'saldo_credito': '(kWh)'}
    )

    # Create the donut chart to display the relationship between 'unidade' and 'credito_mes'
    donut_chart_credito_mes = px.pie(filtered_df, names='unidade', values='credito_mes', title='% Créditos Acumulados por Unidade',
                                     hole=0.9)

    # Create the Gasto_Energia chart to display the relationship between 'data' and 'valor_pago'
    gasto_energia_fig = px.bar(
        filtered_df, x='data', y='valor_pago',
        color='unidade',
        title='Despesa por Mês',
        labels={'valor_pago': '(R$)'}
    )

    # Create the  economia-chart to display the relationship between 'data' and 'economia'
    economia_chart_fig = px.bar(
        filtered_df, x='data', y='economia',
        color='unidade',
        title='Economia por Mês',
        labels={'economia': '(R$)'}
    )

    return combined_fig, doughnut_fig, f'{monthly_avg_consumo:.0f} kWh', f'{monthly_avg_energia:.0f} kWh', saldo_credito_fig, donut_chart_credito_mes, f'{saldo_credito_uni.iloc[1]:.0f} kWh', f'{saldo_credito_uni.iloc[2]:.0f} kWh', f'{saldo_credito_uni.iloc[3]:.0f} kWh', f'{saldo_credito_uni.iloc[1]/avg_consumo_uni.iloc[1]:.0f} Meses', f'{saldo_credito_uni.iloc[2]/avg_consumo_uni.iloc[2]:.0f} Meses', f'{saldo_credito_uni.iloc[-1]/avg_consumo_uni.iloc[-1]:.0f} Meses', gasto_energia_fig, economia_chart_fig, f'R$ {monthly_avg_gasto:.2f}', f'R$ {monthly_avg_economia:.2f}', f'R$ {gasto_uni.iloc[0]:.2f}', f'R$ {gasto_uni.iloc[1]:.2f}', f'R$ {gasto_uni.iloc[2]:.2f}', f'R$ {gasto_uni.iloc[-1]:.2f}', f' R$ {economia_uni.iloc[0]:.2f}', f'R$ {economia_uni.iloc[1]:.2f}', f'R$ {economia_uni.iloc[2]:.2f}', f'R$ {economia_uni.iloc[-1]:.2f}', gauge_fig,



if __name__ == '__main__':
    app.run_server(debug=True)
