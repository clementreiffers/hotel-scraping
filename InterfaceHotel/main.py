
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import table_data
import update
import accueil


# Load data
app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])  # initialisation du dash app

# propriétés des onglets

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#000000',
    'color': 'white',
    'padding': '6px'
}


app.layout = html.Div([
    html.H1("Hotel à Paris", style={'textAlign': 'center'}),
    html.P('Projet de Clément REIFFERS, Quentin MOREL, Maëlle MARCELIN, Adrien TIRLEMONT'),
    dcc.Tabs(id="tabs-hotel", value='tab-1-accueil', children=[
        dcc.Tab(label='Accueil', value='tab-1-accueil',style=tab_style, selected_style=tab_selected_style, children=[
            html.Div([
            accueil.accueil
            ])
        ]),
        dcc.Tab(label='Recherche', value='tab-2-recherche',style=tab_style, selected_style=tab_selected_style, children=[
            html.Div([
            table_data.tab1,
            table_data.table
            ])
        ]),
        dcc.Tab(label='Statistique', value='tab-3-statistique', style=tab_style, selected_style=tab_selected_style, children=[
            dcc.Graph(id="graph"),
            dcc.RadioItems(
                id="choice",
                options=["moyenne", "médiane", "étendue"],
                value="moyenne",
                inline=True
            )
        ]),
        dcc.Tab(label='Carte', value='tab-4-carte',style=tab_style, selected_style=tab_selected_style, children=[
                        html.Div([
                            html.Iframe(id='map', srcDoc=open('Carte_hotel.html', 'r').read(), width='80%', height='500vh',)

                        ], style={'textAlign': 'center'})

        ])
    ], style=tabs_styles),
    html.Div(id='tabs-content-hotel')

],style = {'backgroundColor': '#82DAD0'})

@app.callback([Output('table_data', 'data'),
               Output('graph','figure')],
              [Input('stars', 'value'),
               Input('date', 'value'),
               Input('nb_adulte', 'value'),
               Input('nb_enfant', 'value'),
               Input('nb_room', 'value'),
               Input('choice','value')
               ])
def render_content(stars,date,nb_adulte,nb_enfant,nb_room,choice):
    table = update.update_table(stars, date, nb_adulte, nb_enfant, nb_room)
    fig = update.update_graph(choice)
    return table,fig



if __name__ == '__main__':
    app.run_server(debug=True)
