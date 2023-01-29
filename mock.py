from dash import Dash, html, dcc, Input, Output
import pandas as pd
import numpy as np
import plotly.express as px

app = Dash()

def generate_table(dataframe, last_px, revcon, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ], style={'marginLeft': 'auto', 'marginRight': 'auto', 'minWidth': '300px', 'width': '300px', 'maxWidth': '300px'})

def create_board():
    opt = ["_____"]*5

    # Random multiple of 2.5 from [30,100]
    strike = np.random.randint(12,40) * 2.5
    # Stock is up to 5 away in increments of 0.01
    stock = strike + np.random.randint(-250,250)/100
    # r/c < 0.16
    revcon = np.random.randint(1,16)/100

    # two strikes on each side
    if strike%5==0:
        strikes = [strike-10, strike-5, strike, strike+5, strike+10]
    else:
        strikes = [strike-5, strike-2.5, strike, strike+2.5, strike+5]

    df = pd.DataFrame({
        "c": opt,
        "K": strikes,
        "p": opt
    })

    return df, strikes, stock, revcon

df, strikes, stock, revcon = create_board()

app.layout = html.Div(style={'backgroundColor': 'white', 'textAlign': 'center'}, children=[

    html.H1(children='Hello Mock',),

    # Board
    html.Div(id="board-rc", children=f'r/c = {revcon}' ),
    html.H4(id="board-title", children=f'Stock = {stock}'),
    html.H4(id="board", children=[generate_table(df, stock, revcon)]),

    # Generate order
    html.Button('New Order', id='order', n_clicks=0),
    html.Br(),
    html.H4(id="cust-order", children=f'Null' ),
    html.Br(),

    # Show ans
    html.Button('Implies', id="vbutton1"),
    html.Div(id = "boxes", children=[html.Div(id='implies',children='0')] ),

    # Reset button
    html.Div(children='___', style={"margin-top": "15px"}),
    html.Button('Regenerate', id='reset-board', n_clicks=0),
])

# Reset the table
@app.callback(
    Output(component_id="board", component_property='children'),
    Output(component_id="board-title", component_property='children'),
    Output(component_id="board-rc", component_property='children'),
    Input(component_id="reset-board", component_property="n_clicks")
)
def update_board(n):
    global stock, revcon, strikes, width
    df, strikes, stock, revcon = create_board()
    width = np.random.uniform(0,0.1)
    smarket = f'{(stock - width/2):.2f} - {(stock + width/2):.2f}'
    return generate_table(df, stock, revcon), smarket, f'r/c = {revcon:.2f}'

# New order
@app.callback(
    Output('cust-order','children'),
    Output('implies','children'),
    Input('order','n_clicks')
)
def random_order(n_clicks):
    global imp

    n=np.random.uniform(-width-0.1,width+0.1)
    imp=stock + n

    # strike
    i = np.random.randint(0,5)
    k=strikes[i]

    combo_type='puts-over' if k>stock else ''
    combo_val= np.abs(imp-k+revcon)

    # type
    i = np.random.randint(0,2)
    otyp='bids' if i else 'offers'


    string=f'Customer {otyp} {combo_val:.2f} for the {k} combo'

    return string, f'{imp:.2f}'

@app.callback(Output('boxes', 'style'),[Input('vbutton1', 'n_clicks')])
def update_style(click):
    if click==None:
       return {'display': 'block'}
    if click%2==0:    
       return {'display': 'block'}
    else:
        return {'display': 'none'}

if __name__ == '__main__':
    app.run_server(debug=True)