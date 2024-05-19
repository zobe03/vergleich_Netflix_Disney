import plotly.graph_objects as go
import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from dash.dependencies import State


# Daten einlesen
disney = pd.read_csv('/Users/student/Desktop/2Semester/Data Visualization/Abgabe/1_Datensets/disney_plus_titles_cleaned.csv')
netflix = pd.read_csv('/Users/student/Desktop/2Semester/Data Visualization/Abgabe/1_Datensets/netflix_titles_cleaned.csv')

# Genres für Disney+ und Netflix zusammenführen und eindeutige Genres erhalten
genres_disney = disney['listed_in'].str.split(', ', expand=True).stack()
genres_netflix = netflix['listed_in'].str.split(', ', expand=True).stack()
all_genres = pd.concat([genres_disney, genres_netflix]).unique()


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(
        'Film & TV Show Recommendation', 
        style={
            'text-align': 'center',
            'font-style': 'italic',
            'font-family': 'cursive',
            'font-weight': 'bold',
            'font-size': '30px', 
            'color': 'white'
        }
    ),
    html.Div([
        html.Label('Select Content Type:', style={'font-weight': 'bold', 'font-family': 'Droid Serif', 'color': 'white'}),
        dcc.Dropdown(
            id='content-type-dropdown',
            options=[
                {'label': 'Movie', 'value': 'Movie'},
                {'label': 'TV Show', 'value': 'TV Show'}
            ],
            value='Movie',
            style={'width': '100%', 'color': 'black', 'background-color': 'white'}
        ),
    ], style={'width': '20%', 'display': 'inline-block'}),
    html.Div([
        html.Label('Select Genre:', style={'font-weight': 'bold', 'font-family': 'Droid Serif', 'color': 'white'}),
        dcc.Dropdown(
            id='genre-dropdown',
            options=[{'label': genre, 'value': genre} for genre in all_genres],                    
            value=all_genres[1],
            style={'width': '100%', 'color': 'black', 'background-color': 'white'}
        ),
    ], style={'width': '20%', 'display': 'inline-block'}),
    html.Div([
        html.Label('Select Age Limit:', style={'font-weight': 'bold', 'font-family': 'Droid Serif', 'color': 'white'}),
        dcc.Dropdown(
            id='selected-age',
            options=[
                {'label': 'ALL', 'value': 'ALL'},
                {'label': 'Unrated', 'value': 'unrated'},
                {'label': '0-6', 'value': '0-6'},
                {'label': '7-12', 'value': '7-12'},
                {'label': '13-16', 'value': '13-16'},
                {'label': '17+', 'value': '17+'},
                {'label': '17- with Parental Guidance', 'value': '17- PG'}
            ],
            value='ALL',
            style={'width': '100%', 'color': 'black', 'background-color': 'white'}
        ),
    ], style={'width': '20%', 'display': 'inline-block'}),
    html.Div([
        html.Label('Select Column:', style={'font-weight': 'bold', 'font-family': 'Droid Serif', 'color': 'white'}),
        dcc.Dropdown(
            id='column-dropdown',
            options=[
                {'label': 'None', 'value': 'None'},
                {'label': 'Title', 'value': 'title'},
                {'label': 'Description', 'value': 'description'},
            ],
            value='None',
            style={'width': '100%', 'color': 'black', 'background-color': 'white', 'margin-right': '10px'}
        ),
    ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),
    html.Div([
        html.Label('Search:', style={'font-weight': 'bold', 'font-family': 'Droid Serif', 'color': 'white'}),
        dcc.Input(
            id='search-input',
            type='text',
            placeholder='Search...',
            style={'width': '100%', 'height':'30px','color': 'black', 'background-color': 'white'}
        ),
    ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),
    html.Br(),
    html.Br(),
    dcc.Tabs([
        dcc.Tab(label='Disney+', style={'color':'black', 'text-align':'center', 'font-family':'cursive'},children=[
            html.Br(),
            html.Div([
                html.H2('Disney+', style={'text-align': 'center', 'font-style': 'italic', 'font-family':'cursive','font-weight': 'bold', 'font-size': '25px', 'color': 'white'}),
                dash_table.DataTable(
                    id='disney-table',
                    columns=[
                        {'name': 'Title', 'id': 'title'},
                        {'name': 'Description', 'id': 'description'},
                        {'name': 'Duration', 'id': 'duration'},
                        {'name': 'Release Year', 'id': 'release_year'}
                    ],
                    style_table={'width': '99%', 'overflowX': 'auto', 'border': '2px solid darkgrey', 'background': 'rgba(0, 0, 0, 0.7)'},
                    style_cell={'minWidth': '50px', 'maxWidth': '100px', 'whiteSpace': 'normal', 'color': 'white', 'border': '1px solid darkgrey', 'background': 'transparent', 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
                    style_data_conditional=[
                        {   
                            'if' : {'row_index': 'odd'},
                            'backgroundColor': 'rgba(0, 0, 0, 0.4)',
                        },
                        {
                            'if':{'row_index': 'even'},
                            'backgroundColor': 'rgba(0, 0, 0, 0.7)',
                        },
                        {
                            'if': {'column_id': 'description'},
                            'maxWidth': '300px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                        },
                        {
                            'if': {'column_id': 'title'},
                            'maxWidth': '150px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                        },
                    ],    
                ),
                ], style={'width': '99.6%', 'display': 'inline-block', 'vertical-align': 'top', 'border': '2px solid transparent', 'background': 'linear-gradient(to right, #BFF5FD, #142864)'}),
            ]),
        dcc.Tab(label='Netflix', style={'color':'black', 'font-family':'Open Sans', 'text-align':'center'},  children=[
            html.Br(),
            html.Div([
                html.H2('Netflix', style={'text-align': 'center', 'font-style': 'italic', 'font-family':'Open Sans','font-weight': 'bold', 'font-size': '25px', 'color': 'white'}),
                dash_table.DataTable(
                    id='netflix-table',
                    columns=[
                        {'name': 'Title', 'id': 'title'},
                        {'name': 'Description', 'id': 'description'},
                        {'name': 'Duration', 'id': 'duration'},
                        {'name': 'Release Year', 'id': 'release_year'}
                    ],
                    style_table={'width': '99%', 'overflowX': 'auto', 'border': '2px solid darkgrey', 'background': 'rgba(0, 0, 0, 0.7)'},
                    style_cell={'minWidth': '50px', 'maxWidth': '100px', 'whiteSpace': 'normal', 'color': 'white', 'border': '1px solid darkgrey', 'background': 'transparent', 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
                    style_data_conditional=[
                        {   
                            'if' : {'row_index': 'odd'},
                            'backgroundColor': 'rgba(0, 0, 0, 0.4)',
                        },
                        {
                            'if':{'row_index': 'even'},
                            'backgroundColor': 'rgba(0, 0, 0, 0.7)',
                        },
                        {
                            'if': {'column_id': 'description'},
                            'maxWidth': '300px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                        },
                        {
                            'if': {'column_id': 'title'},
                            'maxWidth': '150px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                        },
                    ],
                ),
            ], style={'width': '99.6%', 'display': 'inline-block', 'vertical-align': 'top', 'border': '2px solid transparent', 'background': 'linear-gradient(to right, #000000, #E50914)'}),
        ]),
    ], style={'backgroundColor': 'black', 'color': 'white', 'fontWeight': 'bold', 'border': '1px solid darkgrey', 'borderRadius': '5px'})
], style={'backgroundColor': 'black'})


@app.callback(
    Output('disney-table', 'data'),
    [Input('content-type-dropdown', 'value'),
     Input('genre-dropdown', 'value'),
     Input('selected-age', 'value'),
     Input('search-input', 'value'),
     Input('column-dropdown', 'value')]
)
def update_disney_table(selected_content_type, selected_genre, selected_age, search_value, column):
    try:
        if selected_age == '0-6':
            rating = ['V-Y']
        elif selected_age == '7-12':
            rating = ['TV-Y7', 'TV-Y7-FV']
        elif selected_age == '13-16':
            rating = ['PG-13', 'TV-14']
        elif selected_age == '17+':
            rating = ['NC-17']
        elif selected_age == '17- PG':
            rating = ['PG', 'TV-PG', 'R']
        elif selected_age == 'unrated':
            rating = ['NR', 'UR']
        else:
            rating = ['NR', 'UR', 'TV-G', 'G', 'PG', 'PG-13', 'TV-PG', 'R', 'NC-17', 'TV-14', 'TV-Y7', 'TV-Y7-FV', 'V-Y']

        if selected_content_type == 'Movie':
            data_disney = disney[(disney['type'] == 'Movie') & 
                                 (disney['listed_in'].str.contains(selected_genre)) & 
                                 (disney['rating'].isin(rating))]
        else:
            data_disney = disney[(disney['type'] == 'TV Show') & 
                                 (disney['listed_in'].str.contains(selected_genre)) & 
                                 (disney['rating'].isin(rating))]
        
        if search_value and column != 'None':
            filtered_data = data_disney[data_disney[column].str.contains(search_value, case=False, na=False)]
            return filtered_data[['title', 'description', 'duration', 'release_year']].to_dict('records')
        else:
            return data_disney[['title', 'description', 'duration', 'release_year']].to_dict('records')
    except Exception as e:
        return []
    

@app.callback(
    Output('netflix-table', 'data'),
    [Input('content-type-dropdown', 'value'),
     Input('genre-dropdown', 'value'),
     Input('selected-age', 'value'),
     Input('search-input', 'value'),
     Input('column-dropdown', 'value')]
)
def update_netflix_table(selected_content_type, selected_genre, selected_age, search_value, column):
    try:
        if selected_age == '0-6':
            rating = ['V-Y']
        elif selected_age == '7-12':
            rating = ['TV-Y7', 'TV-Y7-FV']
        elif selected_age == '13-16':
            rating = ['PG-13', 'TV-14']
        elif selected_age == '17+':
            rating = ['NC-17']
        elif selected_age == '17- PG':
            rating = ['PG', 'TV-PG', 'R']
        elif selected_age == 'unrated':
            rating = ['NR', 'UR']
        else:
            rating = ['NR', 'UR', 'TV-G', 'G', 'PG', 'PG-13', 'TV-PG', 'R', 'NC-17', 'TV-14', 'TV-Y7', 'TV-Y7-FV', 'V-Y']

        if selected_content_type == 'Movie':
            data_netflix = netflix[(netflix['type'] == 'Movie') & 
                                   (netflix['listed_in'].str.contains(selected_genre)) & 
                                   (netflix['rating'].isin(rating))]
        else:
            data_netflix = netflix[(netflix['type'] == 'TV Show') & 
                                   (netflix['listed_in'].str.contains(selected_genre)) & 
                                   (netflix['rating'].isin(rating))]
        
        if search_value and column != 'None':
            filtered_data = data_netflix[data_netflix[column].str.contains(search_value, case=False, na=False)]
            return filtered_data[['title', 'description', 'duration', 'release_year']].to_dict('records')
        else:
            return data_netflix[['title', 'description', 'duration', 'release_year']].to_dict('records')
    except Exception as e:
        return []

if __name__ == '__main__':
    app.run_server(debug=True)

