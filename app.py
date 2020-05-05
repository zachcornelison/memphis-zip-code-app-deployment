import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly
import pandas as pd
import plotly.graph_objs as go



########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='Digital Divide'

########### Set up the layout
df = pd.read_csv('zipcode-data.csv')
df['Zip Code'] = df['Zip Code'].astype(str)

colors = {
    'background': '#000000',
    'text': '#5d76a9',
    'label': '#f5b112'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div([
        html.Div([
            html.H1(children='Memphis Zip Code Data',
                style={
                    'textAlign': 'center',
                    'font-family':'Verdana',
                    'color': colors['text'],
                    'padding-top': 20
                }),
            html.P(children='Visualizing the Digital Divide in Memphis, TN', 
                style={
                    'textAlign': 'center',
                    'font-size': 24,
                    'font-family':'Verdana',
                    'color': colors['text'],
                    'padding-bottom': 10
            }), 
            html.P(['The data below was gathered from the U.S. Census Bureau table B28002, "PRESENCE AND TYPES OF INTERNET SUBSCRIPTIONS IN HOUSEHOLD".',html.Br(),'The data was filtered by zip code to view data for all 34 zip codes in the Memphis area.',html.Br(),'The complete derived datatable can be viewed below.'],
                style={
                    'margin-left': 100,
                    'margin-right': 100,
                    'font-size': 12,
                    'font-family':'Verdana',
                    'textAlign': 'center',
                    'color': colors['text']
            }),
            html.Label([html.A('Zip code data source', href='https://www.memphisrealtysearch.com/memphis-zip-code-map/', target="_blank")],
                style={
                    'font-size': 10,
                    'font-family':'Verdana',
                    'textAlign': 'center',
                    'color': colors['text']
            }),
            html.Label([html.A('Click here to view the data', href='https://data.census.gov/cedsci/table?q=b28002&tid=ACSDT1Y2018.B28002&vintage=2018&hidePreview=true&moe=false', target="_blank")],
                style={
                    'font-size': 10,
                    'font-family':'Verdana',
                    'textAlign': 'center',
                    'color': colors['text'],
                    'padding-bottom': 20
            })
        ], className='row'),
###############################################################      
        html.Div([
            dcc.Dropdown(
                id='demo-dropdown',
                options=[{'label': i, 'value': i} for i in df['Zip Code']],
                value=['38126', '38139'],
                multi=True
            ),
        html.Div(id='dd-output-container')]),
###############################################################        
        html.Div(children='', style={
                'padding': 15
            }),
###############################################################
        html.Div([
            html.Div([
                dcc.Graph(
                    id='graph1'
                )
            ], className='six columns'
            ),
###############################################################  
            html.Div([
                dcc.Graph(
                    id='graph2'
                )
            ], className='six columns'
            ),
###############################################################
            html.Div([
               dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                    style_cell={'padding': '5px'},
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(212, 225, 250)'
                        }
                    ],
                    style_header={
                        'fontWeight': 'bold'
                    },
                    style_cell_conditional=[
                        {
                            'if': {'column_id': c},
                            'textAlign': 'left'
                        } for c in ['Zip Code', 'Area Name', 'Short Name']
                    ]),
            ], className='twelve columns'),
###############################################################
            html.Div([
                html.Footer(children='Created by Zach Cornelison', style={
                    'margin-top': 40,
                    'backgroundColor': 'black',
                    'color': 'white',
                    'font-size': 8,
                    'width': '100%',
                    'textAlign': 'center'
                }),
                html.Footer([html.A('Github Repository', 
                                    href='https://github.com/zachcornelison/Memphis-Zipcode-Data-Dashboardn', 
                                    target="_blank")], style={
                    'backgroundColor': 'black',
                    'color': 'white',
                    'font-size': 8,
                    'width': '100%',
                    'textAlign': 'center'
                })
            ], className='twelve columns'),
###############################################################  
        ], className='row')
    ], className='ten columns offset-by-one'),    
])

@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)
###############################################################  

@app.callback(
    dash.dependencies.Output('graph1', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_image_src(selector):
    filtered_data = df.loc[df['Zip Code'].isin(selector), 
                            ['Short Name', '% Lacking Broadband Internet', 'Zip Code']]
    figure = {
        'data': [{'x': [area_name], 
                  'y': [percent], 
                  'type': 'bar', 
                  'name': zip_code}
                  for area_name, percent, zip_code in filtered_data.to_numpy()
        ],
        'layout': {
            'title': 'Percent of Homes Lacking Broadband Internet',
            "titlefont": {
                "size": 20,
                'fontWeight': 'bold'
            },
            'yaxis' : dict(
                title='Percent Without Broadband',
                titlefont=dict(
                family='Verdana',
                size=16
            ))
        }
    }
    return figure
###############################################################  
@app.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_image_src(selector):
    filtered_data = df.loc[df['Zip Code'].isin(selector), 
                            ['Short Name', 'Mean Income Past 12 Months', 'Zip Code']]
    figure = {
        'data': [{'x': [area_name], 
                  'y': [income], 
                  'type': 'bar', 
                  'name': zip_code}
                  for area_name, income, zip_code in filtered_data.to_numpy()
        ],
        'layout': {
            'title': 'Mean Income Last 12 Months',
            "titlefont": {
                "size": 20,
                'fontWeight': 'bold'
            },
            'yaxis' : dict(
                title='Income',
                titlefont=dict(
                family='Verdana',
                size=16
            ))
        }
    }
    return figure

if __name__ == '__main__':
    app.run_server()
