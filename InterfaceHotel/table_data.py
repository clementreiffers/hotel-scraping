import sys
from dash import dash_table, html, dcc
import pandas as pd
import columns


stars_choice,date_choice,adulte_choice,enfant_choice,room_choice,lenght = columns.columns()

def table_type(df_column):
    # Note - this only works with Pandas >= 1.0.0

    if sys.version_info < (3, 0):  # Pandas 1.0.0 does not support Python 2
        return 'any'

    if isinstance(df_column.dtype, pd.DatetimeTZDtype):
        return 'datetime',
    elif (isinstance(df_column.dtype, pd.StringDtype) or
            isinstance(df_column.dtype, pd.BooleanDtype) or
            isinstance(df_column.dtype, pd.CategoricalDtype) or
            isinstance(df_column.dtype, pd.PeriodDtype)):
        return 'text'
    elif (isinstance(df_column.dtype, pd.SparseDtype) or
            isinstance(df_column.dtype, pd.IntervalDtype) or
            isinstance(df_column.dtype, pd.Int8Dtype) or
            isinstance(df_column.dtype, pd.Int16Dtype) or
            isinstance(df_column.dtype, pd.Int32Dtype) or
            isinstance(df_column.dtype, pd.Int64Dtype)):
        return 'numeric'
    else:
        return 'any'

df = pd.read_csv("test_carte.csv", sep=";")
df_col = df.drop(['gps','nb_adulte','nb_enfant','nb_chambre'], axis=1)
table = dash_table.DataTable( id = 'table_data',
                              columns=[{'name': i, 'id': i, 'type': table_type(df_col[i])} for i in df_col.columns],
                              sort_action = "native",
                              sort_mode= "multi",
                              css = [{
                                  'selector': 'table',
                                  'rule': 'table-layout: fixed'  # note - this does not work with fixed_rows
                              }],
                              style_table = {'height': 400},
                              style_data =  {
                                 'width': '{}%'.format(100. / lenght),
                                 'textOverflow': 'hidden',
                                 'backgroundColor': '#606165',
                                 'color': 'white'
                             },
                              style_data_conditional=[
                                  {
                                      'if': {'row_index': 'odd'},
                                      'backgroundColor': '#9EA0A7',
                                  }
                              ],
                             style_header = {
                               'backgroundColor': '#1E1E1E',
                               'color': 'white'
                             },
                             style_cell={'textAlign': 'center'}

)




tab1 = html.Div([
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='stars',
                            clearable=False,
                            options=[{'label': i, 'value': i} for i in stars_choice],
                            value=10
                        ),
                        html.P("Nombre d'étoile", style={'font_size': '2px'})
                    ],style={'display':'inline-block', 'width': '{}%'.format(100. / 5)}),
                    html.Div([
                        dcc.Dropdown(
                            id='date',
                            clearable=False,
                            options=[{'label': i, 'value': i} for i in date_choice],
                            value="all"
                        ),
                        html.P("Date de départ", style={'font_size': '2px'})
                    ],style={'display':'inline-block', 'width': '{}%'.format(100. / 5)}),
                    html.Div([
                        dcc.Dropdown(
                            id='nb_adulte',
                            clearable=False,
                            options=[{'label': i, 'value': i} for i in adulte_choice],
                            value=10
                        ),html.P("Nombre d'adulte", style={'font_size': '2px'})
                    ],style={'display':'inline-block', 'width': '{}%'.format(100. / 5)}),
                    html.Div([
                        dcc.Dropdown(
                            id='nb_enfant',
                            clearable=False,
                            options=[{'label': i, 'value': i} for i in enfant_choice],
                            value=10
                        ),
                        html.P("Nombre d'enfant", style={'font_size': '2px'})
                    ],style={'display':'inline-block', 'width': '{}%'.format(100. / 5)}),
                    html.Div([
                        dcc.Dropdown(
                            id='nb_room',
                            clearable=False,
                            options=[{'label': i, 'value': i} for i in room_choice],
                            value=10
                        ),
                        html.P("Nombre de chambre", style={'font_size': '2px'})
                    ],style={'display':'inline-block', 'width': '{}%'.format(100. / 5)})
                ], style={"textAlign":"center"})
])